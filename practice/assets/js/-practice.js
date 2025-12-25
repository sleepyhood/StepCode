// practice/assets/js/practice.js

let currentSetData = null;
let currentLang = "c"; // 지금은 C만, 나중에 언어별 코드 확장

// ===== CodeMirror (code 입력만 하이라이트) =====
const CODEMIRROR_EDITORS = new Map();

function getCodeMirrorMode(lang) {
  if (lang === "python") return "python";
  if (lang === "java") return "text/x-java";
  return "text/x-csrc"; // c
}

function destroyCodeMirrorEditors() {
  for (const ed of CODEMIRROR_EDITORS.values()) {
    try {
      ed.toTextArea();
    } catch (_) {}
  }
  CODEMIRROR_EDITORS.clear();
}

function upgradeCodeInputsToCodeMirror(rootEl) {
  if (!rootEl || !window.CodeMirror) return;

  const mode = getCodeMirrorMode(currentLang);

  const textareas = rootEl.querySelectorAll(
    'textarea.answer-input[data-qtype="code"][data-question]'
  );

  textareas.forEach((ta) => {
    const qid = ta.getAttribute("data-question");
    if (!qid || CODEMIRROR_EDITORS.has(qid)) return;

    const editor = CodeMirror.fromTextArea(ta, {
      mode,
      lineNumbers: false,
      indentUnit: 2,
      tabSize: 2,
      viewportMargin: Infinity,
    });

    // 저장된 답 복원
    const saved = currentAnswers && currentAnswers[qid];
    if (typeof saved === "string") editor.setValue(saved);

    editor.on("change", () => {
      recordAnswer(qid, editor.getValue());
    });

    CODEMIRROR_EDITORS.set(qid, editor);
  });
}

// ▼ 아래 세 줄 추가 ▼
let currentSetId = null;
let currentAnswers = {};
const ANSWER_STORAGE_PREFIX = "stepcode:answers:";

// ===== Markdown(지문) 렌더링 =====
let MD = null;

function getMarkdownRenderer() {
  if (MD) return MD;
  // 두 라이브러리가 모두 있어야 안전하게 HTML 렌더
  if (!window.markdownit || !window.DOMPurify) return null;

  MD = window.markdownit({
    html: false, // md 안의 raw HTML 금지(보안)
    linkify: true,
    breaks: true,
  });

  return MD;
}

function renderMarkdownInto(targetEl, mdText) {
  const raw = String(mdText ?? "");
  const md = getMarkdownRenderer();

  if (!md) {
    // 라이브러리가 없으면 안전하게 평문으로
    targetEl.textContent = raw;
    return;
  }

  const html = md.render(raw);
  const safe = window.DOMPurify.sanitize(html);
  targetEl.innerHTML = safe;
}

// ===== 수업모드(코칭) =====
const MODE_STORAGE_KEY = "stepcode:practiceMode"; // "normal" | "class"
const COACH_STATE_PREFIX = "stepcode:coachState:";

let practiceMode = "normal";
let forcedMode = null; // "normal" | "class" | null (페이지가 강제하는 모드)
let activeBucket = "core"; // "core" | "supp"
let coachState = {}; // { [qid]: { touchedAt, stage, wrongGrades, explainUnlocked, solved, explainOpen } }
let coachTicker = null;
let coachSaveTimer = null;

function isClassMode() {
  return practiceMode === "class";
}

function getForcedModeFromDom() {
  const m = document?.body?.dataset?.mode;
  return m === "class" || m === "normal" ? m : null;
}

function detectPracticeMode() {
  // 우선순위: (1) 페이지 강제(data-mode) > (2) query ?mode= > (3) localStorage
  const forced = getForcedModeFromDom();
  if (forced) return forced;

  const saved = localStorage.getItem(MODE_STORAGE_KEY);
  if (saved === "class" || saved === "normal") return saved;

  const q = new URLSearchParams(location.search).get("mode");
  if (q === "class" || q === "normal") return q;
  return "normal";
}

function updateModeHeaderUi() {
  // (선택) lesson.html에서만 존재하는 UI들
  const badge = document.getElementById("mode-badge");
  if (badge) badge.hidden = !isClassMode();

  const policy = document.getElementById("mode-policy");
  if (!policy) return;

  if (!isClassMode()) {
    policy.textContent = "";
    return;
  }

  const cooldownSec = Math.round(GRADE_COOLDOWN_MS / 1000);
  const rec = formatMs(getSetRecommendedMs());
  // wrongGrades는 현재 로직에서 문항당 최대 2회까지 누적/해설 해금에 사용
  policy.textContent = `수업모드 · 권장 ${rec} · 채점 쿨다운 ${cooldownSec}초 · 문항당 오답채점 2회 → 해설 해금`;
}

function getCoachKey(setId) {
  return `${COACH_STATE_PREFIX}${setId}`;
}

function loadCoachState(setId) {
  try {
    const raw = localStorage.getItem(getCoachKey(setId));
    return raw ? JSON.parse(raw) : {};
  } catch (_) {
    return {};
  }
}

function scheduleSaveCoachState() {
  if (!currentSetId) return;
  if (coachSaveTimer) return;
  coachSaveTimer = setTimeout(() => {
    try {
      localStorage.setItem(
        getCoachKey(currentSetId),
        JSON.stringify(coachState)
      );
    } catch (_) {}
    coachSaveTimer = null;
  }, 300);
}

function ensureCoachRow(qid) {
  if (!coachState[qid]) {
    coachState[qid] = {
      touchedAt: null,
      stage: 0, // 0:none, 1:hint1, 2:hint2
      wrongGrades: 0, // 문항당 채점 실패 횟수
      explainUnlocked: false,
      solved: false,
      explainOpen: false,
    };
  }
  return coachState[qid];
}

function getAnswerStorageKey(setId) {
  return `${ANSWER_STORAGE_PREFIX}${setId}`;
}

function loadStoredAnswers(setId) {
  if (!window.localStorage) return {};
  try {
    const raw = localStorage.getItem(getAnswerStorageKey(setId));
    return raw ? JSON.parse(raw) : {};
  } catch (e) {
    console.warn("failed to load stored answers", e);
    return {};
  }
}

function saveStoredAnswers(setId, answers) {
  if (!window.localStorage) return;
  try {
    localStorage.setItem(getAnswerStorageKey(setId), JSON.stringify(answers));
  } catch (e) {
    console.warn("failed to save answers", e);
  }
}

function recordAnswer(questionId, value) {
  if (!currentSetId) return;

  // (추가) 수업모드면 이 문항 '시작 시간' 기록
  if (isClassMode() && typeof getSolveElapsedNow === "function") {
    const row = ensureCoachRow(questionId);
    if (row.touchedAt == null) {
      row.touchedAt = getSolveElapsedNow(); // 누적 풀이시간 기준
      scheduleSaveCoachState();
    }
  }

  currentAnswers[questionId] = value;
  saveStoredAnswers(currentSetId, currentAnswers);
  updateProgressUi();
}

// ▲ 여기까지 추가 ▲

// ====== (추가) 문항별 채점 메타 ======
let qGradeMeta = null; // { date: "YYYY-MM-DD", byQ: { [qid]: { attempts, correct, lastIsCorrect, lastAt } } }
const Q_GRADE_META_PREFIX = "stepcode:qGradeMeta:";

function getQGradeMetaKey(setId) {
  return `${Q_GRADE_META_PREFIX}${setId}`;
}

function loadQGradeMeta(setId) {
  const today = getTodayYmd();
  if (!window.localStorage) return { date: today, byQ: {} };

  try {
    const raw = localStorage.getItem(getQGradeMetaKey(setId));
    if (!raw) return { date: today, byQ: {} };
    const parsed = JSON.parse(raw);

    if (!parsed || parsed.date !== today) return { date: today, byQ: {} };
    if (!parsed.byQ || typeof parsed.byQ !== "object") parsed.byQ = {};
    return parsed;
  } catch (_) {
    return { date: today, byQ: {} };
  }
}

function saveQGradeMeta(setId, meta) {
  if (!window.localStorage) return;
  try {
    localStorage.setItem(getQGradeMetaKey(setId), JSON.stringify(meta));
  } catch (_) {}
}

function ensureQGradeMetaLoaded() {
  if (!currentSetId) return;
  if (!qGradeMeta) qGradeMeta = loadQGradeMeta(currentSetId);
  // 날짜 바뀌었으면 리셋
  const today = getTodayYmd();
  if (qGradeMeta.date !== today) qGradeMeta = { date: today, byQ: {} };
}

function bumpQGradeAttempt(qid, isCorrect) {
  ensureQGradeMetaLoaded();
  const byQ = (qGradeMeta.byQ ||= {});
  const row = (byQ[qid] ||= {
    attempts: 0,
    correct: 0,
    lastIsCorrect: null,
    lastAt: 0,
  });

  if (row.lastIsCorrect === true && isCorrect === true) {
    row.lastAt = Date.now(); // (선택) 마지막 채점 시각만 갱신
    row.lastIsCorrect = true; // 유지
    return;
  }

  row.attempts += 1;
  if (isCorrect) row.correct += 1;
  row.lastIsCorrect = !!isCorrect;
  row.lastAt = Date.now();
}

function updateQGradeBadge(qid) {
  const el = document.querySelector(`[data-qgrade="${qid}"]`);
  if (!el) return;

  ensureQGradeMetaLoaded();
  const row = qGradeMeta.byQ?.[qid];
  const n = row ? Number(row.attempts) || 0 : 0;

  el.classList.remove("correct", "incorrect");

  if (!row || n === 0) {
    el.textContent = `오늘 채점 0회`;
    return;
  }

  const mark = row.lastIsCorrect ? "✅" : "❌";
  el.textContent = `오늘 채점 ${n}회 ${mark}`;
  el.classList.add(row.lastIsCorrect ? "correct" : "incorrect");
}

function refreshAllQGradeBadges() {
  const qs = currentSetData?.problems || [];
  qs.forEach((q) => updateQGradeBadge(q.id));
}

// ====== (추가) 진행도(푼/맞은) ======
function getActiveQuestions() {
  const all = currentSetData?.problems || [];
  const coreCount = Number(currentSetData?.coreCount ?? 6);

  if (!isClassMode()) return all;

  return all.filter((q, idx) => {
    const bucket =
      q.bucket === "supp" || q.bucket === "core"
        ? q.bucket
        : idx < coreCount
        ? "core"
        : "supp";
    return bucket === activeBucket;
  });
}

function isAnswered(q) {
  const v = currentAnswers?.[q.id];
  if (q.type === "mcq")
    return v !== undefined && v !== null && String(v) !== "";
  return String(v ?? "").trim().length > 0;
}

