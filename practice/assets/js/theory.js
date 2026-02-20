function getMdRenderer() {
  if (!window.markdownit || !window.DOMPurify) return null;
  return window.markdownit({
    html: true,
    linkify: true,
    breaks: true,
  });
}

const TOGGLE_LANGS = new Set(["python", "c", "java", "csharp"]);

function renderTheoryMarkdown(target, mdText) {
  const raw = String(mdText || "");
  const md = getMdRenderer();
  if (!md) {
    target.textContent = raw;
    return;
  }
  const safe = window.DOMPurify.sanitize(md.render(raw));
  target.innerHTML = safe;
  applyDataImageFallbacks(target);
}

function resolveDataPathSuffix(src) {
  const s = String(src || "").trim();
  if (s.startsWith("./data/")) return s.slice("./data/".length);
  if (s.startsWith("/data/")) return s.slice("/data/".length);
  if (s.startsWith("/practice/data/")) return s.slice("/practice/data/".length);
  if (s.startsWith("data/")) return s.slice("data/".length);
  return "";
}

function buildDataPathCandidates(src) {
  const suffix = resolveDataPathSuffix(src);
  if (!suffix) return [];
  return [`./data/${suffix}`, `/data/${suffix}`, `/practice/data/${suffix}`];
}

function applyDataImageFallbacks(root) {
  const imgs = root.querySelectorAll("img[src]");
  imgs.forEach((img) => {
    const original = String(img.getAttribute("src") || "").trim();
    const candidates = buildDataPathCandidates(original).filter((v) => v !== original);
    if (!candidates.length) return;

    const tried = new Set([original]);
    let idx = 0;
    const onError = () => {
      while (idx < candidates.length) {
        const next = candidates[idx++];
        if (tried.has(next)) continue;
        tried.add(next);
        img.setAttribute("src", next);
        return;
      }
      img.removeEventListener("error", onError);
    };
    img.addEventListener("error", onError);
  });
}

function normalizeCodeLang(raw) {
  const v = String(raw || "").toLowerCase();
  if (v === "py" || v === "python") return "python";
  if (v === "c" || v === "c99" || v === "c11") return "c";
  if (v === "java") return "java";
  if (v === "cs" || v === "c#" || v === "csharp") return "csharp";
  return v;
}

function isToggleLanguage(lang) {
  return TOGGLE_LANGS.has(lang);
}

function normalizeLanguageList(raw) {
  return String(raw || "")
    .split(",")
    .map((s) => normalizeCodeLang(s.trim()))
    .filter(Boolean);
}

function titleLang(lang) {
  if (lang === "python") return "Python";
  if (lang === "c") return "C";
  if (lang === "java") return "Java";
  if (lang === "csharp") return "C#";
  return lang.toUpperCase();
}

function detectLangFromCode(codeEl) {
  const classes = Array.from(codeEl.classList || []);
  for (const cls of classes) {
    if (!cls.startsWith("language-")) continue;
    return normalizeCodeLang(cls.replace("language-", ""));
  }
  return "";
}

function parseIoFenceText(rawText) {
  const text = String(rawText || "").replace(/\r\n?/g, "\n");
  const lines = text.split("\n");
  let mode = "";
  const input = [];
  const output = [];

  lines.forEach((line) => {
    if (/^\s*(input|in|입력)\s*:\s*$/i.test(line)) {
      mode = "input";
      return;
    }
    if (/^\s*(output|out|출력)\s*:\s*$/i.test(line)) {
      mode = "output";
      return;
    }
    if (mode === "input") input.push(line);
    if (mode === "output") output.push(line);
  });

  return {
    input: input.join("\n").trim(),
    output: output.join("\n").trim(),
  };
}

function parseTraceGridFenceText(rawText) {
  const lines = String(rawText || "").replace(/\r\n?/g, "\n").split("\n");
  const conf = {
    title: "",
    langs: [],
    columns: [],
    rows: [],
  };

  let inRows = false;
  lines.forEach((lineRaw) => {
    const line = lineRaw.trim();
    if (!line) return;

    if (!inRows) {
      const kv = line.match(/^([a-zA-Z_]+)\s*:\s*(.*)$/);
      if (kv) {
        const key = kv[1].toLowerCase();
        const value = kv[2].trim();
        if (key === "title") conf.title = value;
        if (key === "lang" || key === "langs") conf.langs = normalizeLanguageList(value);
        if (key === "columns" || key === "cols") {
          conf.columns = value
            .split(",")
            .map((v) => v.trim())
            .filter(Boolean);
        }
        if (key === "rows") inRows = true;
        return;
      }
    }

    if (inRows) {
      const row = line
        .split("|")
        .map((v) => v.trim())
        .filter((v, idx, arr) => !(idx === 0 && arr.length > 1 && v === ""));
      if (row.length) conf.rows.push(row);
    }
  });

  if (!conf.columns.length || !conf.rows.length) return null;
  return conf;
}

