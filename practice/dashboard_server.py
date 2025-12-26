#!/usr/bin/env python3
"""
StepCode 실시간 수업 대시보드 서버 (정적 파일 + WebSocket)

실행:
  cd practice
  pip install aiohttp
  python dashboard_server.py

접속:
  학생:  http://<host>:8000/practice.html?set=...&room=A&student=1
  교사:  http://<host>:8000/teacher.html?room=A
"""
import json
import time
import asyncio
import os
import secrets
from pathlib import Path
import hmac
import hashlib
import base64
import secrets

from aiohttp import web, WSMsgType

BASE_DIR = Path(__file__).resolve().parent  # practice 폴더에서 실행하는 걸 전제로 함

HOST_PIN_FILE = BASE_DIR / ".host_token"
HOST_COOKIE_NAME = "stepcode_host"
HOST_SESSION_TTL_SEC = 60 * 60 * 8  # 8시간 (원하면 조절)

def load_host_pin() -> str:
    if HOST_PIN_FILE.exists():
        return HOST_PIN_FILE.read_text(encoding="utf-8").strip()

    pin = secrets.token_urlsafe(12)
    HOST_PIN_FILE.write_text(pin, encoding="utf-8")
    print(f"[StepCode] HOST_PIN created: {pin} (saved to {HOST_PIN_FILE.name})")
    return pin

HOST_PIN = load_host_pin()
HOST_SIGN_KEY = hashlib.sha256(HOST_PIN.encode("utf-8")).digest()

def _b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")

def _b64url_decode(s: str) -> bytes:
    pad = "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode((s + pad).encode("utf-8"))

def make_host_cookie() -> str:
    exp = int(time.time()) + HOST_SESSION_TTL_SEC
    payload = str(exp).encode("utf-8")
    sig = hmac.new(HOST_SIGN_KEY, payload, hashlib.sha256).hexdigest().encode("utf-8")
    return _b64url_encode(payload + b"." + sig)

# [dashboard_server.py] (상단쪽) "쿠키 검증"으로 되어있는 첫 번째 is_host_request()를 아래로 교체

def is_host_request(request: web.Request) -> bool:
    # 1) 쿠키 기반(teacher에서 PIN 로그인 후 발급되는 쿠키)
    token = request.cookies.get(HOST_COOKIE_NAME) or ""
    if token:
        try:
            raw = _b64url_decode(token)
            exp_b, sig_b = raw.split(b".", 1)
            exp = int(exp_b.decode("utf-8"))
            if exp >= int(time.time()):
                expected = hmac.new(HOST_SIGN_KEY, exp_b, hashlib.sha256).hexdigest().encode("utf-8")
                if hmac.compare_digest(sig_b, expected):
                    return True
        except Exception:
            pass

    # 2) (레거시) URL host=1&token=... 도 허용하고 싶으면 유지
    q = request.rel_url.query
    if q.get("host") == "1" and q.get("token") == HOST_TOKEN:
        return True

    return False


# ---------------- Host-only 기능 토큰 ----------------
# 학생에게는 노출하지 않고(HTML에 주입하지 않음), 호스트(교사)가 URL로만 접근할 수 있게 하기 위한 토큰.
# - 환경변수 STEPCODE_HOST_TOKEN 이 있으면 그걸 사용
# - 없으면 practice 폴더에 .host_token 파일로 1회 생성 후 재사용
HOST_TOKEN_FILE = BASE_DIR / ".host_token"


def load_or_create_host_token() -> str:
    env = (os.environ.get("STEPCODE_HOST_TOKEN") or "").strip()
    if env:
        return env

    try:
        if HOST_TOKEN_FILE.exists():
            t = HOST_TOKEN_FILE.read_text(encoding="utf-8").strip()
            if t:
                return t
    except Exception:
        pass

    t = secrets.token_urlsafe(18)
    try:
        HOST_TOKEN_FILE.write_text(t, encoding="utf-8")
    except Exception:
        # 파일 저장 실패해도 동작은 해야 하므로 그냥 반환
        pass
    return t


HOST_TOKEN = load_or_create_host_token()

# room -> { "students": { studentKey: statusDict }, "teachers": set(ws) }
ROOMS = {}