function updateProgressUi() {
  const wrap = document.getElementById("progress-wrap");
  if (!wrap || !currentSetData) return;

  ensureQGradeMetaLoaded();
  const byQ = qGradeMeta?.byQ || {};

  const qs = getActiveQuestions();
  const total = qs.length;

  let answered = 0;
  let correct = 0;

  qs.forEach((q) => {
    if (isAnswered(q)) answered++;
    if (byQ[q.id]?.lastIsCorrect === true) correct++;
  });

  const solveLabel = document.getElementById("progress-label-solve");
  const solveFill = document.getElementById("progress-fill-solve");
  const corLabel = document.getElementById("progress-label-correct");
  const corFill = document.getElementById("progress-fill-correct");

  if (solveLabel) solveLabel.textContent = `풀이 ${answered}/${total}`;
  if (corLabel) corLabel.textContent = `정답 ${correct}/${total}`;

  const pSolve = total ? (answered / total) * 100 : 0;
  const pCor = total ? (correct / total) * 100 : 0;

  if (solveFill) solveFill.style.width = `${pSolve}%`;
  if (corFill) corFill.style.width = `${pCor}%`;
}

function appendQGradeBadge(headerEl, qid) {
  const tag = document.createElement("span");
  tag.className = "q-grade-tag";
  tag.setAttribute("data-qgrade", qid);
  tag.textContent = "오늘 채점 0회";
  headerEl.appendChild(tag);
  updateQGradeBadge(qid);
}

// ====== 채점 메타(제출 횟수/쿨다운) ======
const GRADE_META_PREFIX = "stepcode:gradeMeta:";
const GRADE_COOLDOWN_MS = 20000; // 20초 (원하면 숫자만 바꾸면 됨)

function getGradeMetaKey(setId) {
  return `${GRADE_META_PREFIX}${setId}`;
}

function getTodayYmd() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function loadGradeMeta(setId) {
  const today = getTodayYmd();

  if (!window.localStorage) {
    return { date: today, attempts: 0, lastGradeAt: 0 };
  }

  try {
    const raw = localStorage.getItem(getGradeMetaKey(setId));
    if (!raw) return { date: today, attempts: 0, lastGradeAt: 0 };

    const parsed = JSON.parse(raw);
    if (!parsed || parsed.date !== today) {
      return { date: today, attempts: 0, lastGradeAt: 0 };
    }

    return {
      date: today,
      attempts: Number(parsed.attempts) || 0,
      lastGradeAt: Number(parsed.lastGradeAt) || 0,
    };
  } catch (e) {
    return { date: today, attempts: 0, lastGradeAt: 0 };
  }
}

function saveGradeMeta(setId, meta) {
  if (!window.localStorage) return;
  try {
    localStorage.setItem(getGradeMetaKey(setId), JSON.stringify(meta));
  } catch (e) {
    console.warn("failed to save grade meta", e);
  }
}

// ====== 풀이 타이머(스톱워치) ======
const SOLVE_TIMER_PREFIX = "stepcode:solveTime:";
const SOLVE_TICK_MS = 250;
const SOLVE_SAVE_EVERY_MS = 2000;

let solveElapsedMs = 0; // 누적(저장되는) 시간
let solveStartAt = 0; // running 시작 시각(Date.now)
let solveRunning = false;
let solveTicker = null;
let solveLastSavedAt = 0;
let solveTimerInitialized = false;

function getSolveTimerKey(setId) {
  return `${SOLVE_TIMER_PREFIX}${setId}`;
}

function loadSolveElapsed(setId) {
  if (!window.localStorage) return 0;
  try {
    const raw = localStorage.getItem(getSolveTimerKey(setId));
    const n = raw ? Number(raw) : 0;
    return Number.isFinite(n) ? n : 0;
  } catch (e) {
    return 0;
  }
}

function saveSolveElapsed(setId, ms) {
  if (!window.localStorage) return;
  try {
    localStorage.setItem(
      getSolveTimerKey(setId),
      String(Math.max(0, Math.floor(ms)))
    );
  } catch (e) {
    // ignore
  }
}

function getSolveElapsedNow() {
  if (!solveRunning) return solveElapsedMs;
  return solveElapsedMs + (Date.now() - solveStartAt);
}

function formatElapsed(ms) {
  const totalSec = Math.floor(ms / 1000);
  const h = Math.floor(totalSec / 3600);
  const m = Math.floor((totalSec % 3600) / 60);
  const s = totalSec % 60;

  if (h > 0) {
    return `${String(h).padStart(2, "0")}:${String(m).padStart(
      2,
      "0"
    )}:${String(s).padStart(2, "0")}`;
  }
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function renderSolveTimerUi(paused) {
  const wrap = document.querySelector(".solve-timer");
  const labelEl = wrap ? wrap.querySelector(".solve-timer-label") : null;
  const timerEl = document.getElementById("solve-timer");
  const stateEl = document.getElementById("solve-timer-state");
  if (!timerEl) return;

  // 기본: 스톱워치(누적)
  let mainText = formatElapsed(getSolveElapsedNow());
  let stateText = paused ? "일시정지" : "";

  // 수업모드: 타이머(남은 시간)
  if (isClassMode() && currentSetData) {
    const remain = getSetRecommendedMs() - getSolveElapsedNow();

    if (labelEl) labelEl.textContent = "⏳";
    if (wrap)
      wrap.title = "남은 시간 (권장시간 기준, 탭을 벗어나면 자동 일시정지)";

    if (remain >= 0) {
      mainText = formatElapsed(remain);
    } else {
      // 0초 이후: 00:00 유지 + 초과분은 상태에 +로 표시
      mainText = "00:00";
      if (!paused) stateText = `+${formatElapsed(-remain)}`;
    }
  } else {
    // 일반모드: 스톱워치
    if (labelEl) labelEl.textContent = "⏱";
    if (wrap) wrap.title = "누적 풀이시간 (탭을 벗어나면 자동 일시정지)";
  }

  timerEl.textContent = mainText;
  if (wrap) wrap.classList.toggle("paused", !!paused);
  if (stateEl) stateEl.textContent = stateText;
}

function tickSolveTimer() {
  renderSolveTimerUi(false);

  const now = Date.now();
  if (now - solveLastSavedAt >= SOLVE_SAVE_EVERY_MS) {
    solveLastSavedAt = now;
    saveSolveElapsed(currentSetId, getSolveElapsedNow());
  }
}

function startSolveTimer() {
  if (!currentSetId) return;
  if (solveRunning) return;

  solveRunning = true;
  solveStartAt = Date.now();
  solveLastSavedAt = Date.now();

  // 즉시 UI 반영
  renderSolveTimerUi(false);

  if (solveTicker) clearInterval(solveTicker);
  solveTicker = setInterval(tickSolveTimer, SOLVE_TICK_MS);
}

function pauseSolveTimer(save = true) {
  if (!currentSetId) return;

  if (solveRunning) {
    solveElapsedMs = solveElapsedMs + (Date.now() - solveStartAt);
    solveRunning = false;
    solveStartAt = 0;
  }

  if (solveTicker) {
    clearInterval(solveTicker);
    solveTicker = null;
  }

  renderSolveTimerUi(true);
  if (save) saveSolveElapsed(currentSetId, solveElapsedMs);
}

function initSolveTimerOnce() {
  if (solveTimerInitialized) return;
  solveTimerInitialized = true;

  // 탭 숨김/복귀 시 자동 일시정지/재개
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) pauseSolveTimer(true);
    else startSolveTimer();
  });

  // 페이지 이탈 시 저장
  window.addEventListener("pagehide", () => pauseSolveTimer(true));
  window.addEventListener("beforeunload", () => pauseSolveTimer(true));
}

function setupSolveTimerForCurrentSet() {
  if (!currentSetId) return;

  initSolveTimerOnce();

  // 이전 기록 로드
  solveElapsedMs = loadSolveElapsed(currentSetId);
  solveRunning = false;
  solveStartAt = 0;

  // 초기 표시
  renderSolveTimerUi(document.hidden);

  // 보이는 상태면 바로 시작
  if (!document.hidden) startSolveTimer();
}

// ====== 교사용 로그(내보내기) ======
function pad2(n) {
  return String(n).padStart(2, "0");
}

function formatStampForFilename(d) {
  return (
    d.getFullYear() +
    pad2(d.getMonth() + 1) +
    pad2(d.getDate()) +
    "_" +
    pad2(d.getHours()) +
    pad2(d.getMinutes()) +
    pad2(d.getSeconds())
  );
}