function buildTraceGridBlock(conf) {
  const wrap = document.createElement("div");
  wrap.className = "theory-trace-grid";
  wrap.dataset.langScope = "trace";
  if (conf.langs.length) wrap.dataset.langs = conf.langs.join(",");

  if (conf.title) {
    const title = document.createElement("div");
    title.className = "theory-trace-title";
    title.textContent = conf.title;
    wrap.appendChild(title);
  }

  const tableWrap = document.createElement("div");
  tableWrap.className = "theory-trace-table-wrap";

  const table = document.createElement("table");
  table.className = "theory-trace-table";

  const thead = document.createElement("thead");
  const trh = document.createElement("tr");
  conf.columns.forEach((col) => {
    const th = document.createElement("th");
    th.textContent = col;
    trh.appendChild(th);
  });
  thead.appendChild(trh);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  conf.rows.forEach((row) => {
    const tr = document.createElement("tr");
    conf.columns.forEach((_, i) => {
      const td = document.createElement("td");
      td.textContent = row[i] ?? "";
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  tableWrap.appendChild(table);
  wrap.appendChild(tableWrap);
  return wrap;
}

function buildIoExampleBlock(io) {
  const wrap = document.createElement("div");
  wrap.className = "theory-io";

  const title = document.createElement("div");
  title.className = "theory-io-title";
  title.textContent = "예상 입력/출력";
  wrap.appendChild(title);

  const grid = document.createElement("div");
  grid.className = "theory-io-grid";

  const inBox = document.createElement("div");
  inBox.className = "theory-io-box";
  const inLabel = document.createElement("div");
  inLabel.className = "theory-io-label";
  inLabel.textContent = "입력";
  const inPre = document.createElement("pre");
  inPre.className = "theory-io-pre";
  inPre.textContent = io.input || "(입력 없음)";
  inBox.append(inLabel, inPre);

  const outBox = document.createElement("div");
  outBox.className = "theory-io-box";
  const outLabel = document.createElement("div");
  outLabel.className = "theory-io-label";
  outLabel.textContent = "출력";
  const outPre = document.createElement("pre");
  outPre.className = "theory-io-pre";
  outPre.textContent = io.output || "(출력 없음)";
  outBox.append(outLabel, outPre);

  grid.append(inBox, outBox);
  wrap.appendChild(grid);
  return wrap;
}

function enhanceIoBlocks(contentEl) {
  const candidates = contentEl.querySelectorAll("pre > code");
  candidates.forEach((codeEl) => {
    const lang = detectLangFromCode(codeEl);
    if (!["io", "inout", "exampleio"].includes(lang)) return;

    const pre = codeEl.closest("pre");
    if (!pre) return;
    const io = parseIoFenceText(codeEl.textContent || "");
    const ioBlock = buildIoExampleBlock(io);
    pre.replaceWith(ioBlock);
  });
}

function enhanceTraceGridBlocks(contentEl) {
  const candidates = contentEl.querySelectorAll("pre > code");
  candidates.forEach((codeEl) => {
    const lang = detectLangFromCode(codeEl);
    if (!["tracegrid", "trace-grid", "gridtrace"].includes(lang)) return;

    const pre = codeEl.closest("pre");
    if (!pre) return;
    const conf = parseTraceGridFenceText(codeEl.textContent || "");
    if (!conf) return;
    const grid = buildTraceGridBlock(conf);
    pre.replaceWith(grid);
  });
}

function enhanceMarkdownTables(contentEl) {
  const headingEls = Array.from(contentEl.querySelectorAll("h1, h2, h3, h4, h5, h6"));

  function resolveTableTitle(table) {
    const caption = table.querySelector("caption");
    if (caption && caption.textContent.trim()) {
      const text = caption.textContent.trim();
      caption.remove();
      return text;
    }

    let lastHeading = "";
    headingEls.forEach((h) => {
      const rel = h.compareDocumentPosition(table);
      if (rel & Node.DOCUMENT_POSITION_FOLLOWING) {
        lastHeading = (h.textContent || "").trim();
      }
    });
    if (!lastHeading) return "표 요약";
    return `표 요약. ${lastHeading}`;
  }

  const tables = contentEl.querySelectorAll("table");
  tables.forEach((table) => {
    if (table.classList.contains("theory-trace-table")) return;
    if (table.closest(".theory-trace-grid")) return;
    if (table.closest(".theory-md-table-wrap")) return;
    if (!table.parentElement) return;

    const grid = document.createElement("div");
    grid.className = "theory-trace-grid theory-md-table-grid";

    const title = document.createElement("div");
    title.className = "theory-trace-title theory-md-table-title";
    title.textContent = resolveTableTitle(table);

    const wrap = document.createElement("div");
    wrap.className = "theory-trace-table-wrap theory-md-table-wrap";

    table.classList.add("theory-trace-table", "theory-md-table");
    table.parentElement.insertBefore(grid, table);
    grid.appendChild(title);
    grid.appendChild(wrap);
    wrap.appendChild(table);
  });
}

function enhanceMiniCheckSection(contentEl) {
  const h2List = Array.from(contentEl.querySelectorAll("h2"));
  const start = h2List.find((h2) => /미니\s*체크\s*문제/.test(h2.textContent || ""));
  if (!start) return;

  start.classList.add("theory-mini-check-title");

  let cursor = start.nextElementSibling;
  let activeCard = null;

  while (cursor && cursor.tagName !== "H2") {
    const next = cursor.nextElementSibling;

    const isQuestionHeader =
      cursor.tagName === "H3" && /^Q\s*\d+/i.test((cursor.textContent || "").trim());

    if (isQuestionHeader) {
      activeCard = document.createElement("section");
      activeCard.className = "theory-mini-check-card";
      cursor.parentNode.insertBefore(activeCard, cursor);
      activeCard.appendChild(cursor);
    } else if (activeCard) {
      activeCard.appendChild(cursor);
    }

    cursor = next;
  }
}

function mapPrismLanguage(lang) {
  if (lang === "python") return "python";
  if (lang === "c") return "c";
  if (lang === "java") return "java";
  if (lang === "csharp") return "csharp";
  return "";
}

function enhanceCodeBlocks(contentEl) {
  const codeBlocks = contentEl.querySelectorAll("pre > code");
  codeBlocks.forEach((codeEl) => {
    const lang = detectLangFromCode(codeEl);
    const pre = codeEl.closest("pre");
    if (!pre) return;

    pre.classList.add("line-numbers");
    pre.classList.add("theory-code");

    const prismLang = mapPrismLanguage(lang);
    if (prismLang) {
      codeEl.className = `language-${prismLang}`;
    }
  });

  if (window.Prism && typeof window.Prism.highlightAllUnder === "function") {
    window.Prism.highlightAllUnder(contentEl);
  }
}

function isExampleHeaderBlock(el) {
  if (!el || el.tagName !== "P") return false;
  const strong = el.querySelector("strong:only-child");
  if (!strong) return false;
  const txt = String(strong.textContent || "").trim();
  return /예시/.test(txt);
}

function enhanceExampleBlocks(contentEl) {
  const containers = [contentEl, ...Array.from(contentEl.querySelectorAll(".theory-section-block"))];
  containers.forEach((root) => {
    const nodes = Array.from(root.children || []);
    if (!nodes.length) return;

    let i = 0;
    while (i < nodes.length) {
      const cur = nodes[i];
      if (!isExampleHeaderBlock(cur)) {
        i += 1;
        continue;
      }

      const wrap = document.createElement("section");
      wrap.className = "theory-example-block";
      cur.parentNode.insertBefore(wrap, cur);
      wrap.appendChild(cur);

      while (true) {
        const next = wrap.nextElementSibling;
        if (!next) break;
        if (isExampleHeaderBlock(next)) break;
        if (/^H[1-6]$/.test(next.tagName)) break;
        wrap.appendChild(next);
      }

      i += 1;
    }
  });
}

function attachTrailingExampleBlocks(contentEl) {
  const cards = contentEl.querySelectorAll(".theory-example-block");
  cards.forEach((card) => {
    while (true) {
      const next = card.nextElementSibling;
      if (!next) break;
      if (
        next.classList.contains("theory-io") ||
        next.classList.contains("theory-trace-grid")
      ) {
        card.appendChild(next);
        continue;
      }
      break;
    }
  });
}

function annotateLanguageTextBlocks(contentEl) {
  const blocks = contentEl.querySelectorAll(
    "p, li, blockquote, h1, h2, h3, h4, h5, h6"
  );

  blocks.forEach((el) => {
    const html = el.innerHTML || "";
    const m = html.match(/^\s*\{lang:([^}]+)\}\s*/i);
    if (!m) return;

    const langs = normalizeLanguageList(m[1]);
    if (!langs.length) return;

    el.dataset.langs = langs.join(",");
    el.dataset.langScope = "text";
    el.innerHTML = html.replace(/^\s*\{lang:[^}]+\}\s*/i, "");
  });
}

function applyLanguageFilter(contentEl, selected) {
  const blocks = contentEl.querySelectorAll("pre[data-code-lang]");
  blocks.forEach((pre) => {
    const lang = pre.dataset.codeLang || "";
    const visible = selected === "all" || lang === selected;
    pre.style.display = visible ? "" : "none";
    if (pre.previousElementSibling?.classList?.contains("theory-code-label")) {
      pre.previousElementSibling.style.display = visible ? "inline-flex" : "none";
    }
  });

  const textBlocks = contentEl.querySelectorAll("[data-lang-scope='text'][data-langs]");
  textBlocks.forEach((el) => {
    const langs = normalizeLanguageList(el.dataset.langs || "");
    const visible = selected === "all" || langs.includes(selected);
    el.style.display = visible ? "" : "none";
  });

  const traceBlocks = contentEl.querySelectorAll("[data-lang-scope='trace'][data-langs]");
  traceBlocks.forEach((el) => {
    const langs = normalizeLanguageList(el.dataset.langs || "");
    const visible = selected === "all" || langs.includes(selected);
    el.style.display = visible ? "" : "none";
  });
}

function setupLanguageToggle(contentEl, preferredLangRaw) {
  const toggleEl = document.getElementById("theory-lang-toggle");
  if (!toggleEl) return;

  annotateLanguageTextBlocks(contentEl);

  const codeBlocks = Array.from(contentEl.querySelectorAll("pre > code"));
  const langSet = new Set();

  codeBlocks.forEach((code) => {
    const lang = detectLangFromCode(code);
    if (!isToggleLanguage(lang)) return;
    const pre = code.closest("pre");
    if (!pre) return;
    pre.dataset.codeLang = lang;
    langSet.add(lang);

    const badge = document.createElement("span");
    badge.className = "theory-code-label";
    badge.textContent = titleLang(lang);
    pre.parentNode.insertBefore(badge, pre);
  });

  contentEl
    .querySelectorAll("[data-lang-scope='text'][data-langs]")
    .forEach((el) =>
      normalizeLanguageList(el.dataset.langs || "").forEach((lang) =>
        langSet.add(lang)
      )
    );
  contentEl
    .querySelectorAll("[data-lang-scope='trace'][data-langs]")
    .forEach((el) =>
      normalizeLanguageList(el.dataset.langs || "").forEach((lang) =>
        langSet.add(lang)
      )
    );

  const langs = Array.from(langSet);

  if (langs.length <= 1) {
    toggleEl.hidden = true;
    return;
  }

  const preferredLang = normalizeCodeLang(preferredLangRaw);
  const selectedByDefault = langs.includes(preferredLang) ? preferredLang : "all";

  toggleEl.hidden = false;
  toggleEl.innerHTML = "";

  const label = document.createElement("span");
  label.className = "theory-lang-label";
  label.textContent = "언어 예시";
  toggleEl.appendChild(label);

  const ordered = ["python", "c", "java", "csharp"]
    .filter((lang) => langs.includes(lang))
    .concat(
      langs.filter((lang) => !["python", "c", "java", "csharp"].includes(lang))
    );

  const options = ["all", ...ordered];
  options.forEach((lang) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theory-lang-btn";
    btn.dataset.lang = lang;
    btn.textContent = lang === "all" ? "전체" : titleLang(lang);
    if (lang === selectedByDefault) btn.classList.add("is-active");
    btn.addEventListener("click", () => {
      toggleEl
        .querySelectorAll(".theory-lang-btn")
        .forEach((it) => it.classList.toggle("is-active", it === btn));
      applyLanguageFilter(contentEl, lang);
    });
    toggleEl.appendChild(btn);
  });

  applyLanguageFilter(contentEl, selectedByDefault);
}

function detectAudienceFromHeadingText(text) {
  const raw = String(text || "");
  if (/\bCOMMON\b/i.test(raw) || /공통/.test(raw)) return "common";
  if (/\bELEMENTARY\b/i.test(raw) || /초등/.test(raw)) return "elementary";
  if (/\bMIDDLE\b/i.test(raw) || /중등/.test(raw)) return "middle";
  if (/\bHIGH\b/i.test(raw) || /고등/.test(raw)) return "high";
  return "";
}

function detectViewFromHeadingText(text) {
  const m = String(text || "").match(/\{view:(student|teacher)\}/i);
  return m ? m[1].toLowerCase() : "";
}

function cleanHeadingMarkers(el) {
  if (!el) return;
  const next = String(el.textContent || "")
    .replace(/\{view:(student|teacher)\}/gi, "")
    .replace(/\s{2,}/g, " ")
    .trim();
  el.textContent = next;
}

function groupSectionBlocks(contentEl) {
  const children = Array.from(contentEl.children || []);
  if (!children.length) return false;

  const h2Markers = [];
  children.forEach((el, idx) => {
    if (!el || el.tagName !== "H2") return;
    h2Markers.push({ idx });
  });
  if (!h2Markers.length) return false;

  const frag = document.createDocumentFragment();
  let cursor = 0;
  for (let i = 0; i < h2Markers.length; i += 1) {
    const m = h2Markers[i];
    const nextIdx = i + 1 < h2Markers.length ? h2Markers[i + 1].idx : children.length;
    const heading = children[m.idx];
    const aud = detectAudienceFromHeadingText(heading.textContent || "");
    const view = detectViewFromHeadingText(heading.textContent || "");

    while (cursor < m.idx) {
      frag.appendChild(children[cursor]);
      cursor += 1;
    }

    cleanHeadingMarkers(heading);

    const wrap = document.createElement("section");
    wrap.className = "theory-section-block";
    if (aud) wrap.dataset.audience = aud;
    if (view) wrap.dataset.view = view;
    for (let j = m.idx; j < nextIdx; j += 1) {
      wrap.appendChild(children[j]);
    }
    cursor = nextIdx;
    frag.appendChild(wrap);
  }

  while (cursor < children.length) {
    frag.appendChild(children[cursor]);
    cursor += 1;
  }

  contentEl.innerHTML = "";
  contentEl.appendChild(frag);
  return true;
}

function applyAudienceFilter(contentEl, selected) {
  const blocks = contentEl.querySelectorAll(".theory-section-block[data-audience]");
  blocks.forEach((block) => {
    const aud = block.dataset.audience || "";
    let visible = true;
    if (selected === "all") visible = true;
    else if (aud === "common") visible = true;
    else visible = aud === selected;
    block.style.display = visible ? "" : "none";
  });
}

function applyViewFilter(contentEl, selected) {
  const blocks = contentEl.querySelectorAll(".theory-section-block[data-view]");
  blocks.forEach((block) => {
    const view = block.dataset.view || "";
    let visible = true;
    if (selected === "all") visible = true;
    else visible = view === selected;
    block.style.display = visible ? "" : "none";
  });
}

function guessAudienceFromSet(setIdInQuery, setMap) {
  const sid = String(setIdInQuery || "").toLowerCase();
  if (/contest_py_elem_/.test(sid)) return "elementary";
  if (/contest_py_mid_/.test(sid)) return "middle";
  if (/contest_py_high_/.test(sid)) return "high";

  const title = String(setMap?.[setIdInQuery]?.title || "");
  if (title.includes("초등")) return "elementary";
  if (title.includes("중등")) return "middle";
  if (title.includes("고등")) return "high";
  return "all";
}

function syncAudienceParam(selected) {
  try {
    const url = new URL(location.href);
    if (selected === "all") url.searchParams.delete("audience");
    else url.searchParams.set("audience", selected);
    history.replaceState(null, "", url.toString());
  } catch (_) {}
}

function syncViewParam(selected) {
  try {
    const url = new URL(location.href);
    if (selected === "all") url.searchParams.delete("view");
    else url.searchParams.set("view", selected);
    history.replaceState(null, "", url.toString());
  } catch (_) {}
}

function getActiveAudienceValue() {
  const root = document.getElementById("theory-audience-toggle");
  if (root?.dataset?.currentAudience) return root.dataset.currentAudience;
  const active = document.querySelector("#theory-audience-toggle .theory-lang-btn.is-active");
  return active?.dataset?.audience || "all";
}

function getActiveViewValue() {
  const root = document.getElementById("theory-view-toggle");
  if (root?.dataset?.currentView) return root.dataset.currentView;
  const active = document.querySelector("#theory-view-toggle .theory-lang-btn.is-active");
  return active?.dataset?.view || "all";
}

function applySectionFilters(contentEl) {
  applyAudienceFilter(contentEl, getActiveAudienceValue());
  applyViewFilter(contentEl, getActiveViewValue());
}

function setupAudienceToggle(contentEl, params, setIdInQuery, setMap) {
  const toggleEl = document.getElementById("theory-audience-toggle");
  if (!toggleEl) return;

  const hasAudience = !!contentEl.querySelector(".theory-section-block[data-audience]");
  if (!hasAudience) {
    toggleEl.hidden = true;
    return;
  }

  const queryVal = String(params.get("audience") || "").toLowerCase();
  const bySet = guessAudienceFromSet(setIdInQuery, setMap);
  const selectedByDefault = ["all", "elementary", "middle", "high"].includes(queryVal)
    ? queryVal
    : bySet;
  toggleEl.dataset.currentAudience = selectedByDefault;

  toggleEl.hidden = false;
  toggleEl.innerHTML = "";

  const label = document.createElement("span");
  label.className = "theory-lang-label";
  label.textContent = "표시 범위";
  toggleEl.appendChild(label);

  const options = [
    { v: "all", t: "모두" },
    { v: "elementary", t: "초등만" },
    { v: "middle", t: "중등만" },
    { v: "high", t: "고등만" },
  ];

  options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theory-lang-btn";
    btn.dataset.audience = opt.v;
    btn.textContent = opt.t;
    if (opt.v === selectedByDefault) btn.classList.add("is-active");
    btn.addEventListener("click", () => {
      toggleEl
        .querySelectorAll(".theory-lang-btn")
        .forEach((it) => it.classList.toggle("is-active", it === btn));
      toggleEl.dataset.currentAudience = opt.v;
      applySectionFilters(contentEl);
      syncAudienceParam(opt.v);
    });
    toggleEl.appendChild(btn);
  });

  applyAudienceFilter(contentEl, selectedByDefault);
}

