const TOGGLE_LANGS = new Set(["python", "c", "java", "csharp"]);

function qp(name) {
  const p = new URLSearchParams(location.search);
  return (p.get(name) || "").trim();
}

function setQp(name, value) {
  const url = new URL(location.href);
  if (value) url.searchParams.set(name, value);
  else url.searchParams.delete(name);
  history.replaceState(null, "", url.toString());
}

function normalizeLayout(raw) {
  return raw === "double" ? "double" : "single";
}

function normalizeCodeLang(raw) {
  const v = String(raw || "").toLowerCase();
  if (v === "py" || v === "python") return "python";
  if (v === "c" || v === "c99" || v === "c11") return "c";
  if (v === "java") return "java";
  if (v === "cs" || v === "c#" || v === "csharp") return "csharp";
  return v;
}

function normalizeLanguageList(raw) {
  return String(raw || "")
    .split(",")
    .map((s) => normalizeCodeLang(s.trim()))
    .filter(Boolean);
}

function detectLangFromCode(codeEl) {
  const classes = Array.from(codeEl.classList || []);
  for (const cls of classes) {
    if (!cls.startsWith("language-")) continue;
    return normalizeCodeLang(cls.replace("language-", ""));
  }
  return "";
}

function titleLang(lang) {
  if (lang === "python") return "Python";
  if (lang === "c") return "C";
  if (lang === "java") return "Java";
  if (lang === "csharp") return "C#";
  return lang.toUpperCase();
}

function getMdRenderer() {
  if (!window.markdownit || !window.DOMPurify) return null;
  return window.markdownit({
    html: false,
    linkify: true,
    breaks: true,
  });
}

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
  const conf = { title: "", langs: [], columns: [], rows: [] };
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

