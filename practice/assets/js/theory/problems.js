// 1.5. Problem Rendering Utilities (ported from practice.js)
function normalizeCode(str) {
  return (str || '')
    .replace(/\r\n/g, '\n')         // 개행 통일
    .replace(/\/\/.*$/gm, '')        // // 주석 제거
    .replace(/\/\*[\s\S]*?\*\//g, '') // /* */ 주석 제거
    .replace(/\s+/g, ' ')            // 여러 공백 → 하나
    .replace(/\s*([();,=<>+*\/%-&|!])\s*/g, '$1') // 연산자 주변 공백
    .trim();
}

function normalizeText(str) {
  return (str || '').replace(/\s+/g, ' ').trim().toLowerCase();
}

function getCodeMirrorMode(lang) {
  if (lang === 'python') return 'python';
  if (lang === 'java') return 'text/x-java';
  if (lang === 'csharp' || lang === 'c#') return 'text/x-csharp';
  return 'text/x-csrc'; // c
}

function getWrongFeedbackMessage(q, userVal) {
  if (!q) return '';
  if (q.type === 'mcq') {
    if (userVal === undefined || userVal === null || String(userVal) === '') return '보기를 먼저 선택해 주세요.';
    const map = q.wrongFeedback && typeof q.wrongFeedback === 'object' ? q.wrongFeedback : null;
    if (map) { const msg = map[String(userVal)]; if (msg) return String(msg); }
  }
  if (q.type === 'mcq_multi') {
    if (!Array.isArray(userVal) || userVal.length === 0) return '보기를 먼저 선택해 주세요.';
    if (q.wrongFeedbackText) return String(q.wrongFeedbackText);
  }
  if (q.type === 'short' || q.type === 'code') {
    if (userVal === undefined || userVal === null || String(userVal).trim() === '') return '답안을 입력해 주세요.';
    if (q.wrongFeedbackText) return String(q.wrongFeedbackText);
  }
  return '❌ 다시 한 번 생각해보세요.';
}

// 4. Interactive & Stage Gating
async function enhanceInteractiveProblems(root) {
  const problemTags = Array.from(root.querySelectorAll("p")).filter(p => /\[문제 ID:\s*([\w-]+)\]/.test(p.textContent));
  if (!problemTags.length) return;

  const setId = new URLSearchParams(location.search).get("set");
  let currentSet = null;
  if (setId) {
    try { currentSet = await ProblemService.loadSet(setId); } catch (e) {}
  }

  problemTags.forEach(tag => {
    const match = tag.textContent.match(/\[문제 ID:\s*([\w-]+)\]/);
    if (!match) return;
    const pid = match[1];
    const container = document.createElement("div");
    container.className = "interactive-problem-card";
    const data = currentSet?.problems?.find(p => p.id === pid);
    if (data) renderProblemUI(container, data);
    else container.innerHTML = `<div class="callout warn">문제를 찾을 수 없습니다 (ID: ${pid})</div>`;
    tag.replaceWith(container);
  });
  
  // Only apply stage gating if NOT in section mode (optional choice)
  if (!root.classList.contains("is-section-mode")) {
    groupContentIntoStages(root);
  }
}

function groupContentIntoStages(root) {
  const children = Array.from(root.children);
  let currentStage = document.createElement("div");
  currentStage.className = "content-stage";
  root.appendChild(currentStage);
  
  children.forEach(child => {
    currentStage.appendChild(child);
    if (child.classList.contains("interactive-problem-card")) {
      currentStage = document.createElement("div");
      currentStage.className = "content-stage is-locked";
      root.appendChild(currentStage);
    }
  });
  
  const first = root.querySelector(".content-stage");
  if (first) first.classList.remove("is-locked");
}

function unlockNextStage(currentCard) {
  const stage = currentCard.closest(".content-stage");
  if (stage && stage.nextElementSibling) {
    stage.nextElementSibling.classList.remove("is-locked");
    stage.nextElementSibling.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  updateSectionProgress();
}

// ============================================================
// Enhanced Problem Rendering (supports mcq, mcq_multi, short, code, trace)
// ============================================================

const THEORY_CM_EDITORS = new Map(); // CodeMirror instances keyed by problem id

function renderProblemUI(container, data) {
  const type = data.type || 'mcq';
  const lang = data.lang || 'python';

  // --- Header ---
  const typeLabel = { mcq: 'MCQ', mcq_multi: 'MCQ', short: '단답형', code: '코드작성', trace: '실행흐름' }[type] || type.toUpperCase();
  const headerEl = document.createElement('div');
  headerEl.className = 'problem-header';
  headerEl.innerHTML = `<span class="badge badge--${type}">${typeLabel}</span><strong>${data.title || '실력을 확인해보세요!'}</strong>`;
  container.appendChild(headerEl);

  // --- Question body ---
  if (data.question) {
    const qEl = document.createElement('div');
    qEl.className = 'problem-question';
    qEl.textContent = data.question;
    container.appendChild(qEl);
  }

  // --- Dispatch by type ---
  if (type === 'mcq')       renderMCQUI(container, data);
  else if (type === 'mcq_multi') renderMCQMultiUI(container, data);
  else if (type === 'short')     renderShortUI(container, data);
  else if (type === 'code')      renderCodeUI(container, data, lang);
  else if (type === 'trace')     renderTraceProblemUI(container, data);
  else {
    const fb = document.createElement('p');
    fb.textContent = `(지원하지 않는 문제 타입: ${type})`;
    container.appendChild(fb);
  }

  // --- concept ref link ---
  if (data.conceptRef) {
    const refLink = document.createElement('button');
    refLink.className = 'problem-concept-ref';
    refLink.textContent = `📖 관련 개념 다시 보기`;
    refLink.onclick = () => {
      const targetId = `concept-ref-${data.conceptRef}`;
      const el = document.getElementById(targetId) ||
                 document.querySelector(`[data-concept-id="${data.conceptRef}"]`) ||
                 document.querySelector(`h2, h3`);
      if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); el.classList.add('concept-flash'); setTimeout(() => el.classList.remove('concept-flash'), 1200); }
    };
    container.appendChild(refLink);
  }
}