function setupViewToggle(contentEl, params, isHost) {
  const toggleEl = document.getElementById("theory-view-toggle");
  if (!toggleEl) return;

  const hasView = !!contentEl.querySelector(".theory-section-block[data-view]");
  if (!hasView) {
    toggleEl.hidden = true;
    return;
  }

  const queryVal = String(params.get("view") || "").toLowerCase();
  const selectedByDefault = ["all", "student", "teacher"].includes(queryVal)
    ? queryVal
    : "student";
  toggleEl.dataset.currentView = selectedByDefault;

  if (!isHost) {
    toggleEl.hidden = true;
    toggleEl.dataset.currentView = "student";
    applyViewFilter(contentEl, "student");
    syncViewParam("student");
    return;
  }

  toggleEl.hidden = false;
  toggleEl.innerHTML = "";

  const label = document.createElement("span");
  label.className = "theory-lang-label";
  label.textContent = "표시 대상";
  toggleEl.appendChild(label);

  const options = [
    { v: "student", t: "학생용" },
    { v: "teacher", t: "교사용" },
    { v: "all", t: "모두" },
  ];

  options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theory-lang-btn";
    btn.dataset.view = opt.v;
    btn.textContent = opt.t;
    if (opt.v === selectedByDefault) btn.classList.add("is-active");
    btn.addEventListener("click", () => {
      toggleEl
        .querySelectorAll(".theory-lang-btn")
        .forEach((it) => it.classList.toggle("is-active", it === btn));
      toggleEl.dataset.currentView = opt.v;
      applySectionFilters(contentEl);
      syncViewParam(opt.v);
    });
    toggleEl.appendChild(btn);
  });

  applyViewFilter(contentEl, selectedByDefault);
}

