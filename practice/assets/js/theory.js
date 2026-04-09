/**
 * StepCode - Theory Page Logic (Integrated Version)
 * All-in-one script for Markdown rendering, Interactive Problems, and Marp Slides.
 */

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
  return html.replace(/\{lang:([^}]+)\}/g, (match, lang) => {
    const l = lang.toLowerCase();
    const map = { "python": "Python", "c": "C", "java": "Java", "csharp": "C#" };
    const label = map[l] || lang.toUpperCase();
    return `<span class="theory-lang-badge theory-lang-badge--${l}">${label}</span>`;
  });
}

const TOGGLE_LANGS = new Set(["python", "c", "java", "csharp"]);

function renderTheoryMarkdown(target, mdText, mdPath = "") {
  const raw = stripFrontMatter(mdText);
  const md = getMdRenderer();
  if (!md) { target.textContent = raw; return; }
  let html = window.DOMPurify.sanitize(md.render(raw));
  target.innerHTML = replaceLangBadges(html);
  
  target.querySelectorAll('code.language-mermaid').forEach(c => {
    const pre = c.closest('pre');
    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = c.textContent;
    if (pre) pre.replaceWith(div);
  });
  if (window.mermaid) {
    setTimeout(() => {
      try { window.mermaid.init(undefined, target.querySelectorAll('.mermaid')); } catch (e) { console.warn(e); }
    }, 100);
  }
  fixRelativeImagePaths(target, mdPath);
  enhanceLessonCallouts(target);
  applyDataImageFallbacks(target);
  enhanceTraceGridBlocks(target);
  enhanceIoBlocks(target);
  enhanceCodeBlocks(target);
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

// --- Interactive Problems & Stage Gating ---
async function enhanceInteractiveProblems(root) {
  const problemTags = Array.from(root.querySelectorAll("p")).filter(p => /\[문제 ID:\s*([\w-]+)\]/.test(p.textContent));
  if (!problemTags.length) return;

  const setId = new URLSearchParams(location.search).get("set");
  let currentSet = null;
  if (setId) {
    try { currentSet = await ProblemService.loadSet(setId); } 
    catch (e) { console.warn(e); }
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

// --- Marp Slide Mode ---
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
    const fixedPath = slidePath.startsWith("./") ? slidePath.slice(2) : slidePath;
    const res = await fetch(fixedPath);
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
    slides = slideChunks.map(chunk => {
      const sec = document.createElement("section");
      const m = chunk.match(/<!--\s*_class:\s*([\w-]+)\s*-->/);
      if (m) sec.className = m[1];
      let html = window.DOMPurify.sanitize(md.render(chunk));
      sec.innerHTML = replaceLangBadges(html);
      
      sec.querySelectorAll('code.language-mermaid').forEach(c => {
        const pre = c.closest('pre');
        const div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = c.textContent;
        if (pre) pre.replaceWith(div);
      });
      
      fixRelativeImagePaths(sec, slidePath);
      enhanceCodeBlocks(sec);
      return sec;
    });

    if (slides.length > 0) {
      toggleBtn.hidden = false;
      renderSlide(0);
      enterSlideMode();
      if (window.mermaid) {
        setTimeout(() => {
          try { window.mermaid.init(undefined, document.querySelectorAll('#marp-container .mermaid')); } catch (e) { console.warn(e); }
        }, 100);
      }
    }
  } catch (e) { console.error(e); }

  function renderSlide(idx) {
    if (idx < 0 || idx >= slides.length) return;
    currentIndex = idx;
    marpContainer.innerHTML = "";
    const node = slides[currentIndex].cloneNode(true);
    
    marpContainer.style.height = `${marpContainer.clientWidth * (9 / 16)}px`;
    const scale = marpContainer.clientWidth / 1280;
    
    node.style.cssText = `width:1280px;height:720px;transform:scale(${scale});transform-origin:top left;display:block;margin:0;position:absolute;top:0;left:0;`;
    marpContainer.appendChild(node);
    document.getElementById("slide-page-info").textContent = `${currentIndex + 1} / ${slides.length}`;
  }

  window.addEventListener("resize", () => {
    if (isSlideMode) renderSlide(currentIndex);
  });

  function enterSlideMode() {
    isSlideMode = true;
    const layout = document.querySelector(".theory-layout");
    const sidebar = document.querySelector(".theory-side");
    const fabStack = document.querySelector(".theory-fab-stack");
    if (layout) { layout.style.display = "block"; layout.style.padding = "0"; }
    if (sidebar) sidebar.style.display = "none";
    if (fabStack) fabStack.style.display = "none";
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
    const fabStack = document.querySelector(".theory-fab-stack");
    if (layout) { layout.style.display = "grid"; layout.style.padding = ""; }
    if (sidebar) sidebar.style.display = "block";
    if (fabStack) fabStack.style.display = "flex";
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

// --- Essential Registry & Title Helpers ---
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

// --- Callouts & Prism ---
function enhanceLessonCallouts(root) {
  root.querySelectorAll("blockquote").forEach(q => {
    const m = q.textContent.match(/\[!(\w+)\]/);
    if (m) q.classList.add("lesson-callout", `lesson-callout--${m[1].toLowerCase()}`);
  });
}
function applyDataImageFallbacks(root) {}
function enhanceCodeBlocks(root) {
  root.querySelectorAll("pre > code").forEach(c => {
    const pre = c.closest("pre");
    if (pre) { pre.classList.add("line-numbers", "theory-code"); if (window.Prism) window.Prism.highlightElement(c); }
  });
}

function normalizeCodeLang(s) { return String(s||"").trim().toLowerCase(); }
function normalizeLanguageList(raw) {
  return String(raw || "").split(",").map((s) => normalizeCodeLang(s.trim())).filter(Boolean);
}
function detectLangFromCode(codeEl) {
  const classes = Array.from(codeEl.classList || []);
  for (const cls of classes) {
    if (cls.startsWith("language-")) return normalizeCodeLang(cls.replace("language-", ""));
  }
  return "";
}

function parseIoFenceText(rawText) {
  const text = String(rawText || "").replace(/\r\n?/g, "\n");
  const lines = text.split("\n");
  let mode = "";
  const input = []; const output = [];
  lines.forEach((line) => {
    if (/^\s*(input|in|입력)\s*:\s*$/i.test(line)) { mode = "input"; return; }
    if (/^\s*(output|out|출력)\s*:\s*$/i.test(line)) { mode = "output"; return; }
    if (mode === "input") input.push(line);
    if (mode === "output") output.push(line);
  });
  return { input: input.join("\n").trim(), output: output.join("\n").trim() };
}

function buildIoExampleBlock(io) {
  const wrap = document.createElement("div"); wrap.className = "theory-io";
  const title = document.createElement("div"); title.className = "theory-io-title"; title.textContent = "예상 입력/출력"; wrap.appendChild(title);
  const grid = document.createElement("div"); grid.className = "theory-io-grid";
  const inBox = document.createElement("div"); inBox.className = "theory-io-box";
  const inLabel = document.createElement("div"); inLabel.className = "theory-io-label"; inLabel.textContent = "입력";
  const inPre = document.createElement("pre"); inPre.className = "theory-io-pre"; inPre.textContent = io.input || "(입력 없음)";
  inBox.append(inLabel, inPre);
  const outBox = document.createElement("div"); outBox.className = "theory-io-box";
  const outLabel = document.createElement("div"); outLabel.className = "theory-io-label"; outLabel.textContent = "출력";
  const outPre = document.createElement("pre"); outPre.className = "theory-io-pre"; outPre.textContent = io.output || "(출력 없음)";
  outBox.append(outLabel, outPre);
  grid.append(inBox, outBox); wrap.appendChild(grid);
  return wrap;
}

function enhanceIoBlocks(contentEl) {
  const candidates = contentEl.querySelectorAll("pre > code");
  candidates.forEach(codeEl => {
    const lang = detectLangFromCode(codeEl);
    if (!["io", "inout", "exampleio"].includes(lang)) return;
    const pre = codeEl.closest("pre"); if (!pre) return;
    pre.replaceWith(buildIoExampleBlock(parseIoFenceText(codeEl.textContent || "")));
  });
}

function parseTraceGridFenceText(rawText) {
  const lines = String(rawText || "").replace(/\r\n?/g, "\n").split("\n");
  const conf = { title: "", langs: [], columns: [], rows: [] };
  let inRows = false;
  lines.forEach((lineRaw) => {
    const line = lineRaw.trim(); if (!line) return;
    if (!inRows) {
      const kv = line.match(/^([a-zA-Z_]+)\s*:\s*(.*)$/);
      if (kv) {
        const key = kv[1].toLowerCase(), value = kv[2].trim();
        if (key === "title") conf.title = value;
        if (key === "lang" || key === "langs") conf.langs = normalizeLanguageList(value);
        if (key === "columns" || key === "cols") conf.columns = value.split(",").map(v => v.trim()).filter(Boolean);
        if (key === "rows") inRows = true;
        return;
      }
    }
    if (inRows) {
      const row = line.split("|").map((v) => v.trim()).filter((v, idx, arr) => !(idx === 0 && arr.length > 1 && v === ""));
      if (row.length) conf.rows.push(row);
    }
  });
  if (!conf.columns.length || !conf.rows.length) return null;
  return conf;
}

function buildTraceGridBlock(conf) {
  const wrap = document.createElement("div"); wrap.className = "theory-trace-grid";
  if (conf.langs.length) wrap.dataset.langs = conf.langs.join(",");
  if (conf.title) {
    const title = document.createElement("div"); title.className = "theory-trace-title"; title.textContent = conf.title; wrap.appendChild(title);
  }
  const tableWrap = document.createElement("div"); tableWrap.className = "theory-trace-table-wrap";
  const table = document.createElement("table"); table.className = "theory-trace-table";
  const thead = document.createElement("thead"); const trh = document.createElement("tr");
  conf.columns.forEach((col) => { const th = document.createElement("th"); th.textContent = col; trh.appendChild(th); });
  thead.appendChild(trh); table.appendChild(thead);
  const tbody = document.createElement("tbody");
  conf.rows.forEach((row) => {
    const tr = document.createElement("tr");
    conf.columns.forEach((_, i) => { const td = document.createElement("td"); td.textContent = row[i] ?? ""; tr.appendChild(td); });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody); tableWrap.appendChild(table); wrap.appendChild(tableWrap);
  return wrap;
}

function enhanceTraceGridBlocks(contentEl) {
  const candidates = contentEl.querySelectorAll("pre > code");
  candidates.forEach(codeEl => {
    const lang = detectLangFromCode(codeEl);
    if (!["tracegrid", "trace-grid", "gridtrace"].includes(lang)) return;
    const pre = codeEl.closest("pre"); if (!pre) return;
    const conf = parseTraceGridFenceText(codeEl.textContent || "");
    if (!conf) return;
    pre.replaceWith(buildTraceGridBlock(conf));
  });
}

// --- Page Initialization ---
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
  } catch (e) { console.error(e); }
}

document.addEventListener("DOMContentLoaded", initTheoryPage);