function showFeedbackMessage(container, msg, isOk) {
  let fb = container.querySelector('.problem-feedback');
  if (!fb) { fb = document.createElement('div'); fb.className = 'problem-feedback'; container.appendChild(fb); }
  fb.textContent = msg;
  fb.className = `problem-feedback ${isOk ? 'is-correct-feedback' : 'is-wrong-feedback'}`;
  if (!isOk) setTimeout(() => { fb.textContent = ''; fb.className = 'problem-feedback'; }, 1800);
}

function renderMCQUI(container, data) {
  const wrap = document.createElement('div');
  wrap.className = 'problem-options';
  (data.options || []).forEach((opt, idx) => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.innerHTML = `<span class="option-num">${idx + 1}</span><span class="option-text">${opt}</span>`;
    btn.onclick = () => {
      if (container.classList.contains('is-solved')) return;
      if (idx === (data.answer ?? data.correctIndex)) {
        btn.classList.add('is-correct');
        container.classList.add('is-solved');
        showFeedbackMessage(container, '✅ 정답입니다!', true);
        unlockNextStage(container);
        updateSectionProgress();
      } else {
        btn.classList.add('is-wrong');
        const fbMsg = getWrongFeedbackMessage(data, idx);
        showFeedbackMessage(container, fbMsg, false);
        setTimeout(() => btn.classList.remove('is-wrong'), 600);
      }
    };
    wrap.appendChild(btn);
  });
  container.appendChild(wrap);
}

function renderMCQMultiUI(container, data) {
  const correctIndexes = Array.isArray(data.correctIndexes) ? data.correctIndexes.map(Number) : [];
  const wrap = document.createElement('div');
  wrap.className = 'problem-options problem-options--multi';
  const hint = document.createElement('p');
  hint.className = 'problem-multi-hint';
  hint.textContent = `💡 정답을 ${correctIndexes.length}개 선택하세요.`;
  wrap.appendChild(hint);

  const selected = new Set();
  (data.options || []).forEach((opt, idx) => {
    const label = document.createElement('label');
    label.className = 'option-multi-label';
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.onchange = () => { if (cb.checked) selected.add(idx); else selected.delete(idx); };
    const span = document.createElement('span');
    span.textContent = `${idx + 1}) ${opt}`;
    label.append(cb, span);
    wrap.appendChild(label);
  });

  const submitBtn = document.createElement('button');
  submitBtn.className = 'check-btn';
  submitBtn.textContent = '선택 완료';
  submitBtn.onclick = () => {
    if (container.classList.contains('is-solved')) return;
    const picked = Array.from(selected).sort((a,b) => a-b);
    const correct = [...correctIndexes].sort((a,b) => a-b);
    const ok = picked.length === correct.length && picked.every((v,i) => v === correct[i]);
    if (ok) {
      container.classList.add('is-solved');
      showFeedbackMessage(container, '✅ 정답입니다!', true);
      unlockNextStage(container);
      updateSectionProgress();
    } else {
      const fbMsg = getWrongFeedbackMessage(data, Array.from(selected));
      showFeedbackMessage(container, fbMsg, false);
      wrap.classList.add('shake'); setTimeout(() => wrap.classList.remove('shake'), 500);
    }
  };
  wrap.appendChild(submitBtn);
  container.appendChild(wrap);
}