function buildTheoryLookup(items) {
  const byConceptId = {};
  const byCategoryId = {};
  (items || []).forEach((item) => {
    if (!item) return;
    if (item.conceptId) byConceptId[item.conceptId] = item;
    if (item.categoryId) byCategoryId[item.categoryId] = item;
  });
  return { byConceptId, byCategoryId };
}

function toSetMap(sets) {
  const map = {};
  (sets || []).forEach((setMeta) => {
    if (!setMeta || !setMeta.id) return;
    map[setMeta.id] = setMeta;
  });
  return map;
}

function buildRelatedSetIds(entry, allSets) {
  const fixed = Array.isArray(entry.relatedSetIds) ? entry.relatedSetIds : [];
  if (fixed.length) return fixed;
  return (allSets || [])
    .filter((setMeta) => setMeta.categoryId === entry.categoryId)
    .sort((a, b) => (a.round || 0) - (b.round || 0))
    .map((setMeta) => setMeta.id);
}

function renderRelatedList(entry, setMap, setIdInQuery) {
  const listEl = document.getElementById("theory-related-list");
  if (!listEl) return;
  listEl.innerHTML = "";

  const relatedIds = buildRelatedSetIds(entry, Object.values(setMap));
  if (!relatedIds.length) {
    const p = document.createElement("p");
    p.className = "theory-empty";
    p.textContent = "연결된 문제가 아직 없습니다.";
    listEl.appendChild(p);
    return;
  }

  relatedIds.forEach((setId) => {
    const meta = setMap[setId];
    if (!meta) return;

    const a = document.createElement("a");
    a.className = "theory-related-item";
    a.href = `practice.html?set=${encodeURIComponent(setId)}`;
    if (setId === entry.recommendedSetId) a.classList.add("is-recommended");

    const title = document.createElement("strong");
    title.textContent = meta.title || setId;
    const sub = document.createElement("small");
    const tags = [];
    tags.push(`Round ${meta.round ?? "-"}`);
    if (meta.difficulty) tags.push(meta.difficulty);
    if (setIdInQuery && setId === setIdInQuery) tags.push("현재 세트");
    sub.textContent = tags.join(" · ");

    a.appendChild(title);
    a.appendChild(sub);
    listEl.appendChild(a);
  });
}