function downloadTextFile(filename, text, mime = "text/plain;charset=utf-8") {
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function csvEscapeCell(v) {
  const s = String(v ?? "");
  const escaped = s.replace(/"/g, '""');
  return `"${escaped}"`;
}

function makeTeacherLogSnapshot() {
  const now = new Date();

  const meta =
    typeof loadGradeMeta === "function" ? loadGradeMeta(currentSetId) : null;

  const elapsedMs =
    typeof getSolveElapsedNow === "function" ? getSolveElapsedNow() : null;

  // 채점 로직과 동일한 방식으로 "현재 답안 기준" 점수 스냅샷 계산
  const questions = (currentSetData && currentSetData.problems) || [];
  let correctCount = 0;
  const perQuestion = [];

  questions.forEach((q) => {
    let isCorrect = false;

    if (q.type === "mcq") {
      const selected = currentAnswers[q.id];
      isCorrect = String(selected) === String(q.correctIndex);
    } else if (q.type === "short") {
      const val = String((currentAnswers && currentAnswers[q.id]) ?? "");
      if (q.expectedAnyOf) {
        const norm = normalizeText(val);
        isCorrect = q.expectedAnyOf.some((ans) => normalizeText(ans) === norm);
      } else if (q.expectedText) {
        isCorrect = normalizeText(val) === normalizeText(q.expectedText);
      }
    } else if (q.type === "code") {
      const userCode = String((currentAnswers && currentAnswers[q.id]) ?? "");
      const normUser = normalizeCode(userCode);

      let candidates = [];
      if (Array.isArray(q.expectedCode)) candidates = q.expectedCode;
      else if (typeof q.expectedCode === "string")
        candidates = [q.expectedCode];
      if (Array.isArray(q.expectedCodes))
        candidates = candidates.concat(q.expectedCodes);

      isCorrect = candidates
        .filter(Boolean)
        .some((code) => normalizeCode(code) === normUser);
    }

    if (isCorrect) correctCount++;

    // 답안은 교사용 로그에 남기되, 정답(기대값)은 포함하지 않음(학생에게 유출 방지)
    perQuestion.push({
      id: q.id,
      type: q.type,
      isCorrect,
      answer: currentAnswers ? currentAnswers[q.id] : undefined,
    });
  });

  // (선택) 코드/결과 혼동 의심 개수
  let suspiciousCount = 0;
  if (typeof getFormatWarning === "function") {
    perQuestion.forEach((pq) => {
      const q = questions.find((x) => x.id === pq.id);
      if (!q || (q.type !== "short" && q.type !== "code")) return;
      const ans = String((currentAnswers && currentAnswers[q.id]) ?? "");
      if (getFormatWarning(q, ans)) suspiciousCount++;
    });
  }

  return {
    version: 1,
    exportedAt: now.toISOString(),
    set: {
      id: currentSetId,
      title: (currentSetData && currentSetData.title) || "",
      categoryId: (currentSetData && currentSetData.categoryId) || "",
    },
    lang: currentLang,
    solveElapsedMs: elapsedMs,
    gradeMeta: meta, // {date, attempts, lastGradeAt}
    score: { correct: correctCount, total: questions.length },
    suspiciousCount,
    perQuestion,
  };
}

function teacherLogToCsvRows(log) {
  const rows = [];
  rows.push([
    "exportedAt",
    "setId",
    "setTitle",
    "categoryId",
    "lang",
    "solveElapsedMs",
    "attemptsToday",
    "lastGradeAt",
    "correct",
    "total",
    "questionId",
    "type",
    "isCorrect",
    "answer",
  ]);

  const attemptsToday = log.gradeMeta ? log.gradeMeta.attempts : "";
  const lastGradeAt = log.gradeMeta ? log.gradeMeta.lastGradeAt : "";
  const correct = log.score ? log.score.correct : "";
  const total = log.score ? log.score.total : "";

  (log.perQuestion || []).forEach((pq) => {
    const ans = pq.answer;
    const ansStr =
      typeof ans === "string" ? ans : ans == null ? "" : String(ans);
    // CSV 한 줄 안정화를 위해 줄바꿈은 \n 문자열로 치환
    const safeAnswer = ansStr.replace(/\r?\n/g, "\\n");

    rows.push([
      log.exportedAt,
      log.set.id,
      log.set.title,
      log.set.categoryId,
      log.lang,
      log.solveElapsedMs ?? "",
      attemptsToday,
      lastGradeAt,
      correct,
      total,
      pq.id,
      pq.type,
      pq.isCorrect ? "1" : "0",
      safeAnswer,
    ]);
  });

  return rows;
}

function setupExportLog() {
  const btn = document.getElementById("export-log-btn");
  if (!btn) return;

  btn.addEventListener("click", (e) => {
    if (!currentSetId || !currentSetData) {
      alert("세트가 아직 로드되지 않았습니다.");
      return;
    }

    const log = makeTeacherLogSnapshot();
    const stamp = formatStampForFilename(new Date());
    const baseName = `stepcode_log_${currentSetId}_${stamp}`;

    const wantCsv = e.ctrlKey || e.metaKey;
    const wantBoth = e.shiftKey;

    if (!wantCsv || wantBoth) {
      downloadTextFile(
        `${baseName}.json`,
        JSON.stringify(log, null, 2),
        "application/json;charset=utf-8"
      );
    }

    if (wantCsv || wantBoth) {
      const rows = teacherLogToCsvRows(log);
      const csvText = rows
        .map((r) => r.map(csvEscapeCell).join(","))
        .join("\n");
      downloadTextFile(`${baseName}.csv`, csvText, "text/csv;charset=utf-8");
    }
  });
}

document.addEventListener("DOMContentLoaded", initPractice);

// ====== 초기화 ======
async function initPractice() {
  const params = new URLSearchParams(location.search);
  const setId = params.get("set");

  const container = document.getElementById("problem-container");
  const titleSpan = document.getElementById("set-title");

  if (!setId) {
    container.textContent = "잘못된 접근입니다. (set 파라미터가 없습니다)";
    return;
  }

  // 버튼 클릭 시 햅틱 피드백(진동) 및 부드러운 스크롤 효과
  document.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => {
      // 2025 UX: 작은 소리나 진동 효과(모바일 환경)를 고려한 피드백
      if (navigator.vibrate) navigator.vibrate(5);
    });
  });

  // 상단바 스크롤 애니메이션: 스크롤 시 상단바가 더 투명해지거나 작아지는 효과
  window.addEventListener("scroll", () => {
    const topBar = document.querySelector(".top-bar");
    if (window.scrollY > 50) {
      topBar.style.transform = "scale(0.98)";
      topBar.style.opacity = "0.9";
    } else {
      topBar.style.transform = "scale(1)";
      topBar.style.opacity = "1";
    }
  });
  try {
    // 세트 JSON 불러오기
    currentSetData = await ProblemService.loadSet(setId);
    // 세트 정보 + 로컬 저장된 답안 불러오기
    currentSetId = setId;
    currentAnswers = loadStoredAnswers(setId);
    qGradeMeta = loadQGradeMeta(currentSetId);

    // (추가) 모드 로드 + UI 반영
    forcedMode = getForcedModeFromDom();
    practiceMode = detectPracticeMode();
    document.body.classList.toggle("mode-class", isClassMode());

    // (추가) 코칭 상태 로드
    coachState = isClassMode() ? loadCoachState(currentSetId) : {};

    setupSolveTimerForCurrentSet();

    // 제목 표시 (수업모드는 화면에서 확실히 티 나게)
    const baseTitle = currentSetData.title || "연습장";
    titleSpan.textContent = isClassMode()
      ? `수업모드 · ${baseTitle}`
      : baseTitle;

    // (선택) lesson.html 전용 배지/정책 UI 갱신
    updateModeHeaderUi();

    // 언어 셀렉트 (지금은 C만)
    setupLangSelect(currentSetData.availableLanguages || ["c"]);

    // 문제 렌더
    renderSet();

    setupClassModeControls(); // 상단 버튼들
    if (isClassMode()) {
      startCoachTicker();
    }

    // HUD 세팅
    setupHud();

    // 채점 버튼 연결
    setupGrading();

    // ✅ 여기(바로 다음)
    setupExportLog();
    setupWorksheetPrint(); // ✅ 학습지 출력

    setupRealtimeDashboard(); // ← 추가
  } catch (err) {
    console.error(err);
    container.textContent = "문제를 불러오는 중 오류가 발생했습니다.";
  }
}

// ====== 언어 선택 (지금은 거의 장식용) ======
function setupLangSelect(availableLanguages) {
  const select = document.getElementById("lang-select");
  select.innerHTML = "";

  for (const lang of availableLanguages) {
    const opt = document.createElement("option");
    opt.value = lang;
    opt.textContent =
      lang === "c"
        ? "C"
        : lang === "python"
        ? "Python"
        : lang === "java"
        ? "Java"
        : lang;
    select.appendChild(opt);
  }

  currentLang = availableLanguages[0] || "c";
  select.value = currentLang;

  const single = document.getElementById("lang-single");

  if (availableLanguages.length <= 1) {
    select.hidden = true;
    if (single) {
      single.hidden = false;
      single.textContent = select.options[0]?.textContent || currentLang;
    }
  } else {
    select.hidden = false;
    if (single) single.hidden = true;
  }

  select.addEventListener("change", (e) => {
    currentLang = e.target.value;
    // 나중에 언어별 코드가 생기면 여기서 다시 렌더링
    renderSet();
  });
}