function renderShortUI(container, data) {
  const wrap = document.createElement('div');
  wrap.className = 'problem-input-wrap';
  const input = document.createElement('input');
  input.className = 'short-answer-input';
  input.placeholder = data.placeholder || '답안을 입력하세요...';
  const btn = document.createElement('button');
  btn.className = 'check-btn'; btn.textContent = '확인';
  const check = () => {
    if (container.classList.contains('is-solved')) return;
    const val = input.value;
    const normVal = normalizeText(val);
    let ok = false;
    if (data.expectedAnyOf) {
      ok = data.expectedAnyOf.some(ans => normalizeText(ans) === normVal);
    } else if (data.expectedText) {
      ok = normalizeText(data.expectedText) === normVal;
    } else if (Array.isArray(data.answer)) {
      ok = data.answer.some(a => normalizeText(String(a)) === normVal);
    } else if (data.answer !== undefined) {
      ok = normVal === normalizeText(String(data.answer));
    }
    if (ok) {
      container.classList.add('is-solved');
      input.disabled = true; btn.disabled = true;
      showFeedbackMessage(container, '✅ 정답입니다!', true);
      unlockNextStage(container);
      updateSectionProgress();
    } else {
      input.classList.add('is-wrong', 'shake');
      const fbMsg = getWrongFeedbackMessage(data, val);
      showFeedbackMessage(container, fbMsg, false);
      setTimeout(() => input.classList.remove('is-wrong', 'shake'), 600);
    }
  };
  btn.onclick = check;
  input.addEventListener('keydown', e => { if (e.key === 'Enter') check(); });
  wrap.append(input, btn); container.appendChild(wrap);
}

function renderCodeUI(container, data, lang) {
  const wrap = document.createElement('div');
  wrap.className = 'problem-code-wrap';

  // Starter code hint
  const ta = document.createElement('textarea');
  ta.className = 'problem-code-textarea';
  ta.value = data.starterCode || '';
  ta.placeholder = '여기에 코드를 작성하세요...';
  wrap.appendChild(ta);

  const btn = document.createElement('button');
  btn.className = 'check-btn';
  btn.textContent = '코드 제출';
  wrap.appendChild(btn);
  container.appendChild(wrap);

  // CodeMirror upgrade
  let editor = null;
  if (window.CodeMirror) {
    const mode = getCodeMirrorMode(data.lang || lang);
    editor = CodeMirror.fromTextArea(ta, {
      mode,
      theme: 'material-darker',
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      viewportMargin: Infinity,
    });
    if (data.id) THEORY_CM_EDITORS.set(data.id, editor);
  }

  btn.onclick = () => {
    if (container.classList.contains('is-solved')) return;
    const raw = editor ? editor.getValue() : ta.value;
    const normUser = normalizeCode(raw);

    let candidates = [];
    if (Array.isArray(data.expectedCode)) candidates = data.expectedCode;
    else if (typeof data.expectedCode === 'string') candidates = [data.expectedCode];
    if (Array.isArray(data.expectedCodes)) candidates = candidates.concat(data.expectedCodes);

    const ok = candidates.filter(Boolean).some(c => normalizeCode(c) === normUser);
    if (ok) {
      container.classList.add('is-solved');
      btn.disabled = true;
      showFeedbackMessage(container, '✅ 정답입니다!', true);
      unlockNextStage(container);
      updateSectionProgress();
    } else {
      const fbMsg = getWrongFeedbackMessage(data, raw);
      showFeedbackMessage(container, fbMsg, false);
      wrap.classList.add('shake'); setTimeout(() => wrap.classList.remove('shake'), 500);
    }
  };
}

