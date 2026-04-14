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
  autoNumberHeadings(target);
  buildFloatingTOC(target);
  buildRoadmap(target);
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

    const savedPos = localStorage.getItem(`readPosition_${location.search}`);
    if (savedPos && parseInt(savedPos) > 150) {
      setTimeout(() => showResumeToast(parseInt(savedPos)), 500);
    }
  } catch (e) { console.error("Initialization failed:", e); }
}

// 8. Auto Numbering & Floating Navigation
function autoNumberHeadings(root) {
  const headings = Array.from(root.querySelectorAll("h1, h2, h3, h4, h5, h6"));
  if (headings.length === 0) return;

  // Find minimum level (root level)
  let minLevel = 6;
  headings.forEach(h => {
    const level = parseInt(h.tagName.charAt(1));
    if (level < minLevel) minLevel = level;
  });

  const counters = [0, 0, 0, 0, 0, 0, 0];

  headings.forEach(h => {
    // Skip if it sits inside interactive elements or has no real text
    if (h.closest('.interactive-problem-card') || h.closest('.theory-mini-check-card') || h.closest('.theory-toc-popup')) return;
    if (!h.textContent.trim()) return;

    const level = parseInt(h.tagName.charAt(1));
    
    // Ignore levels greater than 6 just in case
    if(level > 6 || level < 1) return;

    counters[level]++;
    // Reset deeper levels
    for (let i = level + 1; i <= 6; i++) {
        counters[i] = 0;
    }

    let numberStr = "";
    for (let i = minLevel; i <= level; i++) {
        numberStr += counters[i] + ".";
    }

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

  tocBtn.onclick = () => {
    popup.classList.toggle("hidden");
  };
  
  // Close popup when clicking outside
  document.addEventListener("click", (e) => {
    if (!widget.contains(e.target)) {
      popup.classList.add("hidden");
    }
  });

  topBtn.onclick = () => window.scrollTo({top: 0, behavior: 'smooth'});
  bottomBtn.onclick = () => window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
}

function buildRoadmap(root) {
  const headings = Array.from(root.querySelectorAll("h1, h2, h3"));
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
    node.dataset.targetId = h.id;
    
    // Add visual hierarchy offset for level 3
    const level = parseInt(h.tagName.charAt(1));
    if (level === 3) {
      node.style.marginLeft = "12px";
    }

    const match = h.textContent.match(/^([\d\.]+)\s+(.*)/);
    let num = "", text = h.textContent;
    if (match) {
      num = match[1];
      text = match[2];
    }

    node.innerHTML = `
      <div class="roadmap-dot"></div>
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
      if (stickyContainer.classList.contains("is-expanded")) {
        icon.setAttribute("d", "M15 18l-6-6 6-6"); // Left chevron
      } else {
        icon.setAttribute("d", "M9 18l6-6-6-6"); // Right chevron
      }
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
    
    if (scrollY > 150) {
      localStorage.setItem(`readPosition_${window.location.search}`, scrollY);
    } else if (scrollY <= 150) {
      localStorage.removeItem(`readPosition_${window.location.search}`);
    }
    
    headings.forEach((h, i) => {
      const top = h.getBoundingClientRect().top + scrollY - 150;
      if (scrollY >= top) {
        currentIndex = i;
      }
    });

    nodes.forEach((node, i) => {
      node.classList.remove("is-active", "is-past");
      if (i < currentIndex) {
        node.classList.add("is-past");
      } else if (i === currentIndex) {
        node.classList.add("is-active");
      }
    });

    const activeNode = nodes[currentIndex];
    if (activeNode) {
      const height = activeNode.offsetTop + 7;
      progressLine.style.height = height + "px";
    }
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

  const autoHide = setTimeout(() => {
    if (toast.parentNode) {
      toast.classList.remove("visible");
      setTimeout(() => toast.remove(), 300);
    }
  }, 8000);

  toast.querySelector(".resume-yes").onclick = () => {
    window.scrollTo({ top: yPosition, behavior: "smooth" });
    toast.classList.remove("visible");
    setTimeout(() => toast.remove(), 300);
    clearTimeout(autoHide);
  };
  toast.querySelector(".resume-no").onclick = () => {
    toast.classList.remove("visible");
    setTimeout(() => toast.remove(), 300);
    clearTimeout(autoHide);
  };
  
  setTimeout(() => toast.classList.add("visible"), 50);
}

document.addEventListener("DOMContentLoaded", initTheoryPage);