function updateTopLinks(entry, setIdInQuery, params) {
  const backLink = document.getElementById("theory-back-link");
  const startBtn = document.getElementById("theory-start-btn");
  const track = params?.get("track") || "";
  const lang = params?.get("lang") || "";
  const indexQ = new URLSearchParams();
  if (track) indexQ.set("track", track);
  if (lang) indexQ.set("lang", lang);
  const indexHref = indexQ.toString() ? `index.html?${indexQ.toString()}` : "index.html";
  if (backLink) {
    if (setIdInQuery) {
      const q = new URLSearchParams();
      q.set("set", setIdInQuery);
      if (track) q.set("track", track);
      if (lang) q.set("lang", lang);
      backLink.href = `practice.html?${q.toString()}`;
      backLink.textContent = "← 문제로 복귀";
    } else {
      backLink.href = indexHref;
      backLink.textContent = "← 목록";
    }
  }
  if (startBtn) {
    if (entry.recommendedSetId) {
      const q = new URLSearchParams();
      q.set("set", entry.recommendedSetId);
      if (track) q.set("track", track);
      if (lang) q.set("lang", lang);
      startBtn.href = `practice.html?${q.toString()}`;
      startBtn.hidden = false;
    } else {
      startBtn.hidden = true;
    }
  }
}