function renderTraceProblemUI(container, data) {
  // If there's a related quiz question after the trace, render it
  if (data.question && data.type === 'trace' && data.answer !== undefined) {
    // Render the trace panel first, then the quiz
    renderTracePanel(container, data);
    // Add a quiz UI below (short type)
    const quizWrap = document.createElement('div');
    quizWrap.className = 'problem-trace-quiz';
    const qEl = document.createElement('p');
    qEl.className = 'problem-question';
    qEl.textContent = data.traceQuestion || '트레이스를 보고, 물음에 답하세요:';
    quizWrap.appendChild(qEl);
    renderShortUI(quizWrap, data);
    container.appendChild(quizWrap);
  } else {
    renderTracePanel(container, data);
  }
}

// Trace Panel (ported from practice.js)
function renderTracePanel(targetEl, q) {
  const steps = Array.isArray(q?.trace) ? q.trace : [];
  if (!steps.length || !q?.code) return;

  const lines = String(q.code).replace(/\r\n?/g, '\n').split('\n');
  let idx = 0;

  const wrap = document.createElement('div');
  wrap.className = 'trace-panel';

  const head = document.createElement('div');
  head.className = 'trace-head';
  const title = document.createElement('div');
  title.className = 'trace-title';
  title.textContent = '실행 흐름(Trace)';
  const pager = document.createElement('div');
  pager.className = 'trace-pager';
  head.appendChild(title); head.appendChild(pager);
  wrap.appendChild(head);

  const body = document.createElement('div');
  body.className = 'trace-body';
  const codeBox = document.createElement('pre');
  codeBox.className = 'trace-code';
  const varBox = document.createElement('div');
  varBox.className = 'trace-vars';
  const noteBox = document.createElement('div');
  noteBox.className = 'trace-note';
  body.append(codeBox, varBox, noteBox);
  wrap.appendChild(body);

  const controls = document.createElement('div');
  controls.className = 'trace-controls';
  const prevBtn = document.createElement('button');
  prevBtn.type = 'button'; prevBtn.textContent = '◀ 이전';
  const nextBtn = document.createElement('button');
  nextBtn.type = 'button'; nextBtn.textContent = '다음 ▶';
  controls.append(prevBtn, nextBtn);
  wrap.appendChild(controls);

  function renderStep(i) {
    const step = steps[i];
    const lineNo = Number(step?.line) || 0;
    codeBox.innerHTML = '';
    lines.forEach((ln, li) => {
      const row = document.createElement('div');
      row.className = 'trace-line' + (lineNo === li + 1 ? ' active' : '');
      const no = document.createElement('span');
      no.className = 'trace-line-no'; no.textContent = String(li + 1).padStart(2, ' ');
      const tx = document.createElement('span');
      tx.className = 'trace-line-text'; tx.textContent = ln;
      row.append(no, tx); codeBox.appendChild(row);
    });

    varBox.innerHTML = '';
    const vars = step?.vars && typeof step.vars === 'object' ? step.vars : {};
    const keys = Object.keys(vars);
    if (keys.length) {
      keys.forEach(k => {
        const row = document.createElement('div');
        row.className = 'trace-var-row';
        const key = document.createElement('span');
        key.className = 'trace-var-key'; key.textContent = k;
        const val = document.createElement('span');
        val.className = 'trace-var-val'; val.textContent = String(vars[k]);
        row.append(key, val); varBox.appendChild(row);
      });
    } else {
      const empty = document.createElement('div');
      empty.className = 'trace-var-empty'; empty.textContent = '변수 변화 없음';
      varBox.appendChild(empty);
    }
    noteBox.textContent = step?.note ? `💡 ${step.note}` : '';
    pager.textContent = `${i + 1} / ${steps.length}`;
    prevBtn.disabled = i <= 0;
    nextBtn.disabled = i >= steps.length - 1;
  }

  prevBtn.addEventListener('click', () => { if (idx > 0) { idx--; renderStep(idx); } });
  nextBtn.addEventListener('click', () => { if (idx < steps.length - 1) { idx++; renderStep(idx); } });
  renderStep(0);
  targetEl.appendChild(wrap);
}