// ====== 유틸: 정규화 함수 (기존 코드 그대로) ======
function normalizeCode(str) {
  return (str || "")
    .replace(/\r\n/g, "\n") // 개행 통일
    .replace(/\/\/.*$/gm, "") // // 주석 제거
    .replace(/\/\*[\s\S]*?\*\//g, "") // /* */ 주석 제거
    .replace(/\s+/g, " ") // 여러 공백 → 하나
    .replace(/\s*([();,=<>+*\/%-&|!])\s*/g, "$1") // 연산자 주변 공백
    .trim();
}

// ====== Code/Output 혼동 방지(휴리스틱) ======
function looksLikeProgramText(text) {
  const t = (text || "").trim();
  if (!t) return false;

  // 대표 키워드/호출(언어 공통-ish)
  if (
    /\b(print|printf|scanf|System\.out|def|return|import|class|if|elif|else|for|while)\b/.test(
      t
    )
  )
    return true;
  if (/#include\b/.test(t)) return true;

  // 코드에서 자주 나오는 기호들
  if (/[;{}]/.test(t)) return true;
  if (/\b(print|printf|scanf)\s*\(/.test(t)) return true;

  return false;
}

function expectedLooksLikeStatement(q) {
  // “이 Code 문제의 정답이 print/printf/scanf 같은 ‘문장’인지”만 판별 (조건식-only는 제외)
  let candidates = [];
  if (Array.isArray(q.expectedCode))
    candidates = candidates.concat(q.expectedCode);
  else if (typeof q.expectedCode === "string") candidates.push(q.expectedCode);
  if (Array.isArray(q.expectedCodes))
    candidates = candidates.concat(q.expectedCodes);

  const joined = candidates.filter(Boolean).join("\n");
  return /\b(print|printf|scanf|System\.out|#include)\b/.test(joined);
}

function getFormatWarning(q, text) {
  const t = String(text ?? "").trim();
  if (!t) return "";

  if (q.type === "short") {
    // Short는 “출력 결과” 칸 → 코드처럼 보이면 경고
    if (looksLikeProgramText(t))
      return "⚠️ 이 칸은 출력 결과를 쓰는 곳이에요. 코드(print/if/...)를 적은 것 같아요.";
    return "";
  }

  if (q.type === "code") {
    // Code는 “코드” 칸 → (문장형 코드가 기대되는 문제에서) 결과처럼 보이면 경고
    if (!expectedLooksLikeStatement(q)) return ""; // 조건식-only 같은 문제는 경고 안 함
    if (!looksLikeProgramText(t) && !/[()]/.test(t)) {
      return "⚠️ 이 칸은 코드를 쓰는 곳이에요. 출력 결과만 적은 것 같아요. (예: print(...) 형태)";
    }
    return "";
  }

  return "";
}

function setInlineWarning(qid, msg) {
  const wrap = document.querySelector(`[data-answer-wrap="${qid}"]`);
  const warn = document.querySelector(`[data-warning="${qid}"]`);
  if (wrap) wrap.classList.toggle("has-warning", !!msg);
  if (warn) warn.textContent = msg || "";
}

function normalizeText(str) {
  return (str || "").replace(/\s+/g, " ").trim().toLowerCase();
}

// ====== 문제 전체 렌더 ======
function renderSet() {
  const container = document.getElementById("problem-container");
  destroyCodeMirrorEditors();

  container.innerHTML = "";

  const questions = currentSetData.problems || [];
  const coreCount = Number(currentSetData.coreCount ?? 6);

  let coreWrap = container;
  let suppWrap = null;

  if (isClassMode()) {
    if (activeBucket !== "core" && activeBucket !== "supp")
      activeBucket = "core";

    // 탭
    const tabs = document.createElement("div");
    tabs.className = "set-tabs";
    tabs.innerHTML = `
  <button type="button" class="tab ${
    activeBucket === "core" ? "active" : ""
  }" data-tab="core">핵심</button>
  <button type="button" class="tab ${
    activeBucket === "supp" ? "active" : ""
  }" data-tab="supp">보강/숙제</button>
  <span class="tab-note">기본 ${Math.min(
    coreCount,
    questions.length
  )}문항 노출</span>
`;

    container.appendChild(tabs);

    coreWrap = document.createElement("div");
    coreWrap.id = "core-wrap";
    suppWrap = document.createElement("div");
    suppWrap.id = "supp-wrap";
    suppWrap.hidden = activeBucket !== "supp";
    coreWrap.hidden = activeBucket !== "core";

    container.appendChild(coreWrap);
    container.appendChild(suppWrap);

    tabs.addEventListener("click", (e) => {
      const btn = e.target?.closest?.("[data-tab]");
      if (!btn) return;
      activeBucket = btn.dataset.tab;

      tabs
        .querySelectorAll(".tab")
        .forEach((b) => b.classList.toggle("active", b === btn));

      coreWrap.hidden = activeBucket !== "core";
      suppWrap.hidden = activeBucket !== "supp";

      // ✅ 추가: 탭 전환 후 HUD 재생성
      if (window.refreshHudIndexPanel) window.refreshHudIndexPanel();
      updateProgressUi();
    });
  }

  // if (window.refreshHudIndexPanel) window.refreshHudIndexPanel();

  questions.forEach((q, idx) => {
    const card = document.createElement("section");
    card.className = "question-card";

    card.dataset.qid = q.id;

    // 버킷(core/supp) 결정: q.bucket 우선, 없으면 앞 6개를 core
    const bucket =
      q.bucket === "supp" || q.bucket === "core"
        ? q.bucket
        : idx < coreCount
        ? "core"
        : "supp";
    card.dataset.bucket = bucket;

    // --- 헤더 (문제 번호 + 제목 + 타입 태그) ---
    const header = document.createElement("div");
    header.className = "question-header";

    const title = document.createElement("h2");
    title.textContent = `${idx + 1}. ${q.title}`;
    header.appendChild(title);

    const typeTag = document.createElement("span");
    typeTag.className = "q-type-tag";
    if (q.type === "mcq") typeTag.textContent = "객관식";
    else if (q.type === "short") typeTag.textContent = "단답형";
    else if (q.type === "code") typeTag.textContent = "코드 작성";
    header.appendChild(typeTag);
    appendQGradeBadge(header, q.id);

    card.appendChild(header);

    // --- 설명 ---
    const desc = document.createElement("div");
    desc.className = "description md";
    renderMarkdownInto(desc, q.description || "");
    card.appendChild(desc);

    // --- 코드 블록 (있으면) ---
    if (q.code) {
      const pre = document.createElement("pre");
      pre.className = "code-block line-numbers";

      const codeEl = document.createElement("code");
      // 현재 선택된 언어 기준으로 Prism 클래스 부여
      codeEl.className = `language-${currentLang}`;
      codeEl.textContent = q.code;

      pre.appendChild(codeEl);
      card.appendChild(pre);
    }

    // --- 유형별 입력/보기 생성 ---
    if (q.type === "mcq") {
      renderMcqOptions(card, q);
    } else {
      renderTextArea(card, q);
    }

    appendCoachPanel(card, q, idx, bucket);

    // --- 피드백 영역 ---
    const feedback = document.createElement("div");
    feedback.className = "feedback";
    feedback.setAttribute("data-feedback", q.id);
    card.appendChild(feedback);

    if (isClassMode() && suppWrap) {
      (bucket === "core" ? coreWrap : suppWrap).appendChild(card);
    } else {
      container.appendChild(card);
    }
  });

  // ▼ 렌더가 다 끝난 뒤에 하이라이트 호출 ▼
  if (window.Prism) {
    Prism.highlightAllUnder(container);
    upgradeCodeInputsToCodeMirror(container);
  }

  if (window.refreshHudIndexPanel) window.refreshHudIndexPanel();

  updateProgressUi();
}

function getHints(q) {
  if (Array.isArray(q.hints) && q.hints.length) return q.hints.filter(Boolean);
  if (q.hint) return [q.hint];
  return [];
}

function formatMs(ms) {
  const sec = Math.max(0, Math.floor(ms / 1000));
  const m = String(Math.floor(sec / 60)).padStart(2, "0");
  const s = String(sec % 60).padStart(2, "0");
  return `${m}:${s}`;
}

function getSetRecommendedMs() {
  const m = Number(currentSetData?.recommendedMinutes ?? 15);
  return m * 60 * 1000;
}

function getQuestionRecommendedMs(q, idx) {
  if (q && Number.isFinite(Number(q.recommendedSec))) {
    return Number(q.recommendedSec) * 1000;
  }
  // 기본: 세트 권장시간 / coreCount
  const coreCount = Number(currentSetData?.coreCount ?? 6);
  const per = Math.floor(
    getSetRecommendedMs() /
      Math.max(1, Math.min(coreCount, (currentSetData?.problems || []).length))
  );
  return Math.max(90_000, per); // 최소 1분30초
}

function appendCoachPanel(card, q, idx, bucket) {
  // 일반모드: 기존처럼 hint(있으면)만 노출
  if (!isClassMode()) {
    if (q.hint) {
      const hint = document.createElement("div");
      hint.className = "hint";
      hint.classList.add("md");
      renderMarkdownInto(hint, q.hint);
      card.appendChild(hint);
    }
    return;
  }

  const panel = document.createElement("div");
  panel.className = "coach-panel";
  panel.setAttribute("data-coach", q.id);

  const status = document.createElement("div");
  status.className = "coach-status";
  status.setAttribute("data-coach-status", q.id);
  panel.appendChild(status);

  const hints = getHints(q);

  const h1 = document.createElement("div");
  h1.className = "coach-block hint";
  h1.setAttribute("data-coach-hint", "1");
  h1.hidden = true;
  h1.textContent = hints[0] ? `힌트1) ${hints[0]}` : "";
  panel.appendChild(h1);

  const h2 = document.createElement("div");
  h2.className = "coach-block hint";
  h2.setAttribute("data-coach-hint", "2");
  h2.hidden = true;
  h2.textContent = hints[1] ? `힌트2) ${hints[1]}` : "";
  panel.appendChild(h2);

  const explainBtn = document.createElement("button");
  explainBtn.type = "button";
  explainBtn.className = "coach-explain-btn";
  explainBtn.setAttribute("data-coach-explain-btn", q.id);
  explainBtn.hidden = true;
  explainBtn.textContent = "해설 보기";
  panel.appendChild(explainBtn);

  const explain = document.createElement("div");
  explain.className = "coach-block";
  explain.setAttribute("data-coach-explain", q.id);
  explain.hidden = true;
  explain.classList.add("md");
  renderMarkdownInto(explain, q.explanation || "");

  panel.appendChild(explain);

  const nudge = document.createElement("div");
  nudge.className = "coach-nudge";
  nudge.setAttribute("data-coach-nudge", q.id);
  nudge.hidden = true;
  nudge.textContent =
    "권장시간을 넘겼어요. 힌트를 보고도 어렵다면 다음 문제로 넘어가세요.";
  panel.appendChild(nudge);

  explainBtn.addEventListener("click", () => {
    const row = ensureCoachRow(q.id);
    row.explainOpen = !row.explainOpen;
    explain.hidden = !row.explainOpen;
    scheduleSaveCoachState();
  });

  // '읽기/클릭'만으로도 문항 시작 처리(타이핑 전에 얼어붙는 케이스 완화)
  card.addEventListener(
    "pointerdown",
    () => {
      if (typeof getSolveElapsedNow !== "function") return;
      const row = ensureCoachRow(q.id);
      if (row.touchedAt == null) {
        row.touchedAt = getSolveElapsedNow();
        scheduleSaveCoachState();
      }
    },
    { once: true }
  );

  card.appendChild(panel);

  // 최초 UI 반영
  renderCoachUiForQuestion(q, idx);
}

function renderCoachUiForQuestion(q, idx) {
  if (!isClassMode()) return;

  const row = ensureCoachRow(q.id);
  const recMs = getQuestionRecommendedMs(q, idx);
  const now =
    typeof getSolveElapsedNow === "function" ? getSolveElapsedNow() : 0;
  const spent = row.touchedAt == null ? 0 : Math.max(0, now - row.touchedAt);

  const statusEl = document.querySelector(`[data-coach-status="${q.id}"]`);
  if (statusEl) {
    const over = row.touchedAt != null && spent >= recMs;
    statusEl.innerHTML = `
      <span>권장 ${formatMs(recMs)}</span>
      <span>${
        row.touchedAt == null ? "시작 전" : `진행 ${formatMs(spent)}`
      }</span>
      <span>채점 ${Math.min(row.wrongGrades, 2)}/2</span>
      ${over ? `<span class="over">초과!</span>` : ""}
    `;
  }

  const hints = getHints(q);
  const panel = document.querySelector(`[data-coach="${q.id}"]`);
  if (!panel) return;

  // const h1 = panel.querySelector(`[data-coach-hint="1"]`);
  const h1 = document.querySelector(
    `[data-coach="${q.id}"] [data-coach-hint="1"]`
  );

  const h2 = panel.querySelector(`[data-coach-hint="2"]`);
  const explainBtn = panel.querySelector(`[data-coach-explain-btn="${q.id}"]`);
  const explain = panel.querySelector(`[data-coach-explain="${q.id}"]`);
  const nudge = panel.querySelector(`[data-coach-nudge="${q.id}"]`);

  if (h1 && hints[0]) h1.hidden = !(row.stage >= 1);
  if (h2 && hints[1]) h2.hidden = !(row.stage >= 2);

  const canExplain = !!q.explanation && row.explainUnlocked;
  if (explainBtn) explainBtn.hidden = !canExplain;
  if (explain) explain.hidden = !(canExplain && row.explainOpen);

  const shouldNudge = row.touchedAt != null && spent >= recMs + 4 * 60 * 1000;
  if (nudge) nudge.hidden = !shouldNudge;
}

function startCoachTicker() {
  if (coachTicker) clearInterval(coachTicker);

  // 상단 권장시간 표시
  const rec = document.getElementById("rec-timer");
  if (rec) rec.textContent = `권장 ${formatMs(getSetRecommendedMs())}`;

  coachTicker = setInterval(() => {
    checkClassTimeboxOnce(); // ✅ 수업모드 15분 도달 체크(1회 팝업)
    const questions = currentSetData?.problems || [];
    const coreCount = Number(currentSetData?.coreCount ?? 6);

    for (let i = 0; i < questions.length; i++) {
      const q = questions[i];
      const row = ensureCoachRow(q.id);

      // 맞춘 문항은 코칭 중지
      if (row.solved) {
        renderCoachUiForQuestion(q, i);
        continue;
      }

      // 시작 전이면 패스
      if (row.touchedAt == null || typeof getSolveElapsedNow !== "function") {
        renderCoachUiForQuestion(q, i);
        continue;
      }

      const recMs = getQuestionRecommendedMs(q, i);
      const spent = Math.max(0, getSolveElapsedNow() - row.touchedAt);

      const hints = getHints(q);

      // 권장시간 초과 → 힌트1 자동
      if (hints[0] && spent >= recMs) row.stage = Math.max(row.stage, 1);

      // +2분 → 힌트2 자동
      if (hints[1] && spent >= recMs + 2 * 60 * 1000)
        row.stage = Math.max(row.stage, 2);

      // +4분 → 해설 버튼 활성
      if (q.explanation && spent >= recMs + 4 * 60 * 1000)
        row.explainUnlocked = true;

      renderCoachUiForQuestion(q, i);
    }

    scheduleSaveCoachState();
  }, 1000);
}

function setupClassModeControls() {
  const modeBtn = document.getElementById("mode-toggle-btn");
  const fsBtn = document.getElementById("fullscreen-btn");
  const popBtn = document.getElementById("popout-btn");

  if (modeBtn) {
    // 페이지가 모드를 강제하면(lesson.html/practice.html) 토글을 숨김
    const forced = getForcedModeFromDom();
    if (forced) {
      modeBtn.hidden = true;
      modeBtn.onclick = null;
    } else {
      modeBtn.hidden = false;
      modeBtn.textContent = isClassMode() ? "수업모드 ON" : "수업모드 OFF";
      modeBtn.onclick = () => {
        const next = isClassMode() ? "normal" : "class";

        // ✅ 수업모드 -> 일반모드 전환 시 답안 전체 삭제
        if (isClassMode() && next === "normal") {
          const ok = confirm(
            "수업모드를 끄면 현재 체크한 답안이 모두 지워집니다.\n계속할까요?"
          );
          if (!ok) return;

          clearAllCurrentAnswers();
        }

        localStorage.setItem(MODE_STORAGE_KEY, next);
        location.reload(); // 렌더/이벤트 중복 방지
      };
    }
  }

  if (fsBtn) {
    fsBtn.onclick = async () => {
      try {
        if (!document.fullscreenElement) {
          await document.documentElement.requestFullscreen();
          fsBtn.textContent = "전체화면 종료";
        } else {
          await document.exitFullscreen();
          fsBtn.textContent = "전체화면";
        }
      } catch (_) {}
    };
  }

  if (popBtn) {
    popBtn.onclick = () => {
      window.open(location.href, "_blank", "noopener,noreferrer");
    };
  }

  const rec = document.getElementById("rec-timer");
  if (rec)
    rec.textContent = isClassMode()
      ? `권장 ${formatMs(getSetRecommendedMs())}`
      : "";

  // (선택) lesson.html 전용 배지/정책 UI는 여기서도 최신화
  updateModeHeaderUi();
}

// ====== MCQ 렌더링 ======
function shouldMcqOptionsUseTwoColumns(q) {
  // 2열은 "짧은 보기"에서만:
  // - 단순 1줄 제한은 너무 빡빡하므로, (대략) 5줄 이내까지 허용
  // - 대신 "가장 긴 행" 기준으로 판단: 한 행의 최대 글자 수(n)가 작으면 2열에서도 읽기 편함
  //   (여기서 n은 아래 MAX_ROW_CHARS)
  const opts = Array.isArray(q?.options) ? q.options : [];
  if (opts.length < 4) return false;
  if (opts.length > 6) return false;

  const MAX_ROWS = 5; // ~5줄 이내
  const MAX_ROW_CHARS = 60; // n (필요하면 조절)

  const normalize = (s) =>
    String(s ?? "")
      .replace(/\r\n/g, "\n")
      .trim();

  return opts.every((o) => {
    const t = normalize(o);
    if (!t) return true;

    const physicalLines = t.split("\n");
    let estimatedRows = 0;

    for (const line of physicalLines) {
      // 공백 없는 긴 덩어리(토큰)가 너무 길면 2열에서 깨질 확률↑
      const tokens = line.split(/\s+/).filter(Boolean);
      const maxTokenLen = tokens.reduce((m, tok) => Math.max(m, tok.length), 0);
      if (maxTokenLen > MAX_ROW_CHARS) return false;

      // n글자 기준으로 래핑된다고 가정해 줄 수 추정
      estimatedRows += Math.max(1, Math.ceil(line.length / MAX_ROW_CHARS));
      if (estimatedRows > MAX_ROWS) return false;
    }

    return true;
  });
}

function renderMcqOptions(card, q) {
  const optionsWrap = document.createElement("div");
  optionsWrap.className = "options";

  // (추가) 짧은 보기일 때만 2열
  if (shouldMcqOptionsUseTwoColumns(q)) {
    optionsWrap.classList.add("options--grid2");
  }

  const saved = currentAnswers && currentAnswers[q.id];

  (q.options || []).forEach((opt, i) => {
    const optDiv = document.createElement("div");
    optDiv.className = "option-item";

    const inputId = `${q.id}_opt${i}`;

    const input = document.createElement("input");
    input.type = "radio";
    input.name = q.id;
    input.value = String(i);
    input.id = inputId;
    input.setAttribute("data-question", q.id);

    // 저장된 값이 있으면 체크 복원
    if (saved !== undefined && String(saved) === String(i)) {
      input.checked = true;
    }

    // 선택이 바뀔 때마다 자동 저장
    input.addEventListener("change", () => {
      if (input.checked) {
        recordAnswer(q.id, input.value);
      }
    });

    const label = document.createElement("label");
    label.className = "option-label";
    label.htmlFor = inputId;

    const letter = document.createElement("span");
    letter.className = "option-letter";
    const labels = q.optionLabels || [];
    letter.textContent = (labels[i] || String.fromCharCode(65 + i)) + ".";

    const codePre = document.createElement("pre");
    codePre.className = "option-code";
    const codeEl = document.createElement("code");
    codeEl.className = `language-${currentLang}`;
    codeEl.textContent = opt;
    codePre.appendChild(codeEl);

    label.appendChild(letter);
    label.appendChild(codePre);

    optDiv.appendChild(input);
    optDiv.appendChild(label);
    optionsWrap.appendChild(optDiv);
  });

  card.appendChild(optionsWrap);
}

// ====== 단답형/코드 입력 렌더링 ======
function renderTextArea(card, q) {
  const field = document.createElement("div");
  field.className = "answer-field";
  field.setAttribute("data-answer-wrap", q.id);

  const header = document.createElement("div");
  header.className = "answer-field-header";

  const badge = document.createElement("span");
  badge.className =
    "answer-badge " + (q.type === "code" ? "badge-code" : "badge-output");
  badge.textContent = q.type === "code" ? "CODE" : "OUTPUT";

  const hintMini = document.createElement("span");
  hintMini.style.fontSize = "0.78rem";
  hintMini.style.color = "#6b7280";
  hintMini.textContent = q.type === "code" ? "코드를 작성" : "출력 결과만 작성";

  header.appendChild(badge);
  header.appendChild(hintMini);

  const input = document.createElement("textarea");
  input.className = "answer-input";
  input.setAttribute("data-question", q.id);
  input.setAttribute("data-qtype", q.type);
  input.spellcheck = false;
  input.rows = q.type === "code" ? 2 : 1;

  if (q.type === "short")
    input.placeholder = "출력 결과를 그대로 입력하세요. (공백/줄바꿈 포함)";
  if (q.type === "code")
    input.placeholder = "여기에 코드를 작성하세요. (예: print('%d' % x))";

  // 저장된 답안 복원
  const saved = currentAnswers && currentAnswers[q.id];
  if (typeof saved === "string") input.value = saved;

  const warn = document.createElement("div");
  warn.className = "answer-warning";
  warn.setAttribute("data-warning", q.id);

  // 입력할 때마다 저장 + 경고 갱신
  input.addEventListener("input", () => {
    recordAnswer(q.id, input.value);
    const msg = getFormatWarning(q, input.value);
    setInlineWarning(q.id, msg);
  });

  field.appendChild(header);
  field.appendChild(input);
  field.appendChild(warn);
  card.appendChild(field);

  // 처음 렌더 시에도 경고 갱신(기존 저장 답이 있을 수 있음)
  const initialMsg = getFormatWarning(q, input.value);
  setInlineWarning(q.id, initialMsg);

  // if (q.hint) {
  //   const hint = document.createElement("div");
  //   hint.className = "hint";
  //   hint.textContent = q.hint;
  //   card.appendChild(hint);
  // }
}

// ===== LanguageAdapter (헬퍼 하드코딩 제거) =====
const LanguageAdapter = {
  python: {
    condBlank: {
      left: (kw) => kw, // if / elif
      right: ":",
      placeholder: "조건식만 입력 (예: 1 <= n <= 10)",
    },
  },
  c: {
    condBlank: {
      left: () => "if (",
      right: ")",
      placeholder: "조건식만 입력 (예: n >= 1 && n <= 10)",
    },
  },
  java: {
    condBlank: {
      left: () => "if (",
      right: ")",
      placeholder: "조건식만 입력 (예: n >= 1 && n <= 10)",
    },
  },
};

function getAdapter() {
  return LanguageAdapter[currentLang] || LanguageAdapter.c;
}

function extractIfKeyword(q) {
  const code = (q && q.code) || "";
  const m = /(^|\n)\s*(if|elif)\s*#\s*__COND_BLANK__/m.exec(code);
  return m ? m[2] : null; // "if" | "elif" | null
}

// ====== Python if 조건식 빈칸 입력 UI 렌더링 ======
// function isIfConditionBlankQuestion(q) {
//   if (!q || q.type !== "code") return false;
//   if (typeof q.code !== "string") return false;
//   // "if  # ..." 또는 "elif  # ..." 패턴 감지
//   return /(^|\n)\s*(if|elif)\s*#/m.test(q.code);
// }
function isIfConditionBlankQuestion(q) {
  return !!extractIfKeyword(q);
}

function renderIfConditionBlank(card, q) {
  const row = document.createElement("div");
  row.className = "code-blank-row";

  const left = document.createElement("span");
  left.className = "code-blank-chip";

  const input = document.createElement("input");
  input.type = "text";
  input.className = "answer-input code-blank-input";
  input.setAttribute("data-question", q.id);
  input.setAttribute("data-qtype", q.type);

  const right = document.createElement("span");
  right.className = "code-blank-chip";

  const kw = extractIfKeyword(q) || "if";
  const adapter = getAdapter();

  left.textContent = adapter.condBlank.left(kw);
  right.textContent = adapter.condBlank.right;
  input.placeholder = adapter.condBlank.placeholder;

  input.value = currentAnswers[q.id] || "";
  input.addEventListener("input", (e) => recordAnswer(q.id, e.target.value));

  row.appendChild(left);
  row.appendChild(input);
  row.appendChild(right);
  card.appendChild(row);
}

// ====== 채점 버튼 로직 ======
function setupGrading() {
  const gradeButton = document.getElementById("grade-btn");
  const scoreEl = document.getElementById("score");
  const metaEl = document.getElementById("grade-meta");

  if (!gradeButton) return;

  let meta = loadGradeMeta(currentSetId);
  let ticker = null;

  const remainingMs = () => {
    if (!isClassMode()) return 0; // ✅ 수업모드에서만 쿨다운 적용
    const last = meta.lastGradeAt || 0;
    const elapsed = Date.now() - last;
    return Math.max(0, GRADE_COOLDOWN_MS - elapsed);
  };

  const updateUi = () => {
    // 날짜 바뀌면 자동 리셋
    const today = getTodayYmd();
    if (meta.date !== today) {
      meta = { date: today, attempts: 0, lastGradeAt: 0 };
      saveGradeMeta(currentSetId, meta);
    }

    const rem = remainingMs();
    const sec = Math.ceil(rem / 1000);
    const solveText =
      typeof getSolveElapsedNow === "function" &&
      typeof formatElapsed === "function"
        ? formatElapsed(getSolveElapsedNow())
        : document.getElementById("solve-timer")?.textContent || "";

    if (rem > 0) {
      gradeButton.disabled = true;
      gradeButton.textContent = `채점 대기 ${sec}초 (오늘 ${meta.attempts}회)`;
      if (metaEl)
        metaEl.textContent = `오늘 채점 ${meta.attempts}회 · 풀이 ${solveText} · 다음 채점까지 ${sec}초`;
    } else {
      gradeButton.disabled = false;
      gradeButton.textContent = `채점하기 (오늘 ${meta.attempts}회)`;
      if (metaEl)
        metaEl.textContent = `오늘 채점 ${meta.attempts}회 · 풀이 ${solveText}`;
    }
  };

  const startTickerIfNeeded = () => {
    const rem = remainingMs();
    if (rem <= 0) {
      if (ticker) {
        clearInterval(ticker);
        ticker = null;
      }
      updateUi();
      return;
    }

    if (ticker) return;
    updateUi();

    ticker = setInterval(() => {
      const left = remainingMs();
      if (left <= 0) {
        clearInterval(ticker);
        ticker = null;
      }
      updateUi();
    }, 250);
  };

  // 초기 상태 반영
  updateUi();
  startTickerIfNeeded();

  gradeButton.addEventListener("click", () => {
    meta = loadGradeMeta(currentSetId);
    qGradeMeta = loadQGradeMeta(currentSetId);

    if (remainingMs() > 0) {
      startTickerIfNeeded();
      return;
    }

    // ✅ 제출 전 소프트 가드: Code/Output 혼동 의심 답안 있으면 확인
    const qs = currentSetData.problems || [];
    let suspicious = 0;

    qs.forEach((q) => {
      if (q.type !== "short" && q.type !== "code") return;
      const ans = String((currentAnswers && currentAnswers[q.id]) ?? "");
      const msg = getFormatWarning(q, ans); // ← 미리 추가해둔 헬퍼 함수 필요
      setInlineWarning(q.id, msg); // ← 경고 UI 갱신(없으면 지워도 됨)
      if (msg) suspicious++;
    });

    if (suspicious > 0) {
      const ok = confirm(
        `⚠️ ${suspicious}개 답안이 형식이 어색해요(코드/결과 혼동 가능).\n그래도 채점할까요?`
      );
      if (!ok) return;
    }

    const all = currentSetData.problems || [];
    const coreCount = Number(currentSetData.coreCount ?? 6);

    const questions = !isClassMode()
      ? all
      : all.filter((q, idx) => {
          const bucket =
            q.bucket === "supp" || q.bucket === "core"
              ? q.bucket
              : idx < coreCount
              ? "core"
              : "supp";
          return bucket === activeBucket;
        });
    let correctCount = 0;
    // bumpQGradeAttempt(q.id, isCorrect);

    questions.forEach((q) => {
      const feedbackEl = document.querySelector(`[data-feedback="${q.id}"]`);
      let isCorrect = false;

      if (q.type === "mcq") {
        const selected = currentAnswers[q.id];
        isCorrect = String(selected) === String(q.correctIndex);
      } else if (q.type === "short") {
        // const inputEl = document.querySelector(`[data-question="${q.id}"]`);
        // const val = (inputEl && inputEl.value) || "";
        const val = String((currentAnswers && currentAnswers[q.id]) ?? "");

        if (q.expectedAnyOf) {
          const norm = normalizeText(val);
          isCorrect = q.expectedAnyOf.some(
            (ans) => normalizeText(ans) === norm
          );
        } else if (q.expectedText) {
          isCorrect = normalizeText(val) === normalizeText(q.expectedText);
        }
      } else if (q.type === "code") {
        // const inputEl = document.querySelector(`[data-question="${q.id}"]`);
        // const userCode = (inputEl && inputEl.value) || "";
        const userCode = String((currentAnswers && currentAnswers[q.id]) ?? "");

        const normUser = normalizeCode(userCode);

        let candidates = [];
        if (Array.isArray(q.expectedCode)) candidates = q.expectedCode;
        else if (typeof q.expectedCode === "string")
          candidates = [q.expectedCode];
        if (Array.isArray(q.expectedCodes))
          candidates = candidates.concat(q.expectedCodes);

        isCorrect = candidates
          .filter(Boolean)
          .some((code) => normalizeCode(code) === normUser);
      }
      bumpQGradeAttempt(q.id, isCorrect);
      if (isClassMode()) {
        const idx = (currentSetData.problems || []).findIndex(
          (x) => x.id === q.id
        );
        const row = ensureCoachRow(q.id);

        row.solved = !!isCorrect; // ✅ 현재 정답 여부로 유지
        if (!isCorrect) {
          row.wrongGrades = Math.min(2, (row.wrongGrades || 0) + 1);

          // 2회 실패 → 해설 버튼 즉시 해금
          if (row.wrongGrades >= 2) row.explainUnlocked = true;

          // 실패 시에도 힌트는 최소 1단계는 열어주는 운영(선택)
          const hints = getHints(q);
          if (hints[0]) row.stage = Math.max(row.stage, 1);
        }

        renderCoachUiForQuestion(q, idx);
        scheduleSaveCoachState();
      }

      if (feedbackEl) {
        if (isCorrect) {
          correctCount++;
          feedbackEl.textContent = "✅ 정답입니다!";
          feedbackEl.classList.remove("incorrect");
          feedbackEl.classList.add("correct");
        } else {
          feedbackEl.textContent = "❌ 다시 한 번 생각해보세요.";
          feedbackEl.classList.remove("correct");
          feedbackEl.classList.add("incorrect");
        }
      }
    });
    saveQGradeMeta(currentSetId, qGradeMeta);
    refreshAllQGradeBadges();
    updateProgressUi();

    if (scoreEl) {
      const label = isClassMode()
        ? activeBucket === "core"
          ? "핵심"
          : "보강/숙제"
        : "전체";
      scoreEl.textContent = `${label} ${questions.length}문제 중 ${correctCount}문제 정답`;
    }

    // ✅ 채점 메타 갱신 (횟수 + 쿨다운 시작)
    meta.attempts += 1;
    meta.date = getTodayYmd();
    if (isClassMode()) meta.lastGradeAt = Date.now(); // ✅ 수업모드에서만 쿨다운 시작
    saveGradeMeta(currentSetId, meta);

    updateUi();
    startTickerIfNeeded();
  });
}

// ====== HUD: 목차(목록/위치) + 위/아래 ======
function setupHud() {
  const btnIndex = document.getElementById("btn-index");
  const btnTop = document.getElementById("btn-top");
  const btnBottom = document.getElementById("btn-bottom");
  const panel = document.getElementById("hud-index-panel");

  // HUD 요소가 없으면 아무 것도 하지 않음
  if (!btnIndex || !btnTop || !btnBottom || !panel) return;

  // const getCards = () =>
  //   Array.from(document.querySelectorAll(".question-card")).filter(
  //     (card) => card.offsetParent !== null
  //   ); // hidden(보강 탭) 제외

  // const scrollToCard = (index) => {
  //   const cards = getCards();
  //   if (!cards.length) return;
  //   if (index < 0) index = 0;
  //   if (index >= cards.length) index = cards.length - 1;

  //   cards[index].scrollIntoView({
  //     behavior: "smooth",
  //     block: "start",
  //   });
  // };

  // // --- 문제 목록 패널 구성 ---
  // panel.innerHTML = "";
  // const cards = getCards();

  // cards.forEach((card, idx) => {
  //   const titleEl = card.querySelector("h2");
  //   const text = titleEl ? titleEl.textContent : `문제 ${idx + 1}`;

  //   const itemBtn = document.createElement("button");
  //   itemBtn.type = "button";
  //   itemBtn.className = "hud-index-item";
  //   itemBtn.textContent = text;

  //   itemBtn.addEventListener("click", () => {
  //     scrollToCard(idx);
  //     panel.classList.remove("open");
  //   });

  //   panel.appendChild(itemBtn);
  // });

  const getCards = () =>
    Array.from(document.querySelectorAll(".question-card")).filter(
      (card) => card.offsetParent !== null
    );

  const buildIndexPanel = () => {
    panel.innerHTML = "";
    const cards = getCards();

    cards.forEach((card, idx) => {
      const titleEl = card.querySelector("h2");
      const text = titleEl ? titleEl.textContent : `문제 ${idx + 1}`;

      const itemBtn = document.createElement("button");
      itemBtn.type = "button";
      itemBtn.className = "hud-index-item";
      itemBtn.textContent = text;

      itemBtn.addEventListener("click", () => {
        const liveCards = getCards();
        liveCards[idx]?.scrollIntoView({ behavior: "smooth", block: "start" });
        panel.classList.remove("open");
      });

      panel.appendChild(itemBtn);
    });
  };

  // 최초 빌드
  buildIndexPanel();

  // 전역 갱신 함수로 노출 (재렌더 후에도 호출 가능)
  window.refreshHudIndexPanel = buildIndexPanel;

  // --- 목차 버튼: 목록 패널 열기/닫기 ---
  btnIndex.addEventListener("click", (e) => {
    e.stopPropagation();
    panel.classList.toggle("open");
  });

  // HUD 밖을 클릭하면 패널 닫기
  document.addEventListener("click", (e) => {
    if (!panel.classList.contains("open")) return;
    const hud = document.querySelector(".nav-hud");
    if (hud && !hud.contains(e.target)) {
      panel.classList.remove("open");
    }
  });

  // --- 위로 / 아래로 이동 (페이지 최상단 / 최하단) ---
  btnTop.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  btnBottom.addEventListener("click", () => {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });
  });
}

// ====== (추가) 실시간 교사용 대시보드 업로드 (WebSocket) ======
const DASH_STUDENT_KEY = "stepcode:dashStudentId";
const DASH_NAME_KEY = "stepcode:dashDisplayName";
const DASH_ROOM_KEY = "stepcode:dashRoomId";

const DASH_SEND_EVERY_MS = 10000; // 10초마다 상태 업로드
const DASH_ACTIVITY_THROTTLE_MS = 3000; // 마우스/키보드 활동은 3초에 1번만 반영

let dashWs = null;
let dashSendTimer = null;
let dashReconnectTimer = null;

let dashRoomId = "default";
let dashStudentId = null;
let dashDisplayName = null;

let dashLastActivityAt = 0;
let dashLastActivityTouchAt = 0;

function dashQP(name) {
  try {
    const p = new URLSearchParams(location.search);
    return (p.get(name) || "").trim();
  } catch (_) {
    return "";
  }
}

function dashGetRoomId() {
  const fromQ = dashQP("room");
  if (fromQ) {
    try {
      localStorage.setItem(DASH_ROOM_KEY, fromQ);
    } catch (_) {}
    return fromQ;
  }
  try {
    const saved = (localStorage.getItem(DASH_ROOM_KEY) || "").trim();
    return saved || "default";
  } catch (_) {
    return "default";
  }
}

function dashGetStudentIdAndName() {
  const sidQ = dashQP("student");
  const nameQ = dashQP("name");

  if (sidQ) {
    try {
      localStorage.setItem(DASH_STUDENT_KEY, sidQ);
    } catch (_) {}
    dashStudentId = sidQ;
  } else {
    try {
      dashStudentId = (localStorage.getItem(DASH_STUDENT_KEY) || "").trim();
    } catch (_) {}
  }

  if (nameQ) {
    try {
      localStorage.setItem(DASH_NAME_KEY, nameQ);
    } catch (_) {}
    dashDisplayName = nameQ;
  } else {
    try {
      dashDisplayName = (localStorage.getItem(DASH_NAME_KEY) || "").trim();
    } catch (_) {}
  }

  // 링크에 student가 없으면 1회만 물어보기(원치 않으면 이 블록 삭제해도 됨)
  if (!dashStudentId) {
    const v = prompt(
      "대시보드용 학생 식별값(좌석/닉네임)을 입력하세요.\n(예: 1번, A-03, 민수)"
    );
    if (v && v.trim()) {
      dashStudentId = v.trim();
      dashDisplayName = dashDisplayName || dashStudentId;
      try {
        localStorage.setItem(DASH_STUDENT_KEY, dashStudentId);
      } catch (_) {}
      try {
        localStorage.setItem(DASH_NAME_KEY, dashDisplayName);
      } catch (_) {}
    }
  }

  if (!dashDisplayName) dashDisplayName = dashStudentId || "unknown";
}

function dashWsUrl() {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  return `${proto}://${location.host}/ws`;
}

function dashComputeProgress() {
  const probs =
    currentSetData && currentSetData.problems ? currentSetData.problems : [];
  const total = probs.length;

  // answered: 답안이 비어있지 않으면 풀이로 간주
  let answered = 0;
  for (const q of probs) {
    const v = currentAnswers ? currentAnswers[q.id] : "";
    if (v != null && String(v).trim() !== "") answered++;
  }

  // correct: 마지막 채점 결과(lastIsCorrect)가 true인 문항 수
  let correct = 0;
  try {
    const byQ = qGradeMeta && qGradeMeta.byQ ? qGradeMeta.byQ : {};
    for (const q of probs) {
      if (byQ[q.id] && byQ[q.id].lastIsCorrect === true) correct++;
    }
  } catch (_) {}

  return { answered, correct, total };
}

function dashComputeTopTries(limit = 3) {
  const probs =
    currentSetData && currentSetData.problems ? currentSetData.problems : [];
  const byQ = qGradeMeta && qGradeMeta.byQ ? qGradeMeta.byQ : {};
  const rows = [];

  for (const q of probs) {
    const m = byQ[q.id];
    if (!m) continue;
    const attempts = Number(m.attempts) || 0;
    if (attempts <= 0) continue;
    rows.push({ qid: q.id, attempts, lastIsCorrect: m.lastIsCorrect });
  }

  rows.sort((a, b) => b.attempts - a.attempts);
  return rows.slice(0, limit);
}

function dashBuildPayload() {
  const setTitle =
    currentSetData && currentSetData.title ? currentSetData.title : "";
  const mode =
    typeof isClassMode === "function" && isClassMode() ? "class" : "practice";
  const bucket =
    mode === "class" && typeof activeBucket === "string" ? activeBucket : "";

  let solveElapsedMs = 0;
  try {
    if (typeof getSolveElapsedNow === "function")
      solveElapsedMs = Number(getSolveElapsedNow()) || 0;
  } catch (_) {}

  let gradeAttemptsToday = 0;
  try {
    if (typeof loadGradeMeta === "function" && currentSetId) {
      gradeAttemptsToday = Number(loadGradeMeta(currentSetId).attempts) || 0;
    }
  } catch (_) {}

  return {
    room: dashRoomId,
    studentId: dashStudentId || "unknown",
    displayName: dashDisplayName || dashStudentId || "unknown",
    setId: currentSetId || "",
    setTitle,
    mode,
    bucket,
    progress: dashComputeProgress(),
    topTries: dashComputeTopTries(3),
    solveElapsedMs,
    gradeAttemptsToday,
    lastActivityAt: dashLastActivityAt || Date.now(),
    helpActive: dashHelpActive,
    helpRequestedAt: dashHelpRequestedAt,
    helpQid: dashHelpQid,
  };
}

function dashSendStatus() {
  if (!dashWs || dashWs.readyState !== WebSocket.OPEN) return;
  if (!dashStudentId) return;

  const payload = dashBuildPayload();
  dashWs.send(JSON.stringify({ type: "status", room: dashRoomId, payload }));
}

function dashMarkActivity(throttled = true) {
  const now = Date.now();
  dashLastActivityAt = now;

  if (!throttled) return;

  if (now - dashLastActivityTouchAt < DASH_ACTIVITY_THROTTLE_MS) return;
  dashLastActivityTouchAt = now;
}

function dashConnectWS() {
  if (!dashStudentId) return;

  if (dashWs) {
    try {
      dashWs.close();
    } catch (_) {}
    dashWs = null;
  }
  if (dashReconnectTimer) {
    clearTimeout(dashReconnectTimer);
    dashReconnectTimer = null;
  }
  dashUISetState("connecting");
  dashUIUpdateAll();

  dashWs = new WebSocket(dashWsUrl());

  dashWs.addEventListener("open", () => {
    dashUISetState("connected");
    dashUIUpdateAll();

    dashWs.send(
      JSON.stringify({
        type: "hello",
        role: "student",
        room: dashRoomId,
        studentId: dashStudentId,
        displayName: dashDisplayName,
      })
    );
    dashSendStatus();
  });

  dashWs.addEventListener("close", () => {
    dashUISetState("disconnected");
    dashUIUpdateAll();

    // 3초 후 재연결
    dashReconnectTimer = setTimeout(dashConnectWS, 3000);
  });

  dashWs.addEventListener("error", () => {
    // close 이벤트로 이어지므로 여기서는 별도 처리 없음
  });
}

function setupRealtimeDashboard() {
  // set 로딩 이후에만 의미가 있으므로 initPractice 끝에서 호출
  dashRoomId = dashGetRoomId();
  dashGetStudentIdAndName();
  dashLoadHelpState();

  dashEnsureControlWidget();
  dashUIUpdateAll();

  if (!dashStudentId) return; // 입력을 취소한 경우

  // 활동 감지(기존 recordAnswer/grade 로직을 안 건드리고도 연결 가능)
  document.addEventListener(
    "input",
    (e) => {
      const t = e.target;
      if (!t) return;
      // 답안 입력류만(불필요한 이벤트 폭발 방지)
      if (t.classList && t.classList.contains("answer-input")) {
        const qid = t.getAttribute?.("data-question") || "";
        if (qid) dashFocusQid = qid;

        dashMarkActivity(false);
        dashSendStatus();
      }
    },
    true
  );

  document.addEventListener(
    "click",
    (e) => {
      const t = e.target;
      if (!t) return;
      if (t.id === "grade-btn") {
        dashMarkActivity(false);
        dashSendStatus();
      }
    },
    true
  );

  document.addEventListener("keydown", () => dashMarkActivity(true), true);
  document.addEventListener("mousemove", () => dashMarkActivity(true), true);

  dashConnectWS();

  if (dashSendTimer) clearInterval(dashSendTimer);
  dashSendTimer = setInterval(() => {
    dashMarkActivity(true);
    dashSendStatus();
  }, DASH_SEND_EVERY_MS);
}

// ====== (추가) 도움 요청(손들기) 상태 ======
let dashHelpActive = false;
let dashHelpRequestedAt = 0;
let dashHelpQid = "";
let dashFocusQid = ""; // 마지막으로 입력/포커스한 문항 id

// 도움 요청 쿨타임(요청 ON에만 적용)
const DASH_HELP_COOLDOWN_MS = 20000; // 20초 (원하면 30000 등으로 변경)
let dashHelpCooldownUntil = 0;
let dashHelpCooldownTimer = null;

function dashHelpRemainingMs() {
  return Math.max(0, (dashHelpCooldownUntil || 0) - Date.now());
}

function dashHelpStartCooldownTicker() {
  if (dashHelpCooldownTimer) return;
  dashHelpCooldownTimer = setInterval(() => {
    // 필요할 때만 갱신
    if (dashHelpRemainingMs() > 0) dashUIUpdateHelpButton();
    else {
      dashUIUpdateHelpButton();
      clearInterval(dashHelpCooldownTimer);
      dashHelpCooldownTimer = null;
    }
  }, 250);
}

function dashHelpKey() {
  // room + studentId 기준으로 저장(PC 공유/재접속에도 유지)
  return `stepcode:dashHelp:${dashRoomId || "default"}:${
    dashStudentId || "unknown"
  }`;
}

function dashLoadHelpState() {
  dashHelpActive = false;
  dashHelpRequestedAt = 0;
  dashHelpQid = "";
  dashHelpCooldownUntil = 0;

  try {
    const raw = localStorage.getItem(dashHelpKey());
    if (!raw) return;

    const obj = JSON.parse(raw);
    dashHelpActive = !!obj.active;
    dashHelpRequestedAt = Number(obj.at || 0) || 0;
    dashHelpQid = String(obj.qid || "");

    // ✅ cooldown은 obj 파싱 이후에 읽어야 함
    dashHelpCooldownUntil = Number(obj.cooldownUntil || 0) || 0;
    if (dashHelpRemainingMs() > 0) dashHelpStartCooldownTicker();
  } catch (_) {}
}

function dashSaveHelpState() {
  try {
    localStorage.setItem(
      dashHelpKey(),
      JSON.stringify({
        active: dashHelpActive,
        at: dashHelpRequestedAt,
        qid: dashHelpQid,
        cooldownUntil: dashHelpCooldownUntil,
      })
    );
  } catch (_) {}
}

function dashSetHelpActive(on) {
  // ON(도움 요청)만 쿨타임 적용, OFF(취소)는 즉시 허용
  if (on && !dashHelpActive) {
    const remain = dashHelpRemainingMs();
    if (remain > 0) {
      // 쿨타임 중이면 UI만 갱신하고 종료
      dashHelpStartCooldownTicker();
      dashUIUpdateHelpButton();
      return;
    }
    // 이번 요청을 성공시키면 즉시 쿨타임 시작
    dashHelpCooldownUntil = Date.now() + DASH_HELP_COOLDOWN_MS;
    dashHelpStartCooldownTicker();
  }

  dashHelpActive = !!on;
  if (dashHelpActive) {
    dashHelpRequestedAt = Date.now();
    dashHelpQid = dashFocusQid || "";
  } else {
    dashHelpRequestedAt = 0;
    dashHelpQid = "";
  }
  dashSaveHelpState();
  dashUIUpdateHelpButton();
  dashSendStatus();
}

function dashToggleHelp() {
  dashSetHelpActive(!dashHelpActive);
}

// ====== (추가) 학생용 연결 상태 위젯(UI) ======
let dashWidgetEl = null;

function dashEnsureControlWidget() {
  if (dashWidgetEl) return dashWidgetEl;

  const w = document.createElement("div");
  w.id = "dash-widget";
  w.className = "dash-widget";
  w.setAttribute("data-state", "disconnected");
  w.setAttribute("role", "status");
  w.setAttribute("aria-live", "polite");

  w.innerHTML = `
    <div class="dash-top">
      <span class="dash-dot" aria-hidden="true"></span>
      <div class="dash-lines">
        <div class="dash-line1">
          <span>Room: <b id="dash-ui-room" class="dash-kv">-</b></span>
          <span id="dash-ui-state" class="dash-muted">끊김</span>
        </div>
        <div class="dash-muted">
          <span id="dash-ui-name" class="dash-kv">-</span>
          <span id="dash-ui-student" class="dash-kv"></span>
        </div>
      </div>
    </div>

    <div class="dash-actions">
      <button type="button" id="dash-ui-reconnect">재연결</button>
      <button type="button" id="dash-ui-reset" class="dash-danger">입장정보 초기화</button>
    </div>
  `;

  document.body.appendChild(w);
  dashWidgetEl = w;

  // 버튼 이벤트
  w.querySelector("#dash-ui-reconnect")?.addEventListener("click", () => {
    // studentId가 없으면(프롬프트 취소 등) 여기서 다시 물어봄
    if (!dashStudentId) {
      dashGetStudentIdAndName();
      dashUIUpdateAll();
    }
    dashReconnectNow();
  });

  // ====== (추가) 도움 요청 버튼(동적 생성) ======
  const actions = w.querySelector(".dash-actions");
  if (actions && !w.querySelector("#dash-ui-help")) {
    const helpBtn = document.createElement("button");
    helpBtn.type = "button";
    helpBtn.id = "dash-ui-help";
    helpBtn.className = "dash-help";
    helpBtn.textContent = "도움 요청";

    helpBtn.addEventListener("click", () => {
      if (!dashStudentId) {
        dashGetStudentIdAndName();
        dashUIUpdateAll();
        // 식별값이 없으면 도움요청 불가
        if (!dashStudentId) return;
        // studentId가 새로 생겼으니 help state도 그 키 기준으로 로드
        dashLoadHelpState();
      }
      dashToggleHelp();
    });

    // 3번째 버튼으로 추가
    actions.appendChild(helpBtn);
  }

  w.querySelector("#dash-ui-reset")?.addEventListener("click", () => {
    dashResetEntryInfo();
  });

  return w;
}

function dashUISetState(state) {
  const w = dashEnsureControlWidget();
  w.setAttribute("data-state", state);

  const t = w.querySelector("#dash-ui-state");
  if (!t) return;

  if (state === "connected") t.textContent = "연결됨";
  else if (state === "connecting") t.textContent = "연결중";
  else t.textContent = "끊김";
}

function dashUIUpdateAll() {
  const w = dashEnsureControlWidget();
  w.querySelector("#dash-ui-room").textContent = dashRoomId || "default";

  const name = dashDisplayName || "-";
  const sid = dashStudentId ? `(ID:${dashStudentId})` : "(ID:미설정)";
  w.querySelector("#dash-ui-name").textContent = name;
  w.querySelector("#dash-ui-student").textContent = ` ${sid}`;

  dashUIUpdateHelpButton();
}
function dashUIUpdateHelpButton() {
  const w = dashEnsureControlWidget();
  const btn = w.querySelector("#dash-ui-help");
  if (!btn) return;

  // 도움 요청 중이면 취소는 항상 가능
  if (dashHelpActive) {
    btn.disabled = false;
    btn.classList.add("active");
    btn.textContent = "도움 취소";
    btn.title = "";
    return;
  }

  // 요청이 꺼져있으면, 쿨타임 동안 재요청을 막음
  const remainMs = dashHelpRemainingMs();
  if (remainMs > 0) {
    const sec = Math.ceil(remainMs / 1000);
    btn.disabled = true;
    btn.classList.remove("active");
    btn.textContent = `대기 ${sec}s`;
    btn.title = "연타 방지를 위해 잠시 대기합니다.";
    return;
  }

  btn.disabled = false;
  btn.classList.remove("active");
  btn.textContent = "도움 요청";
  btn.title = "";
}

function dashReconnectNow() {
  // room/student/name이 없으면 여기서 끝(학생이 입력 취소한 경우)
  if (!dashStudentId) {
    dashUISetState("disconnected");
    dashUIUpdateAll();
    return;
  }

  dashUISetState("connecting");
  dashUIUpdateAll();
  dashConnectWS();
  // 연결 직후 바로 1회 업로드 시도
  setTimeout(() => dashSendStatus(), 200);
}

function dashResetEntryInfo() {
  const ok = confirm(
    "입장정보(room / student / name)를 초기화할까요?\n" +
      "초기화 후 새로고침되며 다시 입력해야 합니다."
  );
  if (!ok) return;

  try {
    localStorage.removeItem(DASH_ROOM_KEY);
  } catch (_) {}
  try {
    localStorage.removeItem(DASH_STUDENT_KEY);
  } catch (_) {}
  try {
    localStorage.removeItem(DASH_NAME_KEY);
  } catch (_) {}
  try {
    localStorage.removeItem(dashHelpKey());
  } catch (_) {}

  // 런타임 값도 리셋
  dashRoomId = "default";
  dashStudentId = null;
  dashDisplayName = null;

  try {
    if (dashWs) dashWs.close();
  } catch (_) {}
  dashWs = null;
  if (dashHelpCooldownTimer) {
    clearInterval(dashHelpCooldownTimer);
    dashHelpCooldownTimer = null;
  }

  location.reload();
}

// ====== (추가) 수업모드 15분 타임박스 ======
const CLASS_TIMEBOX_PREFIX = "stepcode:classTimebox:";

function getClassTimeboxKey(setId) {
  return `${CLASS_TIMEBOX_PREFIX}${setId}:${getTodayYmd()}`; // 하루 1회
}

function hasShownClassTimebox() {
  if (!currentSetId) return true;
  try {
    return localStorage.getItem(getClassTimeboxKey(currentSetId)) === "1";
  } catch (_) {
    return true;
  }
}

function markShownClassTimebox() {
  if (!currentSetId) return;
  try {
    localStorage.setItem(getClassTimeboxKey(currentSetId), "1");
  } catch (_) {}
}

function showClassTimeboxModal() {
  // 중복 생성 방지
  if (document.getElementById("class-timebox-overlay")) return;

  // 타이머는 결정 시간 때문에 손해 보지 않게 일시정지
  if (typeof pauseSolveTimer === "function") pauseSolveTimer(true);

  const overlay = document.createElement("div");
  overlay.id = "class-timebox-overlay";
  overlay.style.cssText = `
    position: fixed; inset: 0; background: rgba(0,0,0,.45);
    display:flex; align-items:center; justify-content:center;
    z-index: 9999;
  `;

  const box = document.createElement("div");
  box.style.cssText = `
    width: min(520px, calc(100vw - 32px));
    background: #fff; border-radius: 14px; padding: 18px 18px 14px 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,.25);
  `;

  const title = document.createElement("div");
  title.style.cssText = `font-size: 18px; font-weight: 700; margin-bottom: 8px;`;
  title.textContent = "권장 시간이 지났어요";

  const desc = document.createElement("div");
  const rec =
    typeof formatElapsed === "function"
      ? formatElapsed(getSetRecommendedMs())
      : "15:00";
  const spent =
    typeof getSolveElapsedNow === "function" &&
    typeof formatElapsed === "function"
      ? formatElapsed(getSolveElapsedNow())
      : "";
  desc.style.cssText = `color:#374151; line-height:1.5; margin-bottom: 14px;`;
  desc.textContent = `권장 ${rec}에 도달했습니다. (현재 ${spent}) 계속 진행할까요, 아니면 선생님을 호출할까요?`;

  const actions = document.createElement("div");
  actions.style.cssText = `display:flex; gap:10px; justify-content:flex-end;`;

  const btnContinue = document.createElement("button");
  btnContinue.type = "button";
  btnContinue.textContent = "이어서 할게요";
  btnContinue.style.cssText = `
    padding: 10px 12px; border-radius: 10px; border: 1px solid #d1d5db;
    background:#fff; cursor:pointer;
  `;

  const btnHelp = document.createElement("button");
  btnHelp.type = "button";
  btnHelp.textContent = "선생님 호출";
  btnHelp.style.cssText = `
    padding: 10px 12px; border-radius: 10px; border: 0;
    background:#111827; color:#fff; cursor:pointer;
  `;

  function close() {
    overlay.remove();
    // 다시 시작
    if (!document.hidden && typeof startSolveTimer === "function")
      startSolveTimer();
  }

  btnContinue.addEventListener("click", close);

  btnHelp.addEventListener("click", () => {
    // 대시보드 손들기(있으면) 자동 ON
    if (typeof dashSetHelpActive === "function") dashSetHelpActive(true);
    close();
  });

  actions.append(btnContinue, btnHelp);
  box.append(title, desc, actions);
  overlay.append(box);
  document.body.appendChild(overlay);
}

function checkClassTimeboxOnce() {
  if (!isClassMode()) return;
  if (!currentSetId) return;
  if (hasShownClassTimebox()) return;

  const nowMs =
    typeof getSolveElapsedNow === "function" ? getSolveElapsedNow() : 0;
  if (nowMs >= getSetRecommendedMs()) {
    markShownClassTimebox();
    showClassTimeboxModal();
  }
}

function clearAllCurrentAnswers() {
  if (!currentSetId) return;

  // 1) 메모리 + 저장 답안 초기화
  currentAnswers = {};
  saveStoredAnswers(currentSetId, currentAnswers);

  // 2) UI 초기화 (라디오/텍스트/코드)
  const root = document.getElementById("problem-container") || document;

  // MCQ 라디오 해제
  root
    .querySelectorAll('input[type="radio"][data-question]')
    .forEach((el) => (el.checked = false));

  // short/code 입력값 비우기 (CodeMirror용 textarea 포함)
  root.querySelectorAll(".answer-input[data-question]").forEach((el) => {
    el.value = "";
    // 입력 이벤트를 통해 내부 로직이 있다면 같이 반영되도록
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  });

  // CodeMirror 에디터 비우기 (있다면)
  if (typeof CODEMIRROR_EDITORS !== "undefined" && CODEMIRROR_EDITORS?.size) {
    CODEMIRROR_EDITORS.forEach((ed) => {
      try {
        ed.setValue("");
      } catch (_) {}
    });
  }

  updateProgressUi();

  // (선택) "정답 n/n"이 남는 게 싫다면 아래도 같이 초기화 추천
  try {
    localStorage.removeItem(getQGradeMetaKey(currentSetId));
  } catch (_) {}
  try {
    localStorage.removeItem(getGradeMetaKey(currentSetId));
  } catch (_) {}
  saveSolveElapsed(currentSetId, 0); // 타이머도 같이 초기화하고 싶으면
}

// ====== 여기까지 practice.js ======

// ====== (추가) 학습지 출력 (A4 가로 2열 · 한 면 4문항) ======
function setupWorksheetPrint() {
  const btn = document.getElementById("print-worksheet-btn");
  if (!btn) return;

  btn.addEventListener("click", (e) => {
    if (!currentSetId || !currentSetData) {
      alert("세트가 아직 로드되지 않았습니다.");
      return;
    }

    // 기본: 일반모드=전체, 수업모드=현재 탭(core/supp)
    let bucket = "all";
    if (typeof isClassMode === "function" && isClassMode()) {
      bucket =
        typeof activeBucket === "string" && activeBucket
          ? activeBucket
          : "core";
    }

    // Shift: 무조건 전체 문항
    if (e.shiftKey) bucket = "all";

    // Alt(or Cmd): 선생님용(정답 포함) 프린트
    const variant = e.altKey || e.metaKey ? "teacher" : "student";

    const url =
      `print.html?set=${encodeURIComponent(currentSetId)}` +
      `&bucket=${encodeURIComponent(bucket)}` +
      `&variant=${encodeURIComponent(variant)}` +
      `&lang=${encodeURIComponent(currentLang || "")}`;

    window.open(url, "_blank", "noopener,noreferrer");
  });
}
// ====== 답안 채점 ======