function enhanceIoBlocks(contentEl) {
  const candidates = contentEl.querySelectorAll("pre > code");
  candidates.forEach((codeEl) => {
    const lang = detectLangFromCode(codeEl);
    if (!["io", "inout", "exampleio"].includes(lang)) return;
    const pre = codeEl.closest("pre");
    if (!pre) return;
    pre.replaceWith(buildIoExampleBlock(parseIoFenceText(codeEl.textContent || "")));
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
    pre.replaceWith(buildTraceGridBlock(conf));
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
    if (TOGGLE_LANGS.has(lang)) {
      pre.dataset.codeLang = lang;
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
  const codeBlocks = contentEl.querySelectorAll("pre[data-code-lang]");
  codeBlocks.forEach((pre) => {
    const lang = pre.dataset.codeLang || "";
    pre.style.display = selected === "all" || lang === selected ? "" : "none";
    const label = pre.previousElementSibling;
    if (label?.classList?.contains("theory-code-label")) {
      label.style.display = selected === "all" || lang === selected ? "inline-flex" : "none";
    }
  });

  const textBlocks = contentEl.querySelectorAll("[data-lang-scope='text'][data-langs]");
  textBlocks.forEach((el) => {
    const langs = normalizeLanguageList(el.dataset.langs || "");
    el.style.display = selected === "all" || langs.includes(selected) ? "" : "none";
  });

  const traceBlocks = contentEl.querySelectorAll("[data-lang-scope='trace'][data-langs]");
  traceBlocks.forEach((el) => {
    const langs = normalizeLanguageList(el.dataset.langs || "");
    el.style.display = selected === "all" || langs.includes(selected) ? "" : "none";
  });
}

function setupLanguageSelect(contentEl, preferredLangRaw) {
  const sel = document.getElementById("tp-lang-select");
  const layoutSel = document.getElementById("tp-layout-select");
  const applyBtn = document.getElementById("tp-apply-btn");
  if (!sel || !layoutSel || !applyBtn) return;

  annotateLanguageTextBlocks(contentEl);

  const langs = new Set();
  contentEl.querySelectorAll("pre[data-code-lang]").forEach((pre) => langs.add(pre.dataset.codeLang));
  contentEl
    .querySelectorAll("[data-lang-scope='text'][data-langs], [data-lang-scope='trace'][data-langs]")
    .forEach((el) => normalizeLanguageList(el.dataset.langs || "").forEach((lang) => langs.add(lang)));

  const available = ["python", "c", "java", "csharp"].filter((lang) =>
    langs.has(lang)
  );
  const selectedFromQuery = normalizeCodeLang(qp("lang"));
  const preferred = normalizeCodeLang(preferredLangRaw);
  const defaultLang = available.includes(selectedFromQuery)
    ? selectedFromQuery
    : available.includes(preferred)
      ? preferred
      : "all";

  Array.from(sel.options).forEach((opt) => {
    if (opt.value === "all") return;
    opt.hidden = !available.includes(opt.value);
  });

  sel.value = defaultLang;
  applyLanguageFilter(contentEl, defaultLang);
  const initialLayout = normalizeLayout(qp("layout"));
  layoutSel.value = initialLayout;
  document.body.classList.toggle("layout-double", initialLayout === "double");

  applyBtn.addEventListener("click", () => {
    const selected = normalizeCodeLang(sel.value) || "all";
    const layout = normalizeLayout(layoutSel.value);
    setQp("lang", selected === "all" ? "" : selected);
    setQp("layout", layout === "single" ? "" : layout);
    applyLanguageFilter(contentEl, selected);
    document.body.classList.toggle("layout-double", layout === "double");
  });
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

function setupToolbarLinks(params, entry) {
  const back = document.getElementById("tp-back-link");
  if (back) {
    const q = new URLSearchParams();
    if (params.get("set")) q.set("set", params.get("set"));
    if (entry?.categoryId) q.set("category", entry.categoryId);
    if (entry?.conceptId) q.set("concept", entry.conceptId);
    const lang = qp("lang");
    if (lang) q.set("lang", lang);
    back.href = `theory.html?${q.toString()}`;
  }

  const printBtn = document.getElementById("tp-print-btn");
  if (printBtn) printBtn.addEventListener("click", () => window.print());
}

function renderDenied(root) {
  root.innerHTML = `
    <section class="theory-print-denied">
      <h1>접근 권한 없음</h1>
      <p>개념 출력은 관리자 접속에서만 사용할 수 있습니다.</p>
      <a href="theory.html">개념 페이지로 돌아가기</a>
    </section>
  `;
}

async function initTheoryPrintPage() {
  const root = document.getElementById("theory-print-root");
  const params = new URLSearchParams(location.search);
  const setIdInQuery = params.get("set");
  const langInQuery = params.get("lang");

  const isHost = await apiIsHost();
  if (!isHost) {
    document.body.classList.add("is-denied");
    const toolbar = document.querySelector(".theory-print-toolbar");
    if (toolbar) toolbar.style.display = "none";
    renderDenied(root);
    return;
  }

  try {
    const [theoryIndex, sets] = await Promise.all([
      ProblemService.listTheoryIndex(),
      ProblemService.listSets(),
    ]);
    const lookup = buildTheoryLookup(theoryIndex);
    const setMap = toSetMap(sets);
    const entry = pickEntry(params, lookup, setMap);

    if (!entry) {
      root.textContent = "출력할 개념을 찾을 수 없습니다.";
      return;
    }

    const title = document.getElementById("tp-title");
    const subtitle = document.getElementById("tp-subtitle");
    if (title) title.textContent = `${entry.title || "개념"} · 출력`;
    if (subtitle) {
      const rows = [];
      if (entry.lang) rows.push(titleLang(normalizeCodeLang(entry.lang)));
      if (entry.categoryId) rows.push(entry.categoryId);
      if (setIdInQuery) rows.push(`set=${setIdInQuery}`);
      subtitle.textContent = rows.join(" · ");
    }

    setupToolbarLinks(params, entry);

    const res = await fetch(entry.mdPath);
    if (!res.ok) throw new Error(`failed to load markdown: ${entry.mdPath}`);
    const mdText = await res.text();

    renderTheoryMarkdown(root, mdText);
    enhanceMiniCheckSection(root);
    enhanceIoBlocks(root);
    enhanceTraceGridBlocks(root);
    enhanceCodeBlocks(root);
    setupLanguageSelect(root, langInQuery || entry.lang);
  } catch (err) {
    console.error(err);
    root.textContent = "개념 출력 페이지를 불러오는 중 오류가 발생했습니다.";
  }
}

document.addEventListener("DOMContentLoaded", initTheoryPrintPage);
