/**
 * StepCode - Theory Page Logic (Ultimate Integrated Version)
 */

// 1. Core Utilities
function getMdRenderer() {
  if (!window.markdownit || !window.DOMPurify) return null;
  return window.markdownit({ html: true, linkify: true, breaks: true });
}

function stripFrontMatter(mdText) {
  const raw = String(mdText || "").replace(/\r\n?/g, "\n");
  if (!raw.startsWith("---\n")) return raw;
  const end = raw.indexOf("\n---\n", 4);
  return end === -1 ? raw : raw.slice(end + 5);
}

function replaceLangBadges(html) {
  if (!html) return "";
  return html.replace(/\{lang:([^}]+)\}/g, (match, lang) => {
    const l = lang.toLowerCase();
    const map = { "python": "Python", "c": "C", "java": "Java", "csharp": "C#" };
    const label = map[l] || lang.toUpperCase();
    return `<span class="theory-lang-badge theory-lang-badge--${l}">${label}</span>`;
  });
}

function replaceCheckboxes(html) {
  if (!html) return "";
  // Converts [ ] and [x] into interactive-looking checkboxes and wraps text for styling
  return html
    .replace(/(<li>|<p>)\s*\[ \]\s*(.*?)(<\/li>|<\/p>)/g, 
      '$1<label class="theory-task-item"><input type="checkbox" class="theory-checkbox"> <span class="theory-task-text">$2</span></label>$3')
    .replace(/(<li>|<p>)\s*\[x\]\s*(.*?)(<\/li>|<\/p>)/gi, 
      '$1<label class="theory-task-item"><input type="checkbox" class="theory-checkbox" checked> <span class="theory-task-text">$2</span></label>$3');
}

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

// 2. Registry & Title Helpers
function buildTheoryLookup(items) {
  const byConceptId = {}, byCategoryId = {};
  (items || []).forEach(it => { if (it.conceptId) byConceptId[it.conceptId] = it; if (it.categoryId) byCategoryId[it.categoryId] = it; });
  return { byConceptId, byCategoryId };
}
function toSetMap(sets) { const map = {}; (sets || []).forEach(s => { if (s.id) map[s.id] = s; }); return map; }
function pickEntry(params, lookup, setMap) {
  const cid = params.get("concept"), catid = params.get("category"), sid = params.get("set");
  if (cid && lookup.byConceptId[cid]) return lookup.byConceptId[cid];
  if (catid && lookup.byCategoryId[catid]) return lookup.byCategoryId[catid];
  if (sid && setMap[sid]?.categoryId) return lookup.byCategoryId[setMap[sid].categoryId];
  return null;
}
function updateTitle(entry) {
  const tEl = document.getElementById("theory-title");
  if (tEl) tEl.textContent = entry.title || "개념";
}

function fixRelativeImagePaths(root, mdPath) {
  if (!mdPath) return;
  const baseDir = mdPath.substring(0, mdPath.lastIndexOf("/"));
  root.querySelectorAll("img").forEach(img => {
    const src = img.getAttribute("src");
    if (src && !src.startsWith("http") && !src.startsWith("data:") && !src.startsWith("/")) {
      img.src = baseDir + (src.startsWith("./") ? src.slice(1) : "/" + src);
    }
  });
}

