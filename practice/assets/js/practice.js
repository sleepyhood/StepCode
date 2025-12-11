// practice/assets/js/practice.js

let currentSetData = null;
let currentLang = "c"; // 지금은 C만, 나중에 언어별 코드 확장

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
  pre.className = "code-block";

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

  (q.options || []).forEach((opt, i) => {
    const optDiv = document.createElement("div");
    optDiv.className = "option-item";

    const input = document.createElement("input");
    input.type = "radio";
    input.name = q.id;
    input.value = String(i);
    input.setAttribute("data-question", q.id);

    const inputId = `${q.id}_opt${i}`;
    input.id = inputId;

    const label = document.createElement("label");
    label.className = "option-label";
    label.htmlFor = inputId;

    const letter = document.createElement("span");
    letter.className = "option-letter";
    const labels = q.optionLabels || [];
    letter.textContent = (labels[i] || String.fromCharCode(65 + i)) + ".";

    // ▼ 여기부터 수정 ▼
    const codePre = document.createElement("pre");
    codePre.className = "option-code";

    const codeEl = document.createElement("code");
    codeEl.className = `language-${currentLang}`;
    codeEl.textContent = opt;

    codePre.appendChild(codeEl);
    // ▲ 여기까지 수정 ▲

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
        const normExp = normalizeCode(q.expectedCode);
        isCorrect = normUser === normExp;
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

// ====== HUD: 이전/다음/TOP/BOTTOM ======
function setupHud() {
  const btnPrev = document.getElementById("btn-prev");
  const btnNext = document.getElementById("btn-next");
  const btnTop = document.getElementById("btn-top");
  const btnBottom = document.getElementById("btn-bottom");

  // HUD가 없는 페이지면 무시
  if (!btnPrev || !btnNext || !btnTop || !btnBottom) return;

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

  const getCurrentIndex = () => {
    const cards = getCards();
    if (!cards.length) return -1;

    const scrollY = window.scrollY;
    const viewportHeight = window.innerHeight;
    const targetY = scrollY + viewportHeight * 0.25; // 화면 위에서 1/4 지점 기준

    let bestIdx = 0;
    let bestDist = Infinity;

    cards.forEach((card, idx) => {
      const top = card.offsetTop;
      const height = card.offsetHeight;
      const mid = top + height / 2;
      const dist = Math.abs(mid - targetY);
      if (dist < bestDist) {
        bestDist = dist;
        bestIdx = idx;
      }
    });

    return bestIdx;
  };

  btnPrev.addEventListener("click", () => {
    const idx = getCurrentIndex();
    if (idx === -1) return;
    scrollToCard(idx - 1);
  });

  btnNext.addEventListener("click", () => {
    const idx = getCurrentIndex();
    if (idx === -1) return;
    scrollToCard(idx + 1);
  });

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