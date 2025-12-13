// practice/assets/js/practice.js

let currentSetData = null;
let currentLang = "c"; // 지금은 C만, 나중에 언어별 코드 확장


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


// ====== 단답형/코드 textarea 렌더링 ======
function renderTextArea(card, q) {
  const input = document.createElement("textarea");
  input.className = "answer-input";
  input.setAttribute("data-question", q.id);
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


// ====== 채점 버튼 로직 ======
function setupGrading() {
  const gradeButton = document.getElementById("grade-btn");
  const scoreEl = document.getElementById("score");

  if (!gradeButton) return;

  gradeButton.addEventListener("click", () => {
    const questions = currentSetData.problems || [];
    let correctCount = 0;

    questions.forEach((q) => {
      const feedbackEl = document.querySelector(
        `[data-feedback="${q.id}"]`
      );
      let isCorrect = false;

      if (q.type === "mcq") {
        const selected = document.querySelector(
          `input[name="${q.id}"]:checked`
        );
        if (selected) {
          const chosenIndex = parseInt(selected.value, 10);
          isCorrect = chosenIndex === q.correctIndex;
        } else {
          isCorrect = false;
        }
      } else if (q.type === "short") {
        const inputEl = document.querySelector(
          `[data-question="${q.id}"]`
        );
        const val = (inputEl && inputEl.value) || "";

        if (q.expectedAnyOf) {
          const norm = normalizeText(val);
          isCorrect = q.expectedAnyOf.some(
            (ans) => normalizeText(ans) === norm
          );
        } else if (q.expectedText) {
          const normUser = normalizeText(val);
          const normExp = normalizeText(q.expectedText);
          isCorrect = normUser === normExp;
        }
      } else if (q.type === "code") {
  const inputEl = document.querySelector(
    `[data-question="${q.id}"]`
  );
  const userCode = (inputEl && inputEl.value) || "";
  const normUser = normalizeCode(userCode);

  // expectedCode가 문자열 하나일 수도, 배열일 수도 있게 처리
  let candidates = [];

  if (Array.isArray(q.expectedCode)) {
    candidates = q.expectedCode;
  } else if (typeof q.expectedCode === "string") {
    candidates = [q.expectedCode];
  }

  // (선택) expectedCodes라는 별도 배열도 허용하고 싶으면:
  if (Array.isArray(q.expectedCodes)) {
    candidates = candidates.concat(q.expectedCodes);
  }

  isCorrect = candidates
    .filter(Boolean)
    .some((code) => normalizeCode(code) === normUser);
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

    scoreEl.textContent = `총 ${currentSetData.problems.length}문제 중 ${correctCount}문제 정답`;
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