// 3. Markdown Rendering
async function renderTheoryMarkdown(target, mdText, mdPath = "") {
  const raw = stripFrontMatter(mdText);
  const md = getMdRenderer();
  if (!md) { target.textContent = raw; return; }
  
  // Render as a single comprehensive document
  const rawHtml = md.render(raw);
  const cleanHtml = window.DOMPurify.sanitize(rawHtml);
  let finalHtml = replaceLangBadges(cleanHtml);
  finalHtml = replaceCheckboxes(finalHtml);
  
  // Convert standard <hr> into a stylish slide divider
  finalHtml = finalHtml.replace(/<hr\s*\/?>/gi, '<div class="theory-slide-divider"></div>');
  
  target.innerHTML = finalHtml;
  
  // Flag as section-mode if dividers are detected (useful for roadmap filtering)
  if (finalHtml.includes('theory-slide-divider')) {
    target.classList.add("is-section-mode");
  } else {
    target.classList.remove("is-section-mode");
  }
  
  // Mermaid Detection
  target.querySelectorAll('code.language-mermaid').forEach(c => {
    const pre = c.closest('pre');
    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = c.textContent;
    if (pre) pre.replaceWith(div);
  });

  if (window.mermaid && target.querySelectorAll('.mermaid').length > 0) {
    const renderMermaid = () => {
      // Visibility check to prevent translate(undefined) errors
      if (target.offsetWidth > 0 || target.offsetHeight > 0) {
        try { 
          window.mermaid.init(undefined, target.querySelectorAll('.mermaid')); 
        } catch (e) {
          console.warn("Mermaid init failed, retrying...", e);
        }
      } else {
        setTimeout(renderMermaid, 500);
      }
    };
    setTimeout(renderMermaid, 300);
  }

  fixRelativeImagePaths(target, mdPath);
  enhanceLessonCallouts(target);
  enhanceCodeBlocks(target);
  enhanceTraceGridBlocks(target);
  enhanceIoBlocks(target);
  await enhanceInteractiveProblems(target);
  autoNumberHeadings(target);
  wrapContentIntoSectionCards(target);
  setupMiniCheckCards(target);
  buildFloatingTOC(target);
  buildRoadmap(target);
  updateSectionProgress();
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

// 5. Marp Slide Mode
async function setupSlideMode(slidePath) {
  const toggleBtn = document.getElementById("theory-mode-toggle");
  const slideViewer = document.getElementById("theory-slide-viewer");
  const docContent = document.getElementById("theory-content");
  const marpContainer = document.getElementById("marp-container");
  if (!toggleBtn || !slideViewer || !marpContainer) return;

  let slides = [];
  let currentIndex = 0;
  let isSlideMode = false;

  try {
    const res = await fetch(slidePath.startsWith("./") ? slidePath.slice(2) : slidePath);
    if (!res.ok) return;
    const mdText = await res.text();
    const baseDir = slidePath.substring(0, slidePath.lastIndexOf("/"));

    const styleMatch = mdText.match(/style:\s*\|?\s*([\s\S]*?)(?=\n---)/);
    if (styleMatch) {
      const css = styleMatch[1].trim().replace(/@import\s+['"](.+?)['"]/g, (m, p) => `@import "${baseDir}/${p}"`);
      let styleTag = document.getElementById("marp-injected-style") || document.createElement("style");
      styleTag.id = "marp-injected-style";
      styleTag.textContent = css.replace(/section/g, "#marp-container section");
      document.head.appendChild(styleTag);
    }

    const md = getMdRenderer();
    const slideChunks = stripFrontMatter(mdText).split(/\n---\n/);
    let lastStage = "1";
    slides = slideChunks.map(chunk => {
      const sec = document.createElement("section");
      const mClass = chunk.match(/<!--\s*_class:\s*([\w-]+)\s*-->/);
      if (mClass) sec.className = mClass[1];
      
      const mStage = chunk.match(/<!--\s*_stage:\s*(\d+)\s*-->/);
      if (mStage) lastStage = mStage[1];
      sec.dataset.stage = lastStage;
      
      const mLocked = chunk.match(/<!--\s*_locked:\s*(true|false)\s*-->/);
      if (mLocked && mLocked[1] === "true") sec.dataset.locked = "true";
      
      const html = window.DOMPurify.sanitize(md.render(chunk));
      sec.innerHTML = replaceLangBadges(html);
      
      sec.querySelectorAll('code.language-mermaid').forEach(c => {
        const pre = c.closest('pre');
        const div = document.createElement('div');
        div.className = 'mermaid'; div.textContent = c.textContent;
        if (pre) pre.replaceWith(div);
      });
      
      fixRelativeImagePaths(sec, slidePath);
      enhanceCodeBlocks(sec);
      return sec;
    });

    if (slides.length > 0) {
      toggleBtn.hidden = false;
      // Option: Start in document mode by default if it's a lesson
      // enterSlideMode();
    }
  } catch (e) { console.error("Slide setup failed:", e); }

  function renderSlide(idx) {
    if (!isSlideMode) return;
    if (idx < 0 || idx >= slides.length) return;
    currentIndex = idx;
    marpContainer.innerHTML = "";
    
    const node = slides[currentIndex].cloneNode(true);
    const sw = slideViewer.clientWidth ? slideViewer.clientWidth - 40 : 1080;
    const scale = sw / 1280;
    
    node.style.cssText = `width:1280px;height:720px;transform:scale(${scale});transform-origin:top left;display:block;margin:0;position:absolute;top:0;left:0;`;
    marpContainer.style.height = `${720 * scale}px`;
    marpContainer.appendChild(node);
    
    // Mermaid render inside slide
    if (window.mermaid) {
      setTimeout(() => { 
        try { window.mermaid.init(undefined, node.querySelectorAll('.mermaid')); } catch (e) {} 
      }, 100);
    }
    
    const info = document.getElementById("slide-page-info");
    if (info) info.textContent = `${currentIndex + 1} / ${slides.length}`;
  }

  function enterSlideMode() {
    isSlideMode = true;
    const layout = document.querySelector(".theory-layout");
    const sidebar = document.querySelector(".theory-side");
    if (layout) { layout.style.display = "block"; layout.style.padding = "0"; }
    if (sidebar) sidebar.style.display = "none";
    slideViewer.style.display = "flex"; slideViewer.hidden = false;
    docContent.style.display = "none";
    const fw = document.getElementById("theory-filter-wrap"); if (fw) fw.style.display = "none";
    toggleBtn.textContent = "문서로 보기"; toggleBtn.classList.add("is-active");
    window.scrollTo(0, 0); renderSlide(currentIndex);
  }

  function enterDocumentMode() {
    isSlideMode = false;
    const layout = document.querySelector(".theory-layout");
    const sidebar = document.querySelector(".theory-side");
    if (layout) { layout.style.display = "grid"; layout.style.padding = ""; }
    if (sidebar) sidebar.style.display = "block";
    slideViewer.style.display = "none"; slideViewer.hidden = true;
    docContent.style.display = "block";
    const fw = document.getElementById("theory-filter-wrap"); if (fw) fw.style.display = "block";
    toggleBtn.textContent = "슬라이드 보기"; toggleBtn.classList.remove("is-active");
  }

  toggleBtn.onclick = (e) => { e.preventDefault(); if (isSlideMode) enterDocumentMode(); else enterSlideMode(); };
  document.getElementById("slide-prev").onclick = () => renderSlide(currentIndex - 1);
  document.getElementById("slide-next").onclick = () => renderSlide(currentIndex + 1);
  
  document.addEventListener("keydown", (e) => {
    if (!isSlideMode) return;
    if (e.key === "ArrowLeft") renderSlide(currentIndex - 1);
    if (e.key === "ArrowRight") renderSlide(currentIndex + 1);
  });
}

// 6. Auxiliary UI Enhancers
function enhanceLessonCallouts(root) {
  root.querySelectorAll("blockquote").forEach(q => {
    const m = q.textContent.match(/\[!(\w+)\]/);
    if (m) q.classList.add("lesson-callout", `lesson-callout--${m[1].toLowerCase()}`);
  });
}
function enhanceCodeBlocks(root) {
  root.querySelectorAll("pre > code").forEach(c => {
    const pre = c.closest("pre");
    if (pre) { 
      pre.classList.add("line-numbers", "theory-code"); 
      if (window.Prism) window.Prism.highlightElement(c); 
    }
  });
}
function enhanceTraceGridBlocks(root) {}
function enhanceIoBlocks(root) {}

// 6.5. Section Card Wrapping (H1/H2 → Card containers)
function wrapContentIntoSectionCards(root) {
  const dividers = root.querySelectorAll('.theory-slide-divider');
  // Only wrap if dividers exist (slide-based content)
  if (dividers.length === 0) return;

  const allChildren = Array.from(root.childNodes);
  const sections = [];
  let currentSection = [];

  allChildren.forEach(node => {
    if (node.classList && node.classList.contains('theory-slide-divider')) {
      if (currentSection.length > 0) {
        sections.push(currentSection);
        currentSection = [];
      }
    } else {
      currentSection.push(node);
    }
  });
  if (currentSection.length > 0) sections.push(currentSection);

  root.innerHTML = '';
  sections.forEach((nodes, idx) => {
    if (nodes.length === 0) return;
    // Skip purely whitespace sections
    const hasContent = nodes.some(n => n.textContent?.trim().length > 0);
    if (!hasContent) return;

    const card = document.createElement('div');
    card.className = 'theory-section-card';
    card.dataset.sectionIndex = idx;
    nodes.forEach(n => card.appendChild(n));
    root.appendChild(card);
  });
}

// 6.6. Progress Tracking
function updateSectionProgress() {
  // Count both legacy interactive-problem-cards and new mini-check-cards
  const legacyCards  = document.querySelectorAll('.interactive-problem-card');
  const miniCards    = document.querySelectorAll('.theory-mini-check-card');
  const total  = legacyCards.length + miniCards.length;
  const solved = document.querySelectorAll('.interactive-problem-card.is-solved').length
               + document.querySelectorAll('.theory-mini-check-card.is-solved').length;

  const milestoneEl = document.getElementById('dashboard-milestone-count');
  if (milestoneEl) milestoneEl.textContent = `${solved}/${total}`;

  const statusEl = document.getElementById('dashboard-status-text');
  if (statusEl) {
    if (total === 0) statusEl.textContent = 'Reading in progress...';
    else if (solved === total) statusEl.textContent = '🎉 All milestones complete!';
    else statusEl.textContent = `${solved} of ${total} milestones completed`;
  }

  const pct = total > 0 ? Math.round((solved / total) * 100) : 0;
  const bar = document.getElementById('roadmap-progress-bar');
  const txt = document.getElementById('roadmap-progress-text');
  if (bar) bar.style.width = pct + '%';
  if (txt) txt.textContent = pct + '% Complete';
}

// 6.7. Mini Check Card Logic (theory-mini-check-card)
/**
 * Initializes all .theory-mini-check-card elements within the given root.
 * Each card must have:
 *   - data-answer: the expected answer string
 *   - .stage-key-input: text input element
 *   - .stage-unlock-btn: submit button element
 *
 * Normalizes both input and answer (trim + lowercase) before comparison.
 * On correct answer: marks card as .is-solved, triggers progress update.
 * On wrong answer: shakes the input briefly.
 */
function setupMiniCheckCards(root) {
  const cards = root.querySelectorAll('.theory-mini-check-card');
  if (cards.length === 0) return;

  cards.forEach(card => {
    // Prevent double-binding if re-rendered
    if (card.dataset.bound === 'true') return;
    card.dataset.bound = 'true';

    const expectedAnswer = (card.dataset.answer || '').trim();
    const input = card.querySelector('.stage-key-input');
    const btn = card.querySelector('.stage-unlock-btn');

    if (!input || !btn || !expectedAnswer) return;

    // Normalize helper: remove all whitespace for flexible matching
    const normalize = (s) => s.replace(/\s+/g, '').toLowerCase();

    const submit = () => {
      if (card.classList.contains('is-solved')) return; // Already solved

      const val = input.value;
      const isCorrect = normalize(val) === normalize(expectedAnswer);

      if (isCorrect) {
        card.classList.add('is-solved');
        input.disabled = true;
        btn.disabled = true;
        btn.textContent = '✓ 완료!';
        btn.classList.add('is-correct-btn');
        updateSectionProgress();
      } else {
        input.classList.add('is-wrong');
        input.classList.add('shake');
        setTimeout(() => {
          input.classList.remove('is-wrong', 'shake');
        }, 600);
      }
    };

    btn.addEventListener('click', submit);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') submit();
    });
  });
}

// 7. Related Problems Rendering
function renderRelatedProblems(entry, setMap) {
  const listEl = document.getElementById("theory-related-list");
  const startBtn = document.getElementById("theory-start-btn");
  if (!listEl) return;

  listEl.innerHTML = "";

  if (entry.recommendedSetId && startBtn) {
    startBtn.hidden = false;
    startBtn.href = `practice.html?set=${encodeURIComponent(entry.recommendedSetId)}`;
  } else if (startBtn) {
    startBtn.hidden = true;
  }

  let relatedSets = [];
  if (Array.isArray(entry.relatedSetIds) && entry.relatedSetIds.length > 0) {
    relatedSets = entry.relatedSetIds.map(id => setMap[id]).filter(Boolean);
  } else if (entry.categoryId) {
    relatedSets = Object.values(setMap).filter(s => s.categoryId === entry.categoryId);
  }

  relatedSets.sort((a, b) => (a.round || 0) - (b.round || 0));

  if (relatedSets.length === 0) {
    const emptyMsg = document.createElement("p");
    emptyMsg.style.fontSize = "14px";
    emptyMsg.style.color = "var(--color-gray-500)";
    emptyMsg.textContent = "관련 문제가 없습니다.";
    listEl.appendChild(emptyMsg);
    return;
  }

  const row = document.createElement("div");
  row.className = "part-round-row";
  row.style.display = "flex";
  row.style.flexWrap = "wrap";
  row.style.gap = "8px";
  row.style.marginTop = "10px";

  relatedSets.forEach(setMeta => {
    const a = document.createElement("a");
    a.className = "part-round-chip";
    a.href = `practice.html?set=${encodeURIComponent(setMeta.id)}`;
    a.style.textDecoration = "none";
    const diff = setMeta.difficulty === "challenge" ? "Challenge" : "Basic";
    a.textContent = `R${setMeta.round || 1} · ${diff}`;
    if (setMeta.title) a.title = setMeta.title;
    row.appendChild(a);
  });

  listEl.appendChild(row);
}

async function initTheoryPage() {
  const contentEl = document.getElementById("theory-content");
  const params = new URLSearchParams(location.search);
  try {
    const [theoryIndex, sets] = await Promise.all([ProblemService.listTheoryIndex(), ProblemService.listSets()]);
    const setMap = toSetMap(sets);
    const entry = pickEntry(params, buildTheoryLookup(theoryIndex), setMap);
    if (!entry) return;
    updateTitle(entry);
    const res = await fetch(entry.mdPath);
    if (!res.ok) throw new Error("MD fetch failed");
    const mdText = await res.text();
    await renderTheoryMarkdown(contentEl, mdText, entry.mdPath);
    if (entry.slidePath) setupSlideMode(entry.slidePath);
    
    renderRelatedProblems(entry, setMap);

    const savedPos = localStorage.getItem(`readPosition_${location.search}`);
    if (savedPos && parseInt(savedPos) > 150) {
      setTimeout(() => showResumeToast(parseInt(savedPos)), 1000);
    }
  } catch (e) { console.error("Initialization failed:", e); }
}

// 8. Auto Numbering & Floating Navigation
function autoNumberHeadings(root) {
  const headings = Array.from(root.querySelectorAll("h1, h2, h3, h4, h5, h6"));
  if (headings.length === 0) return;

  let minLevel = 6;
  headings.forEach(h => {
    const level = parseInt(h.tagName.charAt(1));
    if (level < minLevel) minLevel = level;
  });

  const counters = [0, 0, 0, 0, 0, 0, 0];
  headings.forEach(h => {
    if (h.closest('.interactive-problem-card') || h.closest('.theory-mini-check-card') || h.closest('.theory-toc-popup')) return;
    const level = parseInt(h.tagName.charAt(1));
    if(level > 6 || level < 1) return;

    counters[level]++;
    for (let i = level + 1; i <= 6; i++) counters[i] = 0;

    // Check if the heading already starts with a number (e.g. "1. ", "1.1 ", "1.1. ")
    if (/^\s*\d+(\.\d+)*\.?\s/.test(h.textContent)) {
      return; // Skip adding generated number span
    }

    let numberStr = "";
    for (let i = minLevel; i <= level; i++) numberStr += counters[i] + ".";

    const numSpan = document.createElement("span");
    numSpan.className = "theory-heading-number";
    numSpan.textContent = numberStr + " ";
    h.insertBefore(numSpan, h.firstChild);
  });
}

function buildFloatingTOC(root) {
  let existing = document.querySelector(".theory-floating-widget");
  if (existing) existing.remove();

  const headings = root.querySelectorAll("h1, h2, h3");
  if (headings.length === 0) return;

  const widget = document.createElement("div");
  widget.className = "theory-floating-widget";
  widget.innerHTML = `
    <div id="theory-toc-popup" class="theory-toc-popup hidden">
      <div class="toc-header">목차</div>
      <div class="toc-content" id="theory-toc-content"></div>
    </div>
    <button id="theory-toc-btn" class="floating-btn" title="목차">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
    </button>
    <button id="theory-top-btn" class="floating-btn" title="맨 위로">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
    </button>
    <button id="theory-bottom-btn" class="floating-btn" title="맨 아래로">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
    </button>
  `;
  document.body.appendChild(widget);

  const tocContent = document.getElementById("theory-toc-content");
  headings.forEach((h, i) => {
    if (!h.id) h.id = "heading-" + i;
    const a = document.createElement("a");
    a.href = "#" + h.id;
    a.textContent = h.textContent;
    a.className = "theory-toc-item level-" + h.tagName.charAt(1);
    a.onclick = (e) => {
      e.preventDefault();
      const y = h.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({top: y, behavior: "smooth"});
    };
    tocContent.appendChild(a);
  });

  const tocBtn = document.getElementById("theory-toc-btn");
  const topBtn = document.getElementById("theory-top-btn");
  const bottomBtn = document.getElementById("theory-bottom-btn");
  const popup = document.getElementById("theory-toc-popup");

  tocBtn.onclick = () => popup.classList.toggle("hidden");
  document.addEventListener("click", (e) => { if (!widget.contains(e.target)) popup.classList.add("hidden"); });
  topBtn.onclick = () => window.scrollTo({top: 0, behavior: 'smooth'});
  bottomBtn.onclick = () => window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
}

function buildRoadmap(root) {
  let query = "h1, h2, h3";
  if (root.classList.contains("is-section-mode")) {
    query = "h1, h2"; // Hide h3 in section mode to avoid roadmap overload
  }
  const headings = Array.from(root.querySelectorAll(query));
  if (headings.length === 0) return;

  const container = document.getElementById("theory-roadmap-container");
  if (!container) return;
  container.innerHTML = "";

  const progressLine = document.createElement("div");
  progressLine.className = "roadmap-progress-line";
  progressLine.id = "roadmap-progress-line";
  container.appendChild(progressLine);

  headings.forEach((h, i) => {
    if (!h.id) h.id = "heading-" + i;
    const node = document.createElement("a");
    node.href = "#" + h.id;
    node.className = "roadmap-node";
    const level = parseInt(h.tagName.charAt(1));
    if (level === 3) node.style.marginLeft = "12px";

    node.title = h.textContent;

    const match = h.textContent.match(/^([\d\.]+)\s+(.*)/);
    let num = "", text = h.textContent;
    if (match) { num = match[1]; text = match[2]; }

    node.innerHTML = `
      <div class="roadmap-dot" data-num="${i + 1}"></div>
      <div class="roadmap-text">
        <span class="roadmap-num">${num}</span>
        <span class="roadmap-title-text">${text}</span>
      </div>
    `;
    node.onclick = (e) => {
      e.preventDefault();
      const y = h.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({top: y, behavior: "smooth"});
    };
    container.appendChild(node);
  });

  const toggleBtn = document.getElementById("roadmap-toggle-btn");
  const stickyContainer = document.getElementById("theory-roadmap-sticky");
  if (toggleBtn && stickyContainer && !toggleBtn.dataset.bound) {
    toggleBtn.dataset.bound = "true";
    toggleBtn.onclick = () => {
      stickyContainer.classList.toggle("is-expanded");
      const icon = toggleBtn.querySelector("path");
      icon.setAttribute("d", stickyContainer.classList.contains("is-expanded") ? "M15 18l-6-6 6-6" : "M9 18l6-6-6-6");
    };
  }
  setupRoadmapScrollSpy(headings);
}

function setupRoadmapScrollSpy(headings) {
  const nodes = document.querySelectorAll(".roadmap-node");
  const progressLine = document.getElementById("roadmap-progress-line");
  if(nodes.length === 0) return;

  const updateScroll = () => {
    let currentIndex = 0;
    const scrollY = window.scrollY;
    if (scrollY > 150) localStorage.setItem(`readPosition_${window.location.search}`, scrollY);
    else if (scrollY <= 150) localStorage.removeItem(`readPosition_${window.location.search}`);
    
    headings.forEach((h, i) => {
      const top = h.getBoundingClientRect().top + scrollY - 150;
      if (scrollY >= top) currentIndex = i;
    });

    // Bottom-of-page detection: if scrolled to within 50px of the document bottom,
    // force-activate the last heading so the final node & section are always highlighted.
    const atBottom = (window.innerHeight + scrollY) >= (document.documentElement.scrollHeight - 50);
    if (atBottom && headings.length > 0) {
      currentIndex = headings.length - 1;
    }

    nodes.forEach((node, i) => {
      node.classList.remove("is-active", "is-past");
      if (i < currentIndex) node.classList.add("is-past");
      else if (i === currentIndex) node.classList.add("is-active");
    });

    // Sync active node into view inside the roadmap sidebar
    const activeNode = nodes[currentIndex];
    if (activeNode) {
      const sticky = document.getElementById('theory-roadmap-sticky');
      if (sticky) {
        const nodeTop = activeNode.offsetTop;
        const stickyScroll = sticky.scrollTop;
        const stickyH = sticky.clientHeight;
        if (nodeTop < stickyScroll + 60 || nodeTop > stickyScroll + stickyH - 60) {
          sticky.scrollTo({ top: nodeTop - stickyH / 2, behavior: 'smooth' });
        }
      }
    }

    // Section card active/inactive dim effect
    const sectionCards = document.querySelectorAll('.theory-section-card');
    if (sectionCards.length > 0) {
      const activeHeading = headings[currentIndex];
      sectionCards.forEach(card => {
        if (card.contains(activeHeading)) {
          card.classList.add('is-active');
          card.classList.remove('is-inactive');
        } else {
          card.classList.remove('is-active');
          card.classList.add('is-inactive');
        }
      });
    }

    if (activeNode) progressLine.style.height = (activeNode.offsetTop + 7) + "px";
  };
  window.addEventListener('scroll', updateScroll);
  setTimeout(updateScroll, 100);
}

function showResumeToast(yPosition) {
  const toast = document.createElement("div");
  toast.className = "theory-resume-toast";
  toast.innerHTML = `
    <span class="resume-text">이전에 읽던 위치가 있습니다. 이어보시겠습니까?</span>
    <div class="resume-actions">
      <button class="resume-btn resume-yes">이동</button>
      <button class="resume-btn resume-no">닫기</button>
    </div>
  `;
  document.body.appendChild(toast);
  toast.querySelector(".resume-yes").onclick = () => {
    window.scrollTo({ top: yPosition, behavior: "smooth" });
    toast.classList.remove("visible"); setTimeout(() => toast.remove(), 300);
  };
  toast.querySelector(".resume-no").onclick = () => {
    toast.classList.remove("visible"); setTimeout(() => toast.remove(), 300);
  };
  setTimeout(() => toast.classList.add("visible"), 50);
}

document.addEventListener("DOMContentLoaded", initTheoryPage);
