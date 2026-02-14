function getMdRenderer() {
  if (!window.markdownit || !window.DOMPurify) return null;
  return window.markdownit({
    html: false,
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

function updateTopLinks(entry, setIdInQuery) {
  const backLink = document.getElementById("theory-back-link");
  const startBtn = document.getElementById("theory-start-btn");
  if (backLink) {
    if (setIdInQuery) {
      backLink.href = `practice.html?set=${encodeURIComponent(setIdInQuery)}`;
      backLink.textContent = "← 문제로 복귀";
    } else {
      backLink.href = "index.html";
      backLink.textContent = "← 목록";
    }
  }
  if (startBtn) {
    if (entry.recommendedSetId) {
      startBtn.href = `practice.html?set=${encodeURIComponent(entry.recommendedSetId)}`;
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

    if (!entry) {
      contentEl.textContent = "개념을 찾을 수 없습니다. 목록에서 개념을 선택해 주세요.";
      return;
    }

    updateTitle(entry);
    updateTopLinks(entry, setIdInQuery);
    await syncTheoryPrintButton(entry, params, setIdInQuery);
    renderRelatedList(entry, setMap, setIdInQuery);

    const res = await fetch(entry.mdPath);
    if (!res.ok) throw new Error(`failed to load markdown: ${entry.mdPath}`);
    const mdText = await res.text();
    renderTheoryMarkdown(contentEl, mdText);
    enhanceMiniCheckSection(contentEl);
    enhanceIoBlocks(contentEl);
    enhanceTraceGridBlocks(contentEl);
    enhanceCodeBlocks(contentEl);
    setupLanguageToggle(contentEl, langInQuery || entry.lang);
  } catch (err) {
    console.error(err);
    contentEl.textContent = "개념 페이지를 불러오는 중 오류가 발생했습니다.";
  }
}

document.addEventListener("DOMContentLoaded", initTheoryPage);