async function apiIsHost() {
  if (window.__STEPCODE_IS_HOST__ === true) return true;
  try {
    const r = await fetch("/api/host/status", { credentials: "same-origin" });
    if (!r.ok) return false;
    const j = await r.json();
    return !!j.isHost;
  } catch (_) {
    return false;
  }
}

async function syncTheoryPrintButton(entry, params, setIdInQuery) {
  const btn = document.getElementById("theory-print-btn");
  if (!btn) return;
  btn.hidden = true;

  const isHost = await apiIsHost();
  if (!isHost) return;

  const q = new URLSearchParams();
  if (setIdInQuery) q.set("set", setIdInQuery);
  if (entry?.categoryId) q.set("category", entry.categoryId);
  if (entry?.conceptId) q.set("concept", entry.conceptId);

  const lang = params.get("lang") || entry?.lang || "";
  if (lang) q.set("lang", lang);

  btn.href = `theory_print.html?${q.toString()}`;
  btn.hidden = false;
}

function pickCombinedSetId(entry, setIdInQuery, setMap) {
  if (setIdInQuery && setMap?.[setIdInQuery]) return setIdInQuery;
  if (entry?.recommendedSetId && setMap?.[entry.recommendedSetId]) return entry.recommendedSetId;
  const related = buildRelatedSetIds(entry, Object.values(setMap || {}));
  return related.find((id) => setMap?.[id]) || "";
}

