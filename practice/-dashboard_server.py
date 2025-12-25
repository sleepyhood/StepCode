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
from pathlib import Path

from aiohttp import web, WSMsgType

BASE_DIR = Path(__file__).resolve().parent  # practice 폴더에서 실행하는 걸 전제로 함

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


async def ws_handler(request: web.Request):
    ws = web.WebSocketResponse(heartbeat=25)  # ping/pong
    await ws.prepare(request)

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


def main():
    app = web.Application()
    app.router.add_get("/ws", ws_handler)

    # 정적 파일 제공 (practice 폴더 전체)
    app.router.add_static("/", path=str(BASE_DIR), show_index=True)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    web.run_app(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