GC_EVERY_SEC = 10
EXPIRE_SEC = 180  # 학생이 이 시간 이상 업데이트 없으면 목록에서 제거


def now_ms() -> int:
    return int(time.time() * 1000)


def get_room(room_id: str):
    room_id = room_id or "default"
    room = ROOMS.get(room_id)
    if not room:
        room = {"students": {}, "teachers": set()}
        ROOMS[room_id] = room
    return room


async def broadcast_teachers(room_id: str, message: dict):
    room = get_room(room_id)
    dead = []
    data = json.dumps(message, ensure_ascii=False)
    for ws in list(room["teachers"]):
        try:
            await ws.send_str(data)
        except Exception:
            dead.append(ws)
    for ws in dead:
        room["teachers"].discard(ws)

async def host_status(request: web.Request):
    return web.json_response({"isHost": is_host_request(request)}, dumps=lambda x: json.dumps(x, ensure_ascii=False))

async def host_login(request: web.Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    pin = str(body.get("pin") or "").strip()
    if pin != HOST_PIN:
        return web.json_response({"ok": False, "error": "invalid_pin"}, status=403, dumps=lambda x: json.dumps(x, ensure_ascii=False))

    resp = web.json_response({"ok": True}, dumps=lambda x: json.dumps(x, ensure_ascii=False))
    resp.set_cookie(
        HOST_COOKIE_NAME,
        make_host_cookie(),
        httponly=True,
        samesite="Lax",
        max_age=HOST_SESSION_TTL_SEC,
        path="/",
    )
    return resp

async def host_logout(request: web.Request):
    resp = web.json_response({"ok": True}, dumps=lambda x: json.dumps(x, ensure_ascii=False))
    resp.del_cookie(HOST_COOKIE_NAME, path="/")
    return resp

async def deny_private(request: web.Request):
    raise web.HTTPNotFound()


async def ws_handler(request: web.Request):
    ws = web.WebSocketResponse(heartbeat=25)  # ping/pong
    await ws.prepare(request)
    req_is_host = is_host_request(request)

    role = None
    room_id = "default"
    student_key = None

    async def send_snapshot():
        room = get_room(room_id)
        items = list(room["students"].values())
        await ws.send_str(json.dumps({"type": "snapshot", "room": room_id, "items": items}, ensure_ascii=False))

    try:
        async for msg in ws:
            if msg.type != WSMsgType.TEXT:
                continue

            try:
                data = json.loads(msg.data)
            except Exception:
                continue

            mtype = data.get("type")

            if mtype == "hello":
                role = data.get("role")
                room_id = data.get("room") or "default"

                room = get_room(room_id)

                if role == "teacher":
                    if not req_is_host:
                        await ws.send_str(json.dumps({"type": "error", "error": "host_required"}, ensure_ascii=False))
                        await ws.close()
                        return ws
                    room["teachers"].add(ws)
                    await ws.send_str(json.dumps({"type": "hello_ack", "role": "teacher", "room": room_id}, ensure_ascii=False))
                    await send_snapshot()
                else:
                    # student
                    sid = str(data.get("studentId") or "").strip() or "unknown"
                    student_key = f"{room_id}:{sid}"

                    await ws.send_str(json.dumps({"type": "hello_ack", "role": "student", "room": room_id, "studentKey": student_key}, ensure_ascii=False))

                    # hello만 와도 기본 엔트리 생성
                    st = {
                        "studentKey": student_key,
                        "room": room_id,
                        "studentId": sid,
                        "displayName": data.get("displayName") or sid,
                        "lastSeenAt": now_ms(),
                    }
                    room["students"][student_key] = st
                    await broadcast_teachers(room_id, {"type": "status", "room": room_id, "studentKey": student_key, "payload": st})

            elif mtype == "status" and role != "teacher":
                if not room_id:
                    room_id = data.get("room") or "default"
                room = get_room(room_id)

                payload = data.get("payload") or {}
                sid = str(payload.get("studentId") or data.get("studentId") or "").strip() or "unknown"
                if student_key is None:
                    student_key = f"{room_id}:{sid}"

                payload["studentKey"] = student_key
                payload["room"] = room_id
                payload["studentId"] = sid
                payload["displayName"] = payload.get("displayName") or payload.get("studentId") or sid
                payload["lastSeenAt"] = now_ms()

                room["students"][student_key] = payload
                await broadcast_teachers(room_id, {"type": "status", "room": room_id, "studentKey": student_key, "payload": payload})

            elif mtype == "snapshot_request" and role == "teacher":
                await send_snapshot()

    finally:
        # 연결 종료 정리
        try:
            if role == "teacher":
                get_room(room_id)["teachers"].discard(ws)
            elif role != "teacher" and student_key:
                room = get_room(room_id)
                # 바로 제거하지 말고 lastSeenAt만 갱신해두면 GC에서 자연스럽게 제거됨
                st = room["students"].get(student_key)
                if st:
                    st["lastSeenAt"] = now_ms()
                    st["disconnected"] = True
                    await broadcast_teachers(room_id, {"type": "status", "room": room_id, "studentKey": student_key, "payload": st})
        except Exception:
            pass

    return ws


async def gc_task(app: web.Application):
    while True:
        await asyncio.sleep(GC_EVERY_SEC)
        t = now_ms()
        for room_id, room in list(ROOMS.items()):
            students = room["students"]
            expired = [k for k, v in students.items() if t - int(v.get("lastSeenAt") or 0) > EXPIRE_SEC * 1000]
            for k in expired:
                students.pop(k, None)
                await broadcast_teachers(room_id, {"type": "bye", "room": room_id, "studentKey": k})


async def on_startup(app: web.Application):
    app["gc"] = asyncio.create_task(gc_task(app))


async def on_cleanup(app: web.Application):
    task = app.get("gc")
    if task:
        task.cancel()


# [dashboard_server.py] (하단쪽) "URL에 host=1&token=..." 설명이 있는 두 번째 is_host_request()는
# 쿠키용 is_host_request()를 덮어써서 항상 false가 되는 원인이므로 "이름을 변경"해야 함.

# (기존) def is_host_request(request: web.Request) -> bool:
def is_host_token_request(request: web.Request) -> bool:
    """(레거시) URL에 host=1&token=<HOST_TOKEN> 이 포함되면 호스트로 간주"""
    q = request.rel_url.query
    if q.get("host") == "1" and q.get("token") == HOST_TOKEN:
        return True
    return False



async def practice_html_handler(request: web.Request):
    """practice.html을 읽어서 host 플래그를 head에 주입해서 반환."""
    html_path = BASE_DIR / "practice.html"
    try:
        text = html_path.read_text(encoding="utf-8")
    except Exception:
        raise web.HTTPNotFound()

    is_host = is_host_request(request)

    # 학생에게는 토큰을 절대 주지 않음(노출 금지)
    injected = (
        "<script>window.__STEPCODE_IS_HOST__="
        + ("true" if is_host else "false")
        + ";</script>\n"
    )

    # </head> 앞에 주입(없으면 맨 앞)
    if "</head>" in text:
        text = text.replace("</head>", injected + "</head>", 1)
    else:
        text = injected + text

    return web.Response(text=text, content_type="text/html", charset="utf-8")


def main():
    app = web.Application()
    app.router.add_get("/ws", ws_handler)
    app.router.add_get("/api/host/status", host_status)
    app.router.add_post("/api/host/login", host_login)
    app.router.add_post("/api/host/logout", host_logout)

    # 비공개 파일 직접 접근 차단 (show_index도 끄는 걸 권장)
    app.router.add_route("*", "/.host_token", deny_private)


    # practice.html은 host 플래그를 HTML에 주입해야 하므로 정적 라우팅보다 먼저 별도 처리
    app.router.add_get("/practice.html", practice_html_handler)

    # 정적 파일 제공 (practice 폴더 전체)
    app.router.add_static("/", path=str(BASE_DIR), show_index=False)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    # 서버 콘솔에 호스트 토큰을 출력(교사만 확인)
    # ※ 이 토큰을 URL에 붙여야 practice.html의 교사 전용 버튼(인쇄/로그)이 보입니다.
    print("[StepCode] HOST_TOKEN:", HOST_TOKEN)
    print("[StepCode] Host mode URL example:")
    print("          http://<host>:8000/practice.html?set=...&room=...&host=1&token=<HOST_TOKEN>")

    web.run_app(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