function syncTheoryCombinedPrintButton(entry, params, setIdInQuery, setMap, isHost) {
  const btn = document.getElementById("theory-combined-print-btn");
  if (!btn) return;
  btn.hidden = true;
  if (!isHost) return;

  const targetSetId = pickCombinedSetId(entry, setIdInQuery, setMap);
  if (!targetSetId) return;

  const q = new URLSearchParams();
  q.set("set", targetSetId);
  q.set("bucket", "all");
  q.set("variant", "student");
  q.set("concept", "1");
  q.set("theoryLayout", "double");
  q.set("mode", "quick");

  const lang = params.get("lang") || entry?.lang || "";
  if (lang) q.set("lang", lang);

  btn.href = `print.html?${q.toString()}`;
  btn.hidden = false;
}

function updateTitle(entry) {
  const titleEl = document.getElementById("theory-title");
  const subEl = document.getElementById("theory-subtitle");
  if (titleEl) titleEl.textContent = entry.title || entry.conceptId || "개념";
  if (subEl) {
    const rows = [];
    if (entry.lang) rows.push(entry.lang.toUpperCase());
    if (entry.categoryId) rows.push(entry.categoryId);
    subEl.textContent = rows.join(" · ");
  }
}

function pickEntry(params, lookup, setMap) {
  const conceptId = params.get("concept");
  const categoryId = params.get("category");
  const setId = params.get("set");

  if (conceptId && lookup.byConceptId[conceptId]) return lookup.byConceptId[conceptId];
  if (categoryId && lookup.byCategoryId[categoryId]) return lookup.byCategoryId[categoryId];
  if (setId && setMap[setId]) {
    const cat = setMap[setId].categoryId;
    if (cat && lookup.byCategoryId[cat]) return lookup.byCategoryId[cat];
  }
  return null;
}

