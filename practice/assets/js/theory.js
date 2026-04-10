/**
 * StepCode - Theory Page Logic (Ultimate Integrated Version)
 * Fixes: Undefined functions, Slide rendering sequence, and Mermaid theme bugs.
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

// 3. Markdown Rendering
function renderTheoryMarkdown(target, mdText, mdPath = "") {
  const raw = stripFrontMatter(mdText);
  const md = getMdRenderer();
  if (!md) { target.textContent = raw; return; }
  
  let html = window.DOMPurify.sanitize(md.render(raw));
  target.innerHTML = replaceLangBadges(html);
  
  // Mermaid Detection
  target.querySelectorAll('code.language-mermaid').forEach(c => {
    const pre = c.closest('pre');
    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = c.textContent;
    if (pre) pre.replaceWith(div);
  });

  if (window.mermaid && target.querySelectorAll('.mermaid').length > 0) {
    setTimeout(() => {
      try { window.mermaid.init(undefined, target.querySelectorAll('.mermaid')); } catch (e) {}
    }, 200);
  }

  fixRelativeImagePaths(target, mdPath);
  enhanceLessonCallouts(target);
  enhanceCodeBlocks(target);
  enhanceTraceGridBlocks(target);
  enhanceIoBlocks(target);
  enhanceInteractiveProblems(target);
}

function fixRelativeImagePaths(root, mdPath) {
  if (!mdPath) return;
  const baseDir = mdPath.substring(0, mdPath.lastIndexOf("/"));
  root.querySelectorAll("img").forEach(img => {
    const src = img.getAttribute("src");
    if (src && (src.startsWith("./") || src.startsWith("../"))) {
      img.src = baseDir + (src.startsWith("./") ? src.slice(1) : "/" + src);
    }
  });
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
  groupContentIntoStages(root);
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
}

function renderProblemUI(container, data) {
  const type = data.type || "mcq";
  container.innerHTML = `<div class="problem-header"><span class="badge">${type.toUpperCase()}</span> <strong>실력을 확인해보세요!</strong></div>`;
  if (type === "mcq") renderMCQUI(container, data);
  else renderShortUI(container, data);
}

function renderMCQUI(container, data) {
  const wrap = document.createElement("div");
  wrap.className = "problem-options";
  (data.options || []).forEach((opt, idx) => {
    const btn = document.createElement("button");
    btn.className = "option-btn";
    btn.textContent = `${idx + 1}) ${opt}`;
    btn.onclick = () => {
      if (idx === data.answer) { btn.classList.add("is-correct"); unlockNextStage(container); }
      else { btn.classList.add("is-wrong"); setTimeout(() => btn.classList.remove("is-wrong"), 500); }
    };
    wrap.appendChild(btn);
  });
  container.appendChild(wrap);
}

function renderShortUI(container, data) {
  const wrap = document.createElement("div");
  wrap.className = "problem-input-wrap";
  const input = document.createElement("input");
  input.className = "short-answer-input";
  const btn = document.createElement("button");
  btn.className = "check-btn"; btn.textContent = "확인";
  btn.onclick = () => {
    const val = input.value.trim();
    const ok = Array.isArray(data.answer) ? data.answer.includes(val) : val === String(data.answer);
    if (ok) { container.classList.add("is-solved"); unlockNextStage(container); }
    else { input.classList.add("is-wrong"); setTimeout(() => input.classList.remove("is-wrong"), 500); }
  };
  wrap.append(input, btn); container.appendChild(wrap);
}

// 5. Marp Slide Mode
async function setupSlideMode(slidePath) {
  const toggleBtn = document.getElementById("theory-mode-toggle");
  const slideViewer = document.getElementById("theory-slide-viewer");
  const docContent = document.getElementById("theory-content");
  const marpContainer = document.getElementById("marp-container");
  if (!toggleBtn || !slideViewer || !marpContainer) return;

  if (window.mermaid) {
    window.mermaid.initialize({
      startOnLoad: false, theme: 'base', securityLevel: 'loose',
      themeVariables: {
        primaryColor: 'rgba(99, 91, 255, 0.25)', primaryTextColor: '#ffffff',
        primaryBorderColor: '#635bff', lineColor: 'rgba(255, 255, 255, 0.4)',
        fontSize: '18px', fontFamily: 'JetBrains Mono, Pretendard, sans-serif',
        nodePadding: 60
      },
      flowchart: { htmlLabels: false, useMaxWidth: false, padding: 50, curve: 'basis' }
    });
  }

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
      let css = styleMatch[1].trim().replace(/@import\s+['"](.+?)['"]/g, (m, p) => `@import "${baseDir}/${p}"`);
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
      let html = window.DOMPurify.sanitize(md.render(chunk));
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
      enterSlideMode();
    }
  } catch (e) { console.error(e); }

  function showToast(message) {
    let toast = document.getElementById("theory-toast-msg");
    if (!toast) {
      toast = document.createElement("div");
      toast.id = "theory-toast-msg";
      toast.className = "theory-toast";
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 3000);
  }

  function checkNavigationGuard() {
    const currentSlide = slides[currentIndex];
    if (currentSlide && currentSlide.dataset.locked === "true") {
      const nextBtn = document.getElementById("slide-next");
      if (nextBtn) {
        nextBtn.classList.remove("shake-error");
        void nextBtn.offsetWidth; // Reflow
        nextBtn.classList.add("shake-error");
      }
      showToast("문제를 해결해야 다음 스테이지로 넘어갈 수 있습니다.");
      return false;
    }
    return true;
  }

  function updateProgressUI() {
    const infoContainer = document.getElementById("slide-page-info");
    if (!infoContainer) return;
    
    // Check if stages exist
    let hasStages = slides.some(s => s.dataset.stage);
    if (!hasStages) {
      infoContainer.textContent = `${currentIndex + 1} / ${slides.length}`;
      return;
    }

    infoContainer.innerHTML = "";
    infoContainer.classList.add("stage-progress-wrapper");

    let currentStageNum = parseInt(slides[currentIndex].dataset.stage) || 1;
    let stages = [];
    slides.forEach((s, idx) => {
      if (s.dataset.stage && !stages.some(st => st.stage === s.dataset.stage)) {
        stages.push({ stage: s.dataset.stage, idx: idx, locked: s.dataset.locked === "true" });
      }
    });

    stages.forEach((st, i) => {
      const node = document.createElement("div");
      node.className = "stage-node";
      let stNum = parseInt(st.stage);

      if (st.locked) {
        node.classList.add("is-locked");
      } else if (stNum < currentStageNum) {
        node.classList.add("is-completed");
        node.textContent = "✓";
      } else if (stNum === currentStageNum) {
        node.classList.add("is-current");
        node.textContent = st.stage;
      } else {
        node.textContent = st.stage;
      }

      infoContainer.appendChild(node);

      if (i < stages.length - 1) {
        const line = document.createElement("div");
        line.className = "stage-line";
        if (parseInt(stages[i+1].stage) <= currentStageNum) {
          line.classList.add("is-active");
        }
        infoContainer.appendChild(line);
      }
    });
  }

  function renderSlide(idx) {
    if (!isSlideMode) return; // Wait until visible to avoid width=0
    if (idx < 0 || idx >= slides.length) return;
    currentIndex = idx;
    marpContainer.innerHTML = "";
    
    // Flexbox shrink-wrap workaround
    marpContainer.style.alignSelf = "stretch";
    marpContainer.style.margin = "0 auto";
    
    const node = slides[currentIndex].cloneNode(true);
    const sw = slideViewer.clientWidth ? slideViewer.clientWidth - 40 : 1080;
    const cw = marpContainer.clientWidth || sw; // Fallback if 0
    const scale = cw / 1280;
    
    node.style.cssText = `width:1280px;height:720px;transform:scale(${scale});transform-origin:top left;display:block;margin:0;position:absolute;top:0;left:0;`;
    marpContainer.style.height = `${720 * scale}px`;
    marpContainer.appendChild(node);
    
    // Interactive Quiz Handlers (Step 4)
    const unlockBtn = node.querySelector('.stage-unlock-btn');
    if (unlockBtn) {
      unlockBtn.onclick = () => {
        const input = node.querySelector('.stage-key-input');
        const card = node.querySelector('.theory-mini-check-card');
        if (!input || !card) return;
        
        const expected = (card.dataset.answer || "").replace(/\s+/g, "").toLowerCase();
        const given = (input.value || "").replace(/\s+/g, "").toLowerCase();
        
        if (expected === given) {
          slides[currentIndex].dataset.locked = "false"; // Unlock master slide node
          showToast("✅ 정답입니다! 다음 스테이지로 진입합니다.");
          unlockBtn.textContent = "잠금 해제 성공!";
          unlockBtn.style.background = "#10b981";
          input.disabled = true;
          setTimeout(() => renderSlide(currentIndex + 1), 800);
        } else {
          showToast("❌ 올바른 응답이 아닙니다. 코드를 지문과 비교해보세요.");
          input.classList.remove("shake-error");
          void input.offsetWidth;
          input.classList.add("shake-error");
          input.value = "";
          input.focus();
        }
      };
      
      // Submit on Enter
      const input = node.querySelector('.stage-key-input');
      if (input) {
        input.onkeydown = (e) => {
          if (e.key === "Enter") unlockBtn.onclick();
        };
      }
    }
    
    if (window.mermaid) {
      setTimeout(() => { try { window.mermaid.init(undefined, node.querySelectorAll('.mermaid')); } catch (e) {} }, 100);
    }
    updateProgressUI();
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
    window.scrollTo(0, 0); setTimeout(() => { renderSlide(currentIndex); }, 50);
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
  document.getElementById("slide-next").onclick = () => {
    if (checkNavigationGuard()) renderSlide(currentIndex + 1);
  };
  document.addEventListener("keydown", (e) => {
    if (!isSlideMode) return;
    if (e.key === "ArrowLeft") renderSlide(currentIndex - 1);
    if (e.key === "ArrowRight") {
      if (checkNavigationGuard()) renderSlide(currentIndex + 1);
    }
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
    if (pre) { pre.classList.add("line-numbers", "theory-code"); if (window.Prism) window.Prism.highlightElement(c); }
  });
}
function enhanceTraceGridBlocks(root) {
  root.querySelectorAll("pre > code").forEach(codeEl => {
    const classes = Array.from(codeEl.classList || []);
    if (classes.some(cls => ["language-tracegrid", "language-trace-grid"].includes(cls))) {
      // TraceGrid logic would go here if needed
    }
  });
}
function enhanceIoBlocks(root) {}

// 7. Page Initialization
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
    const mdText = await res.text();
    renderTheoryMarkdown(contentEl, mdText, entry.mdPath);
    if (entry.slidePath) setupSlideMode(entry.slidePath);
  } catch (e) { console.error("Initialization failed:", e); }
}

document.addEventListener("DOMContentLoaded", initTheoryPage);
