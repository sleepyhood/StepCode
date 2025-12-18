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
    html: false,     // md 안의 raw HTML 금지(보안)
    linkify: true,
    breaks: true
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
let activeBucket = "core"; // "core" | "supp"
let coachState = {}; // { [qid]: { touchedAt, stage, wrongGrades, explainUnlocked, solved, explainOpen } }
let coachTicker = null;
let coachSaveTimer = null;

function isClassMode() {
  return practiceMode === "class";
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
}

// ▲ 여기까지 추가 ▲

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
  const timerEl = document.getElementById("solve-timer");
  const stateEl = document.getElementById("solve-timer-state");
  if (!timerEl) return;

  timerEl.textContent = formatElapsed(getSolveElapsedNow());

  if (wrap) wrap.classList.toggle("paused", !!paused);
  if (stateEl) stateEl.textContent = paused ? "일시정지" : "";
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

  try {
    // 세트 JSON 불러오기
    currentSetData = await ProblemService.loadSet(setId);
    // 세트 정보 + 로컬 저장된 답안 불러오기
    currentSetId = setId;
    currentAnswers = loadStoredAnswers(setId);

    // (추가) 모드 로드 + UI 반영
    practiceMode =
      localStorage.getItem(MODE_STORAGE_KEY) === "class" ? "class" : "normal";
    document.body.classList.toggle("mode-class", isClassMode());

    // (추가) 코칭 상태 로드
    coachState = isClassMode() ? loadCoachState(currentSetId) : {};

    setupSolveTimerForCurrentSet();

    // 제목 표시
    titleSpan.textContent = currentSetData.title || "연습장";

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
    if (activeBucket !== "core" && activeBucket !== "supp") activeBucket = "core";

    // 탭
    const tabs = document.createElement("div");
    tabs.className = "set-tabs";
    tabs.innerHTML = `
  <button type="button" class="tab ${activeBucket === "core" ? "active" : ""}" data-tab="core">핵심</button>
  <button type="button" class="tab ${activeBucket === "supp" ? "active" : ""}" data-tab="supp">보강/숙제</button>
  <span class="tab-note">기본 ${Math.min(coreCount, questions.length)}문항 노출</span>
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

  tabs.querySelectorAll(".tab")
    .forEach((b) => b.classList.toggle("active", b === btn));

  coreWrap.hidden = activeBucket !== "core";
  suppWrap.hidden = activeBucket !== "supp";

  // ✅ 추가: 탭 전환 후 HUD 재생성
  if (window.refreshHudIndexPanel) window.refreshHudIndexPanel();
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
    modeBtn.textContent = isClassMode() ? "수업모드 ON" : "수업모드 OFF";
    modeBtn.onclick = () => {
      const next = isClassMode() ? "normal" : "class";
      localStorage.setItem(MODE_STORAGE_KEY, next);
      location.reload(); // 렌더/이벤트 중복 방지
    };
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
}

// ====== MCQ 렌더링 ======
function renderMcqOptions(card, q) {
  const optionsWrap = document.createElement("div");
  optionsWrap.className = "options";

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

      if (isClassMode()) {
        const idx = (currentSetData.problems || []).findIndex(
          (x) => x.id === q.id
        );
        const row = ensureCoachRow(q.id);

        if (isCorrect) {
          row.solved = true;
        } else {
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
    meta.lastGradeAt = Date.now();
    meta.date = getTodayYmd();
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

// ====== 여기까지 practice.js ======
