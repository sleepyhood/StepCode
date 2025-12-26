/* StepCode 교사용 대시보드 */
(() => {
  const $ = (sel) => document.querySelector(sel);

  const tbody = $("#tbody");
  const roomInput = $("#room");
  const btnConnect = $("#connect");
  const btnRefresh = $("#refresh");

  const hostBadge = $("#host-badge");
  const hostAuth = $("#host-auth");
  const hostPin = $("#host-pin");
  const btnHostLogin = $("#host-login");
  const btnHostLogout = $("#host-logout");

  const state = {
    ws: null,
    room: "default",
    rows: new Map(),      // studentKey -> <tr>
    last: new Map(),      // studentKey -> {progressKey, lastProgressAt}
    connectedAt: 0,
    payloads: new Map(),   // studentKey -> payload
    isHost: false
  };

  let resortTimer = null;

function scheduleResort() {
  if (resortTimer) return;
  resortTimer = setTimeout(() => {
    resortTimer = null;
    resortRows();
  }, 80);
}

function resortRows() {
  const items = [];
  for (const [k, p] of state.payloads.entries()) {
    const tr = state.rows.get(k);
    if (!tr) continue;
    items.push({ k, p, tr });
  }

  // 도움 요청(손들기) > 최신 접속 순
  items.sort((a, b) => {
    const ha = a.p.helpActive ? 1 : 0;
    const hb = b.p.helpActive ? 1 : 0;
    if (hb !== ha) return hb - ha;

    const la = Number(a.p.lastSeenAt || 0);
    const lb = Number(b.p.lastSeenAt || 0);
    return lb - la;
  });

  for (const it of items) tbody.appendChild(it.tr);
}


  function getRoomFromQuery() {
    const p = new URLSearchParams(location.search);
    return (p.get("room") || "").trim();
  }

  function fmtAgo(ms) {
    if (!ms) return "-";
    const sec = Math.max(0, Math.floor((Date.now() - ms) / 1000));
    if (sec < 60) return `${sec}s`;
    const m = Math.floor(sec / 60);
    const s = sec % 60;
    return `${m}m ${s}s`;
  }

  async function apiHostStatus() {
  const r = await fetch("/api/host/status", { credentials: "same-origin" });
  if (!r.ok) return { isHost: false };
  return await r.json();
}

async function apiHostLogin(pin) {
  const r = await fetch("/api/host/login", {
    method: "POST",
    headers: { "content-type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ pin }),
  });
  return { ok: r.ok, data: await r.json().catch(() => ({})) };
}

async function apiHostLogout() {
  await fetch("/api/host/logout", { method: "POST", credentials: "same-origin" }).catch(() => {});
}

function applyHostUi(isHost) {
  state.isHost = !!isHost;

  if (hostBadge) hostBadge.hidden = !state.isHost;
  if (hostAuth) hostAuth.hidden = state.isHost;

  if (btnConnect) btnConnect.disabled = !state.isHost;
  if (btnRefresh) btnRefresh.disabled = !state.isHost;

  if (btnHostLogout) btnHostLogout.hidden = !state.isHost;
}

async function bootstrapHostAuth() {
  const s = await apiHostStatus();
  applyHostUi(!!s.isHost);

  // 잠금 상태면 테이블 안내 표시
  if (!state.isHost) {
    if (tbody) tbody.innerHTML = `<tr><td colspan="8" class="small">교사 인증이 필요합니다. (PIN 입력 후 교사모드 ON)</td></tr>`;
  } else {
    // host면 기존 편의 기능 유지: room 있으면 자동 연결
    if (roomInput.value) connect();
  }
}


  function safeText(v) {
    return String(v ?? "").replace(/[<>]/g, "");
  }

  function ensureRow(studentKey) {
    if (state.rows.has(studentKey)) return state.rows.get(studentKey);

    // 첫 row 생성 시, "빈 상태" row 제거
    if (tbody.children.length === 1 && tbody.querySelector("td[colspan]")) {
      tbody.innerHTML = "";
    }

    const tr = document.createElement("tr");
    tr.setAttribute("data-student", studentKey);
    tr.innerHTML = `
      <td class="mono"></td>
      <td></td>
      <td></td>
      <td class="mono"></td>
      <td class="mono"></td>
      <td></td>
      <td class="mono right"></td>
      <td class="mono"></td>
    `;
    tbody.appendChild(tr);
    state.rows.set(studentKey, tr);
    return tr;
  }

  function makeModeBadges(payload) {
    const mode = payload.mode || "practice"; // "class" | "practice"
    const bucket = payload.bucket || "";
    const tags = [];
    tags.push(`<span class="tag ${mode}">${mode === "class" ? "수업" : "연습"}</span>`);
    if (bucket) tags.push(`<span class="tag ${bucket}">${bucket === "core" ? "핵심" : "보강"}</span>`);
    return tags.join("");
  }

  function makeTopTries(payload) {
    const top = Array.isArray(payload.topTries) ? payload.topTries : [];
    if (!top.length) return "-";
    return top
      .map((x) => {
        const mark = x.lastIsCorrect === true ? "✅" : x.lastIsCorrect === false ? "❌" : "";
        const n = Number(x.attempts) || 0;
        return `${safeText(x.qid)}:${n}${mark}`;
      })
      .join(" · ");
  }

  function detectStuckSignal(studentKey, payload) {
    // "막힘"은 완벽하게 판단할 수 없으니, 운영에 도움이 되는 약한 신호만 표시
    const progress = payload.progress || {};
    const total = Number(progress.total) || 0;
    const answered = Number(progress.answered) || 0;
    const correct = Number(progress.correct) || 0;
    const pKey = `${answered}/${correct}/${total}`;

    const prev = state.last.get(studentKey) || { progressKey: "", lastProgressAt: Date.now() };
    if (prev.progressKey !== pKey) {
      prev.progressKey = pKey;
      prev.lastProgressAt = Date.now();
      state.last.set(studentKey, prev);
      return ""; // 방금 진전 있음
    }

    // 진전 없이 오래 있음 + 채점 TOP가 높으면 막힘 가능성 ↑
    const idleSec = Math.floor((Date.now() - prev.lastProgressAt) / 1000);
    const top = Array.isArray(payload.topTries) ? payload.topTries : [];
    const maxTry = top.reduce((m, x) => Math.max(m, Number(x.attempts) || 0), 0);

    if (idleSec >= 180 && maxTry >= 2) return "🚧 3분↑ 정체 + 재채점多";
    if (idleSec >= 240) return "⏳ 4분↑ 정체";
    if (maxTry >= 4) return "🔁 동일문항 4회↑";
    return "";
  }

  function render(payload) {
    const studentKey = payload.studentKey;
    const tr = ensureRow(studentKey);
state.payloads.set(studentKey, payload);

    const name = payload.displayName || payload.studentId || studentKey;
    const setTitle = payload.setTitle || payload.setId || "-";
    const setId = payload.setId ? `<span class="small mono">${safeText(payload.setId)}</span>` : "";
    const progress = payload.progress || {};
    const pText = `${Number(progress.answered)||0}/${Number(progress.total)||0} · ${Number(progress.correct)||0}✓`;

    const lastAct = payload.lastActivityAt || payload.lastSeenAt || 0;
    const stale = Date.now() - (payload.lastSeenAt || 0);

    tr.classList.toggle("stale", stale > 30_000);
    tr.classList.toggle("dead", payload.disconnected === true);

    const stuck = detectStuckSignal(studentKey, payload);

    const gradeAttempts = Number(payload.gradeAttemptsToday) || 0;

    const tds = tr.querySelectorAll("td");
    tds[0].innerHTML = `<div class="mono">${safeText(name)}</div><div class="small mono">${safeText(payload.studentId || "")}</div>`;
    tds[1].innerHTML = `<div>${safeText(setTitle)}</div>${setId}`;
    tds[2].innerHTML = makeModeBadges(payload);
    tds[3].textContent = pText;
    tds[4].textContent = fmtAgo(lastAct);
    const helpText = payload.helpActive
      ? `🙋 도움 요청${payload.helpQid ? " · Q:" + payload.helpQid : ""}`
      : "";

    tds[5].textContent = helpText || stuck || "-";
    tds[6].textContent = String(gradeAttempts);
    tds[7].textContent = makeTopTries(payload);

    scheduleResort();

  }

  function connect() {
    if (!state.isHost) {
  alert("교사 인증(PIN)이 필요합니다.");
  return;
}

    const room = (roomInput.value || "").trim() || "default";
    state.room = room;

    if (state.ws) {
      try { state.ws.close(); } catch (_) {}
      state.ws = null;
    }

    const proto = location.protocol === "https:" ? "wss" : "ws";
    const wsUrl = `${proto}://${location.host}/ws`;

    const ws = new WebSocket(wsUrl);
    state.ws = ws;

    ws.addEventListener("open", () => {
      state.connectedAt = Date.now();
      ws.send(JSON.stringify({ type: "hello", role: "teacher", room }));
    });

    ws.addEventListener("message", (ev) => {
      let msg = null;
      try { msg = JSON.parse(ev.data); } catch (_) { return; }
      if (msg.type === "snapshot") {
        const items = Array.isArray(msg.items) ? msg.items : [];
        items.forEach(render);
      } else if (msg.type === "status") {
        if (msg.payload) render(msg.payload);
      } else if (msg.type === "bye") {
        // 삭제는 보수적으로: row를 지우기보단 회색 처리하려면 여기서 처리
        // (지금은 단순히 남겨둠)
      }
    });

    ws.addEventListener("close", () => {
      // 표시만: 자동 재연결은 사용자가 눌러도 됨
      btnConnect.textContent = "재연결";
    });

    ws.addEventListener("error", () => {
      btnConnect.textContent = "재연결";
    });

    btnConnect.textContent = "연결중...";
    setTimeout(() => (btnConnect.textContent = "연결"), 500);
  }

  btnConnect.addEventListener("click", connect);
  btnRefresh.addEventListener("click", () => {
    if (state.ws && state.ws.readyState === WebSocket.OPEN) {
      state.ws.send(JSON.stringify({ type: "snapshot_request" }));
    }
  });

  // 초기 room 값 세팅
  const initialRoom = getRoomFromQuery();
  if (initialRoom) roomInput.value = initialRoom;

  // 바로 연결(편의)
btnHostLogin?.addEventListener("click", async () => {
  const pin = (hostPin?.value || "").trim();
  if (!pin) return;

  const res = await apiHostLogin(pin);
  if (!res.ok) {
    alert("PIN이 올바르지 않습니다.");
    return;
  }

  // 쿠키 발급 후 상태 재조회 → UI 해제
  await bootstrapHostAuth();
});

btnHostLogout?.addEventListener("click", async () => {
  await apiHostLogout();
  applyHostUi(false);
});

bootstrapHostAuth();
})();
