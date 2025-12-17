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
    localStorage.setItem(
      getAnswerStorageKey(setId),
      JSON.stringify(answers)
    );
  } catch (e) {
    console.warn("failed to save answers", e);
  }
}

function recordAnswer(questionId, value) {
  if (!currentSetId) return;
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
      lastGradeAt: Number(parsed.lastGradeAt) || 0
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

let solveElapsedMs = 0;      // 누적(저장되는) 시간
let solveStartAt = 0;        // running 시작 시각(Date.now)
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
    localStorage.setItem(getSolveTimerKey(setId), String(Math.max(0, Math.floor(ms))));
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
    return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
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

    setupSolveTimerForCurrentSet();

    // 제목 표시
    titleSpan.textContent = currentSetData.title || "연습장";

    // 언어 셀렉트 (지금은 C만)
    setupLangSelect(currentSetData.availableLanguages || ["c"]);

    // 문제 렌더
    renderSet();

    

    // HUD 세팅
    setupHud();

    // 채점 버튼 연결
    setupGrading();
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

  select.addEventListener("change", (e) => {
    currentLang = e.target.value;
    // 나중에 언어별 코드가 생기면 여기서 다시 렌더링
    renderSet();
  });
}

// ====== 유틸: 정규화 함수 (기존 코드 그대로) ======
function normalizeCode(str) {
  return (
    (str || "")
      .replace(/\r\n/g, "\n") // 개행 통일
      .replace(/\/\/.*$/gm, "") // // 주석 제거
      .replace(/\/\*[\s\S]*?\*\//g, "") // /* */ 주석 제거
      .replace(/\s+/g, " ") // 여러 공백 → 하나
      .replace(/\s*([();,=<>+*\/%-&|!])\s*/g, "$1") // 연산자 주변 공백
      .trim()
  );
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

  questions.forEach((q, idx) => {
    const card = document.createElement("section");
    card.className = "question-card";

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
    const desc = document.createElement("p");
    desc.className = "description";
    desc.textContent = q.description || "";
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

    // --- 피드백 영역 ---
    const feedback = document.createElement("div");
    feedback.className = "feedback";
    feedback.setAttribute("data-feedback", q.id);
    card.appendChild(feedback);

    container.appendChild(card);
  });

    // ▼ 렌더가 다 끝난 뒤에 하이라이트 호출 ▼
  if (window.Prism) {
    Prism.highlightAllUnder(container);
    upgradeCodeInputsToCodeMirror(container);

  }
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
  // ✅ (추가) Python if Code: "if  # ..." 형태면 조건식 빈칸 입력 UI로 렌더
  if (q.type === "code" && isIfConditionBlankQuestion(q)) {
    renderIfConditionBlank(card, q);
    return;
  }

  // (기존) short/code 기본 textarea
  const input = document.createElement("textarea");
  input.className = "answer-input";
  input.setAttribute("data-question", q.id);
  input.setAttribute("data-qtype", q.type);

  input.spellcheck = false;
  input.rows = q.type === "code" ? 2 : 1;

  if (q.type === "short") {
    input.placeholder = "정답을 입력하세요.";
  } else if (q.type === "code") {
    input.placeholder = "여기에 코드를 작성하세요.";
  }

  // 저장된 답안 복원
  const saved = currentAnswers && currentAnswers[q.id];
  if (typeof saved === "string") {
    input.value = saved;
  }

  // 입력할 때마다 자동 저장
  input.addEventListener("input", () => {
    recordAnswer(q.id, input.value);
  });

  card.appendChild(input);

  if (q.hint) {
    const hint = document.createElement("div");
    hint.className = "hint";
    hint.textContent = q.hint;
    card.appendChild(hint);
  }
}

// ===== LanguageAdapter (헬퍼 하드코딩 제거) =====
const LanguageAdapter = {
  python: {
    condBlank: {
      left: (kw) => kw,     // if / elif
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
  (typeof getSolveElapsedNow === "function" && typeof formatElapsed === "function")
    ? formatElapsed(getSolveElapsedNow())
    : (document.getElementById("solve-timer")?.textContent || "");

if (rem > 0) {
  gradeButton.disabled = true;
  gradeButton.textContent = `채점 대기 ${sec}초 (오늘 ${meta.attempts}회)`;
  if (metaEl) metaEl.textContent = `오늘 채점 ${meta.attempts}회 · 풀이 ${solveText} · 다음 채점까지 ${sec}초`;
} else {
  gradeButton.disabled = false;
  gradeButton.textContent = `채점하기 (오늘 ${meta.attempts}회)`;
  if (metaEl) metaEl.textContent = `오늘 채점 ${meta.attempts}회 · 풀이 ${solveText}`;
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

    const questions = currentSetData.problems || [];
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
          isCorrect = q.expectedAnyOf.some((ans) => normalizeText(ans) === norm);
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
        else if (typeof q.expectedCode === "string") candidates = [q.expectedCode];
        if (Array.isArray(q.expectedCodes)) candidates = candidates.concat(q.expectedCodes);

        isCorrect = candidates.filter(Boolean).some((code) => normalizeCode(code) === normUser);
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
      scoreEl.textContent = `총 ${currentSetData.problems.length}문제 중 ${correctCount}문제 정답`;
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

  const getCards = () =>
    Array.from(document.querySelectorAll(".question-card"));

  const scrollToCard = (index) => {
    const cards = getCards();
    if (!cards.length) return;
    if (index < 0) index = 0;
    if (index >= cards.length) index = cards.length - 1;

    cards[index].scrollIntoView({
      behavior: "smooth",
      block: "start"
    });
  };

  // --- 문제 목록 패널 구성 ---
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
      scrollToCard(idx);
      panel.classList.remove("open");
    });

    panel.appendChild(itemBtn);
  });

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
      behavior: "smooth"
    });
  });

  btnBottom.addEventListener("click", () => {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth"
    });
  });
}


// ====== 여기까지 practice.js ======