async function initTheoryPage() {
  const contentEl = document.getElementById("theory-content");
  const params = new URLSearchParams(location.search);
  const setIdInQuery = params.get("set");
  const langInQuery = params.get("lang");

  try {
    const [theoryIndex, sets] = await Promise.all([
      ProblemService.listTheoryIndex(),
      ProblemService.listSets(),
    ]);
    const lookup = buildTheoryLookup(theoryIndex);
    const setMap = toSetMap(sets);
    const entry = pickEntry(params, lookup, setMap);
    const isHost = await apiIsHost();

    if (!entry) {
      contentEl.textContent = "개념을 찾을 수 없습니다. 목록에서 개념을 선택해 주세요.";
      return;
    }

    updateTitle(entry);
    updateTopLinks(entry, setIdInQuery, params);
    await syncTheoryPrintButton(entry, params, setIdInQuery);
    syncTheoryCombinedPrintButton(entry, params, setIdInQuery, setMap, isHost);
    renderRelatedList(entry, setMap, setIdInQuery);

    const res = await fetch(entry.mdPath);
    if (!res.ok) throw new Error(`failed to load markdown: ${entry.mdPath}`);
    const mdText = await res.text();
    renderTheoryMarkdown(contentEl, mdText);
    groupSectionBlocks(contentEl);
    setupAudienceToggle(contentEl, params, setIdInQuery, setMap);
    setupViewToggle(contentEl, params, isHost);
    applySectionFilters(contentEl);
    enhanceMiniCheckSection(contentEl);
    enhanceIoBlocks(contentEl);
    enhanceTraceGridBlocks(contentEl);
    enhanceMarkdownTables(contentEl);
    enhanceCodeBlocks(contentEl);
    enhanceExampleBlocks(contentEl);
    attachTrailingExampleBlocks(contentEl);
    setupLanguageToggle(contentEl, langInQuery || entry.lang);
  } catch (err) {
    console.error(err);
    contentEl.textContent = "개념 페이지를 불러오는 중 오류가 발생했습니다.";
  }
}

document.addEventListener("DOMContentLoaded", initTheoryPage);
