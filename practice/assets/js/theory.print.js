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

function normalizeContestLang(raw) {
  const v = String(raw || "").trim().toLowerCase();
  if (v === "c") return "c";
  if (v === "py" || v === "python") return "py";
  return "";
}

function normalizeContestLevel(raw) {
  const v = String(raw || "").trim().toLowerCase();
  if (v === "elem" || v === "elementary" || v === "초등" || v === "초") return "elementary";
  if (v === "mid" || v === "middle" || v === "중등" || v === "중") return "middle";
  if (v === "high" || v === "고등" || v === "고") return "high";
  return "";
}

function inferContestLevelFromAudience(raw) {
  const v = String(raw || "").trim().toLowerCase();
  if (v === "elementary") return "elementary";
  if (v === "middle") return "middle";
  if (v === "high") return "high";
  return "";
}

function inferContestModeArgs(params) {
  const setId = String(params.get("set") || "");
  const setMatch = setId.match(/^contest_(c|py)_(elem|mid|high)_\d{4}_r\d+_b\d+$/i);

  const queryContestLang = normalizeContestLang(qp("contestLang"));
  const queryContestLevel = normalizeContestLevel(qp("contestLevel"));
  const queryLang = normalizeCodeLang(qp("lang"));
  const queryAudience = String(params.get("audience") || "").toLowerCase();
  const hasContestWeeks = !!qp("contestWeeks");

  const contestLang =
    queryContestLang ||
    (setMatch ? String(setMatch[1]).toLowerCase() : "") ||
    (queryLang === "python" ? "py" : queryLang === "c" ? "c" : "");
  const contestLevel =
    queryContestLevel ||
    (setMatch
      ? normalizeContestLevel(String(setMatch[2]).toLowerCase())
      : "") ||
    inferContestLevelFromAudience(queryAudience);

  const contestWeeksRaw = Number(qp("contestWeeks") || "11");
  const contestWeeks = Number.isFinite(contestWeeksRaw)
    ? Math.max(1, Math.min(30, Math.floor(contestWeeksRaw)))
    : 11;

  const isContestSet = !!setMatch;
  const wantsBatchByQuery = !!queryContestLang || !!queryContestLevel || hasContestWeeks;
  const batchMode = !!contestLang && (wantsBatchByQuery || (isContestSet && hasContestWeeks));

  return { batchMode, contestLang, contestLevel, contestWeeks };
}

function resolveContestTheoryEntries(theoryIndex, contestLang, maxWeeks) {
  const langToken = contestLang === "py" ? "py" : "c";
  const pat = new RegExp(`^contest_${langToken}_w(\\d{2})_`, "i");
  return (theoryIndex || [])
    .filter((it) => pat.test(String(it?.conceptId || "")))
    .map((it) => {
      const m = String(it.conceptId || "").match(/_w(\d{2})_/i);
      return { entry: it, week: m ? Number(m[1]) : Number.MAX_SAFE_INTEGER };
    })
    .sort((a, b) => a.week - b.week)
    .slice(0, Math.max(1, maxWeeks))
    .map((v) => v.entry);
}

function parseContestWeekFromConceptId(rawConceptId) {
  const m = String(rawConceptId || "").match(/_w(\d{2})_/i);
  return m ? Number(m[1]) : null;
}

function parseWeekSelection(raw, availableWeeks) {
  const available = (availableWeeks || []).map((v) => Number(v)).filter((v) => Number.isFinite(v));
  if (!available.length) return new Set();
  const picked = String(raw || "")
    .split(",")
    .map((v) => Number(v.trim()))
    .filter((v) => Number.isFinite(v) && available.includes(v));
  return picked.length ? new Set(picked) : new Set(available);
}

function serializeWeekSelection(selectedWeeks, availableWeeks) {
  const available = (availableWeeks || []).map((v) => Number(v)).filter((v) => Number.isFinite(v));
  const picked = available.filter((w) => selectedWeeks && selectedWeeks.has(w));
  if (!available.length || !picked.length || picked.length === available.length) return "";
  return picked.join(",");
}

function parseBatchConceptSelection(raw, availableConceptsByWeek) {
  const out = new Map();
  const chunks = String(raw || "")
    .split(";")
    .map((s) => s.trim())
    .filter(Boolean);
  chunks.forEach((chunk) => {
    const m = chunk.match(/^(\d{1,2}):(.*)$/);
    if (!m) return;
    const week = Number(m[1]);
    if (!Number.isFinite(week) || !availableConceptsByWeek.has(week)) return;
    const available = new Set(availableConceptsByWeek.get(week) || []);
    const picked = String(m[2] || "")
      .split(",")
      .map((v) => String(Number(v.trim())))
      .filter((v) => /^\d+$/.test(v) && available.has(v));
    out.set(week, new Set(picked));
  });
  return out;
}

function serializeBatchConceptSelection(selectedByWeek, availableConceptsByWeek, selectedWeeks) {
  const rows = [];
  const weeks = Array.from(availableConceptsByWeek.keys()).sort((a, b) => a - b);
  weeks.forEach((week) => {
    if (!selectedWeeks.has(week)) return;
    const available = availableConceptsByWeek.get(week) || [];
    const selected = Array.from(selectedByWeek.get(week) || []);
    const picked = available.filter((v) => selected.includes(v));
    if (!picked.length || picked.length === available.length) return;
    rows.push(`${week}:${picked.join(",")}`);
  });
  return rows.join(";");
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
  const pre = codeEl.closest("pre");
  if (pre && pre.dataset && pre.dataset.lang) {
    return normalizeCodeLang(pre.dataset.lang);
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
    html: true,
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

function findLastHeadingInNode(node) {
  if (!node) return null;
  if (/^H[1-6]$/.test(node.tagName || "")) return node;
  if (!node.querySelectorAll) return null;
  const hs = node.querySelectorAll("h1, h2, h3, h4, h5, h6");
  return hs.length ? hs[hs.length - 1] : null;
}

function findNearestPreviousHeadingText(root, startEl) {
  let cursor = startEl;
  while (cursor && cursor !== root) {
    let prev = cursor.previousElementSibling;
    while (prev) {
      const h = findLastHeadingInNode(prev);
      if (h) return String(h.textContent || "");
      prev = prev.previousElementSibling;
    }
    cursor = cursor.parentElement;
  }
  return "";
}

function isPracticeLinkedSectionByHeading(text) {
  return /연계\s*실습/.test(String(text || ""));
}

function isIoLabelParagraph(el) {
  if (!el || el.tagName !== "P") return false;
  const raw = String(el.textContent || "").trim();
  return /^예상\s*(입력\s*\/\s*출력|출력)\s*[:：]?\s*$/i.test(raw);
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
    const headingText = findNearestPreviousHeadingText(contentEl, pre);
    const inPractice = isPracticeLinkedSectionByHeading(headingText);
    if (inPractice) {
      const prev = pre.previousElementSibling;
      if (isIoLabelParagraph(prev)) prev.remove();
      pre.remove();
      return;
    }
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
  const heads = Array.from(contentEl.querySelectorAll("h2, h3"));
  const starts = heads.filter((h) => /미니\s*체크/.test(h.textContent || ""));
  if (!starts.length) return;

  starts.forEach((start) => {
    start.classList.add("theory-mini-check-title");

    const blockNodes = [];
    let cursor = start.nextElementSibling;
    while (cursor && cursor.tagName !== "H2") {
      blockNodes.push(cursor);
      cursor = cursor.nextElementSibling;
    }
    if (!blockNodes.length) return;

    const qLabel = blockNodes.find(
      (el) =>
        el.tagName === "P" &&
        /^문항\s*[:：]?\s*$/i.test(String(el.textContent || "").trim())
    );
    const qList =
      qLabel && qLabel.nextElementSibling && qLabel.nextElementSibling.tagName === "OL"
        ? qLabel.nextElementSibling
        : null;

    const aLabel = blockNodes.find(
      (el) =>
        el.tagName === "P" &&
        /^답안\s*작성\s*[:：]?\s*$/i.test(String(el.textContent || "").trim())
    );
    const aList =
      aLabel && aLabel.nextElementSibling && aLabel.nextElementSibling.tagName === "OL"
        ? aLabel.nextElementSibling
        : null;

    if (qLabel) qLabel.remove();
    if (aLabel) aLabel.remove();
    if (aList) aList.remove();

    if (!qList) return;
    qList.classList.add("theory-mini-check-qlist");
    const items = Array.from(qList.querySelectorAll(":scope > li"));
    items.forEach((li, idx) => {
      li.classList.add("theory-mini-check-qitem");

      const questionHtml = li.innerHTML;
      li.innerHTML = "";

      const itemRow = document.createElement("div");
      itemRow.className = "theory-mini-check-item-row";

      const itemNo = document.createElement("div");
      itemNo.className = "theory-mini-check-item-no";
      itemNo.textContent = `${idx + 1}.`;

      const itemWrap = document.createElement("div");
      itemWrap.className = "theory-mini-check-item-wrap";

      const question = document.createElement("div");
      question.className = "theory-mini-check-question";
      question.innerHTML = questionHtml;

      const answers = document.createElement("div");
      answers.className = "theory-mini-check-inline-answer";

      const answer = document.createElement("div");
      answer.className = "theory-mini-check-inline-field";
      const answerLabel = document.createElement("div");
      answerLabel.className = "theory-mini-check-inline-label";
      answerLabel.textContent = "정답";
      const answerBox = document.createElement("div");
      answerBox.className = "theory-mini-check-inline-box";
      answer.append(answerLabel, answerBox);

      const reason = document.createElement("div");
      reason.className = "theory-mini-check-inline-field";
      const reasonLabel = document.createElement("div");
      reasonLabel.className = "theory-mini-check-inline-label";
      reasonLabel.textContent = "근거";
      const reasonBox = document.createElement("div");
      reasonBox.className = "theory-mini-check-inline-box theory-mini-check-inline-box--reason";
      reason.append(reasonLabel, reasonBox);

      answers.append(answer, reason);
      itemWrap.append(question, answers);
      itemRow.append(itemNo, itemWrap);
      li.appendChild(itemRow);
    });
  });
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

function detectAudienceFromHeadingText(text) {
  const raw = String(text || "");
  if (/\bCOMMON\b/i.test(raw) || /공통/.test(raw)) return "common";
  if (/\bELEMENTARY\b/i.test(raw) || /초등/.test(raw)) return "elementary";
  if (/\bMIDDLE\b/i.test(raw) || /중등/.test(raw)) return "middle";
  if (/\bHIGH\b/i.test(raw) || /고등/.test(raw)) return "high";
  return "";
}

function detectViewFromHeadingText(text) {
  const raw = String(text || "");
  const m = raw.match(/\{view:(student|teacher)\}/i);
  if (m) return m[1].toLowerCase();
  if (/^\s*메타\s*$/i.test(raw)) return "teacher";
  return "";
}

function cleanHeadingMarkers(el) {
  if (!el) return;
  const next = String(el.textContent || "")
    .replace(/\{view:(student|teacher)\}/gi, "")
    .replace(/\s{2,}/g, " ")
    .trim();
  el.textContent = next;
}

function detectConceptFromHeadingText(text) {
  const m = String(text || "").match(/^\s*개념\s*(\d+)\)/i);
  return m ? String(Number(m[1])) : "";
}

function normalizeConceptHeadingLabel(text) {
  return String(text || "").replace(/\s+/g, " ").trim();
}

function groupSectionBlocks(contentEl) {
  const children = Array.from(contentEl.children || []);
  if (!children.length) return false;
  const markers = [];
  children.forEach((el, idx) => {
    if (el?.tagName === "H2") markers.push({ idx });
  });
  if (!markers.length) return false;

  const frag = document.createDocumentFragment();
  let cursor = 0;
  for (let i = 0; i < markers.length; i += 1) {
    const m = markers[i];
    const nextIdx = i + 1 < markers.length ? markers[i + 1].idx : children.length;
    const heading = children[m.idx];
    const aud = detectAudienceFromHeadingText(heading.textContent || "");
    const view = detectViewFromHeadingText(heading.textContent || "");
    cleanHeadingMarkers(heading);

    while (cursor < m.idx) {
      frag.appendChild(children[cursor]);
      cursor += 1;
    }

    const wrap = document.createElement("section");
    wrap.className = "theory-section-block";
    if (aud) wrap.dataset.audience = aud;
    if (view) wrap.dataset.view = view;
    for (let j = m.idx; j < nextIdx; j += 1) wrap.appendChild(children[j]);
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

function groupConceptBlocks(contentEl) {
  const sections = Array.from(contentEl.querySelectorAll(".theory-section-block"));
  if (!sections.length) return false;

  let grouped = false;
  sections.forEach((section) => {
    const children = Array.from(section.children || []);
    if (!children.length) return;

    const markers = [];
    children.forEach((el, idx) => {
      if (el?.tagName !== "H3") return;
      const headingText = String(el.textContent || "");
      const conceptNo = detectConceptFromHeadingText(headingText);
      if (!conceptNo) return;
      markers.push({
        idx,
        conceptNo,
        label: normalizeConceptHeadingLabel(headingText),
      });
    });
    if (!markers.length) return;

    const frag = document.createDocumentFragment();
    let cursor = 0;
    for (let i = 0; i < markers.length; i += 1) {
      const m = markers[i];
      const nextIdx = i + 1 < markers.length ? markers[i + 1].idx : children.length;

      while (cursor < m.idx) {
        frag.appendChild(children[cursor]);
        cursor += 1;
      }

      const wrap = document.createElement("section");
      wrap.className = "theory-concept-block";
      wrap.dataset.concept = m.conceptNo;
      wrap.dataset.conceptLabel = m.label || "";
      for (let j = m.idx; j < nextIdx; j += 1) wrap.appendChild(children[j]);
      cursor = nextIdx;
      frag.appendChild(wrap);
    }

    while (cursor < children.length) {
      frag.appendChild(children[cursor]);
      cursor += 1;
    }

    section.innerHTML = "";
    section.appendChild(frag);
    grouped = true;
  });

  return grouped;
}

function extractConceptItems(contentEl) {
  const byNo = new Map();
  contentEl.querySelectorAll(".theory-concept-block[data-concept]").forEach((block) => {
    const v = String(block.dataset.concept || "").trim();
    if (!/^\d+$/.test(v)) return;
    const label = String(block.dataset.conceptLabel || "").trim() || `개념 ${v}`;
    if (!byNo.has(v)) byNo.set(v, { no: v, label });
  });
  return Array.from(byNo.values()).sort((a, b) => Number(a.no) - Number(b.no));
}

function parseConceptSelection(raw, availableConcepts) {
  const values = String(raw || "")
    .split(",")
    .map((v) => String(Number(v.trim())))
    .filter((v) => /^\d+$/.test(v));
  if (!values.length) return null;

  const available = new Set((availableConcepts || []).map((v) => String(v)));
  const picked = new Set(values.filter((v) => available.has(v)));
  if (!picked.size) return null;
  if (picked.size === available.size) return null;
  return picked;
}

function serializeConceptSelection(selectedSet, availableConcepts) {
  if (!selectedSet || !selectedSet.size) return "";
  const available = (availableConcepts || []).map((v) => String(v));
  const picked = available.filter((v) => selectedSet.has(v));
  if (!picked.length || picked.length === available.length) return "";
  return picked.join(",");
}

function refreshSectionVisibility(block) {
  const byAudience = block.dataset.filterAudience !== "0";
  const byView = block.dataset.filterView !== "0";
  const byConcept = block.dataset.filterConcept !== "0";
  const byBatch = block.dataset.filterBatch !== "0";
  block.style.display = byAudience && byView && byConcept && byBatch ? "" : "none";
}

function setSectionFilterState(block, key, visible) {
  block.dataset[key] = visible ? "1" : "0";
  refreshSectionVisibility(block);
}

function applyAudienceFilter(contentEl, selected) {
  const blocks = contentEl.querySelectorAll(".theory-section-block[data-audience]");
  blocks.forEach((block) => {
    const aud = block.dataset.audience || "";
    let visible = true;
    if (selected === "all") visible = true;
    else if (aud === "common") visible = true;
    else visible = aud === selected;
    setSectionFilterState(block, "filterAudience", visible);
  });
}

function applyViewFilter(contentEl, selected) {
  const blocks = contentEl.querySelectorAll(".theory-section-block[data-view]");
  blocks.forEach((block) => {
    const view = block.dataset.view || "";
    const visible = selected === "all" ? true : view === selected;
    setSectionFilterState(block, "filterView", visible);
  });
}

function applyConceptFilter(contentEl, selectedSet) {
  const sections = contentEl.querySelectorAll(".theory-section-block");
  sections.forEach((section) => {
    const conceptBlocks = Array.from(
      section.querySelectorAll(":scope > .theory-concept-block[data-concept]")
    );
    if (!conceptBlocks.length) {
      setSectionFilterState(section, "filterConcept", true);
      return;
    }

    let hasVisible = false;
    conceptBlocks.forEach((block) => {
      const conceptNo = String(block.dataset.concept || "");
      const visible = !selectedSet || selectedSet.has(conceptNo);
      block.style.display = visible ? "" : "none";
      if (visible) hasVisible = true;
    });
    setSectionFilterState(section, "filterConcept", hasVisible);
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

function setupLanguageSelect(contentEl, preferredLangRaw, params, setIdInQuery, setMap, options) {
  const sel = document.getElementById("tp-lang-select");
  const audSel = document.getElementById("tp-audience-select");
  const viewSel = document.getElementById("tp-view-select");
  const layoutSel = document.getElementById("tp-layout-select");
  const conceptToggle = document.getElementById("tp-concept-toggle");
  const applyBtn = document.getElementById("tp-apply-btn");
  if (!sel || !audSel || !viewSel || !layoutSel || !applyBtn) return;

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
  const audienceFromQuery = String(params.get("audience") || "").toLowerCase();
  const defaultAudience = ["all", "elementary", "middle", "high"].includes(audienceFromQuery)
    ? audienceFromQuery
    : guessAudienceFromSet(setIdInQuery, setMap);
  const viewFromQuery = String(params.get("view") || "").toLowerCase();
  const defaultView = ["all", "student", "teacher"].includes(viewFromQuery)
    ? viewFromQuery
    : "student";
  const conceptItems = extractConceptItems(contentEl);
  const availableConcepts = conceptItems.map((it) => it.no);
  let selectedConceptSet = parseConceptSelection(params.get("concepts"), availableConcepts);

  Array.from(sel.options).forEach((opt) => {
    if (opt.value === "all") return;
    opt.hidden = !available.includes(opt.value);
  });

  sel.value = defaultLang;
  audSel.value = defaultAudience;
  viewSel.value = defaultView;
  applyLanguageFilter(contentEl, defaultLang);
  applyAudienceFilter(contentEl, defaultAudience);
  applyViewFilter(contentEl, defaultView);
  applyConceptFilter(contentEl, selectedConceptSet);
  if (typeof options?.onAfterFilter === "function") options.onAfterFilter();
  const initialLayout = normalizeLayout(qp("layout"));
  layoutSel.value = initialLayout;
  document.body.classList.toggle("layout-double", initialLayout === "double");

  const disableConceptToggle = !!options?.disableConceptToggle;
  if (conceptToggle) {
    conceptToggle.innerHTML = "";
    if (availableConcepts.length && !disableConceptToggle) {
      const label = document.createElement("span");
      label.className = "tp-concept-label";
      label.textContent = "개념";
      conceptToggle.appendChild(label);

      const allBtn = document.createElement("button");
      allBtn.type = "button";
      allBtn.className = "tp-concept-btn";
      allBtn.textContent = "전체";
      conceptToggle.appendChild(allBtn);

      const conceptBtns = conceptItems.map((item) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "tp-concept-btn";
        btn.dataset.concept = item.no;
        btn.textContent = item.label;
        conceptToggle.appendChild(btn);
        return btn;
      });

      const renderConceptBtns = () => {
        allBtn.classList.toggle("is-active", !selectedConceptSet || !selectedConceptSet.size);
        conceptBtns.forEach((btn) => {
          const conceptNo = String(btn.dataset.concept || "");
          btn.classList.toggle("is-active", !!selectedConceptSet && selectedConceptSet.has(conceptNo));
        });
      };

      allBtn.addEventListener("click", () => {
        selectedConceptSet = null;
        renderConceptBtns();
      });

      conceptBtns.forEach((btn) => {
        btn.addEventListener("click", () => {
          const conceptNo = String(btn.dataset.concept || "");
          if (!selectedConceptSet) {
            selectedConceptSet = new Set([conceptNo]);
          } else {
            if (selectedConceptSet.has(conceptNo)) selectedConceptSet.delete(conceptNo);
            else selectedConceptSet.add(conceptNo);
            if (!selectedConceptSet.size || selectedConceptSet.size === availableConcepts.length) {
              selectedConceptSet = null;
            }
          }
          renderConceptBtns();
        });
      });

      renderConceptBtns();
    }
  }

  applyBtn.addEventListener("click", () => {
    const selected = normalizeCodeLang(sel.value) || "all";
    const selectedAudience = audSel.value || "all";
    const selectedView = viewSel.value || "student";
    const layout = normalizeLayout(layoutSel.value);
    const concepts = serializeConceptSelection(selectedConceptSet, availableConcepts);
    setQp("lang", selected === "all" ? "" : selected);
    setQp("audience", selectedAudience === "all" ? "" : selectedAudience);
    setQp("view", selectedView === "all" ? "" : selectedView);
    if (!disableConceptToggle || !options?.preserveConceptParam) setQp("concepts", concepts);
    setQp("layout", layout === "single" ? "" : layout);
    applyLanguageFilter(contentEl, selected);
    applyAudienceFilter(contentEl, selectedAudience);
    applyViewFilter(contentEl, selectedView);
    applyConceptFilter(contentEl, disableConceptToggle ? null : selectedConceptSet);
    if (typeof options?.onAfterFilter === "function") options.onAfterFilter();
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
    const audience = qp("audience");
    const view = qp("view");
    const concepts = qp("concepts");
    if (audience) q.set("audience", audience);
    if (view) q.set("view", view);
    if (concepts) q.set("concepts", concepts);
    back.href = `theory.html?${q.toString()}`;
  }

  const printBtn = document.getElementById("tp-print-btn");
  if (printBtn) printBtn.addEventListener("click", () => window.print());
}

function applyBatchWeekConceptFilter(weekModels, selectedWeeks, selectedConceptsByWeek) {
  (weekModels || []).forEach((weekModel) => {
    const week = Number(weekModel.week);
    const weekSelected = selectedWeeks.has(week);
    const selectedConcepts = selectedConceptsByWeek.get(week) || new Set();
    const sectionBlocks = Array.from(
      weekModel.body.querySelectorAll(".theory-section-block")
    );

    sectionBlocks.forEach((section) => {
      const conceptBlocks = Array.from(
        section.querySelectorAll(":scope > .theory-concept-block[data-concept]")
      );
      if (!conceptBlocks.length) {
        setSectionFilterState(section, "filterBatch", weekSelected);
        return;
      }

      let hasVisibleConcept = false;
      conceptBlocks.forEach((block) => {
        const conceptNo = String(block.dataset.concept || "");
        const visible = weekSelected && selectedConcepts.has(conceptNo);
        block.style.display = visible ? "" : "none";
        if (visible) hasVisibleConcept = true;
      });
      setSectionFilterState(section, "filterConcept", hasVisibleConcept);
      setSectionFilterState(section, "filterBatch", weekSelected);
    });

    const hasVisibleSection = sectionBlocks.some((section) => section.style.display !== "none");
    weekModel.section.style.display = weekSelected && hasVisibleSection ? "" : "none";
  });
}

function setupContestBatchToolbar(weekModels) {
  const panel = document.getElementById("tp-batch-controls");
  if (!panel) return null;

  const sortedWeeks = (weekModels || [])
    .map((m) => Number(m.week))
    .filter((w) => Number.isFinite(w))
    .sort((a, b) => a - b);
  if (!sortedWeeks.length) {
    panel.hidden = true;
    panel.innerHTML = "";
    return null;
  }

  const params = new URLSearchParams(location.search);
  const availableConceptsByWeek = new Map();
  const conceptLabelByWeek = new Map();
  const conceptDisplayLabelByNo = new Map();
  weekModels.forEach((model) => {
    const pairs = (model.conceptItems || []).map((it) => ({
      no: String(it.no),
      label: String(it.label || `개념 ${it.no}`),
    }));
    availableConceptsByWeek.set(
      Number(model.week),
      pairs.map((it) => it.no)
    );
    const weekLabelMap = new Map();
    pairs.forEach((it) => {
      weekLabelMap.set(it.no, it.label);
      if (!conceptDisplayLabelByNo.has(it.no)) conceptDisplayLabelByNo.set(it.no, it.label);
    });
    conceptLabelByWeek.set(Number(model.week), weekLabelMap);
  });

  const selectedWeeks = parseWeekSelection(params.get("weeks"), sortedWeeks);
  const selectedByWeek = new Map();
  sortedWeeks.forEach((week) => {
    selectedByWeek.set(week, new Set(availableConceptsByWeek.get(week) || []));
  });

  const parsedByWeek = parseBatchConceptSelection(params.get("concepts"), availableConceptsByWeek);
  parsedByWeek.forEach((pickedSet, week) => {
    selectedByWeek.set(week, new Set(pickedSet));
  });

  sortedWeeks.forEach((week) => {
    const available = availableConceptsByWeek.get(week) || [];
    const selected = selectedByWeek.get(week) || new Set();
    if (!available.length || !selected.size) selectedWeeks.delete(week);
  });

  const unionConceptNos = Array.from(
    new Set(
      sortedWeeks.flatMap((week) => availableConceptsByWeek.get(week) || [])
    )
  ).sort((a, b) => Number(a) - Number(b));
  let bulkSelectedSet = new Set(unionConceptNos);

  panel.hidden = false;
  panel.innerHTML = "";

  const weeksRow = document.createElement("div");
  weeksRow.className = "tp-batch-row";
  const weeksTitle = document.createElement("span");
  weeksTitle.className = "tp-batch-row-title";
  weeksTitle.textContent = "주차 선택";
  weeksRow.appendChild(weeksTitle);

  const weekAllBtn = document.createElement("button");
  weekAllBtn.type = "button";
  weekAllBtn.className = "tp-batch-btn secondary";
  weekAllBtn.textContent = "전체 선택";
  weeksRow.appendChild(weekAllBtn);

  const weekClearBtn = document.createElement("button");
  weekClearBtn.type = "button";
  weekClearBtn.className = "tp-batch-btn secondary";
  weekClearBtn.textContent = "전체 해제";
  weeksRow.appendChild(weekClearBtn);

  const weekButtons = new Map();
  sortedWeeks.forEach((week) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tp-batch-btn";
    btn.dataset.week = String(week);
    btn.textContent = `${week}주차`;
    weekButtons.set(week, btn);
    weeksRow.appendChild(btn);
  });
  panel.appendChild(weeksRow);

  const bulkRow = document.createElement("div");
  bulkRow.className = "tp-batch-row";
  const bulkTitle = document.createElement("span");
  bulkTitle.className = "tp-batch-row-title";
  bulkTitle.textContent = "일괄 동작";
  bulkRow.appendChild(bulkTitle);

  const bulkConceptButtons = [];
  unionConceptNos.forEach((conceptNo) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "tp-batch-btn";
    btn.dataset.concept = conceptNo;
    btn.textContent = conceptDisplayLabelByNo.get(conceptNo) || `개념 ${conceptNo}`;
    bulkConceptButtons.push(btn);
    bulkRow.appendChild(btn);
  });

  const bulkApplyBtn = document.createElement("button");
  bulkApplyBtn.type = "button";
  bulkApplyBtn.className = "tp-batch-btn secondary";
  bulkApplyBtn.textContent = "선택 주차 동일 적용";
  bulkRow.appendChild(bulkApplyBtn);

  const bulkClearBtn = document.createElement("button");
  bulkClearBtn.type = "button";
  bulkClearBtn.className = "tp-batch-btn secondary";
  bulkClearBtn.textContent = "모두 해제";
  bulkRow.appendChild(bulkClearBtn);
  panel.appendChild(bulkRow);

  const editorTitle = document.createElement("div");
  editorTitle.className = "tp-batch-row-title";
  editorTitle.textContent = "개념 선택 편집";
  panel.appendChild(editorTitle);

  const editorList = document.createElement("div");
  editorList.className = "tp-week-editor-list";
  panel.appendChild(editorList);

  const rowRefs = new Map();
  sortedWeeks.forEach((week) => {
    const item = document.createElement("div");
    item.className = "tp-week-editor-item";
    const label = document.createElement("span");
    label.className = "tp-week-editor-label";
    label.textContent = `${week}주차`;
    item.appendChild(label);

    const allBtn = document.createElement("button");
    allBtn.type = "button";
    allBtn.className = "tp-batch-btn";
    allBtn.dataset.week = String(week);
    allBtn.textContent = "전체";
    item.appendChild(allBtn);

    const conceptBtns = [];
    (availableConceptsByWeek.get(week) || []).forEach((conceptNo) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "tp-batch-btn";
      btn.dataset.week = String(week);
      btn.dataset.concept = conceptNo;
      btn.textContent =
        conceptLabelByWeek.get(week)?.get(conceptNo) || `개념 ${conceptNo}`;
      conceptBtns.push(btn);
      item.appendChild(btn);
    });

    rowRefs.set(week, { item, allBtn, conceptBtns });
    editorList.appendChild(item);
  });

  function syncBatchQuery() {
    setQp("weeks", serializeWeekSelection(selectedWeeks, sortedWeeks));
    setQp(
      "concepts",
      serializeBatchConceptSelection(selectedByWeek, availableConceptsByWeek, selectedWeeks)
    );
  }

  function apply() {
    applyBatchWeekConceptFilter(weekModels, selectedWeeks, selectedByWeek);
    syncBatchQuery();
  }

  function renderState() {
    sortedWeeks.forEach((week) => {
      const isWeekSelected = selectedWeeks.has(week);
      const refs = rowRefs.get(week);
      const picked = selectedByWeek.get(week) || new Set();
      const available = availableConceptsByWeek.get(week) || [];
      const weekBtn = weekButtons.get(week);
      if (weekBtn) weekBtn.classList.toggle("is-active", isWeekSelected);
      refs.item.classList.toggle("is-off", !isWeekSelected);
      refs.allBtn.classList.toggle("is-active", !!available.length && picked.size === available.length);
      refs.conceptBtns.forEach((btn) => {
        const c = String(btn.dataset.concept || "");
        btn.classList.toggle("is-active", picked.has(c));
      });
    });

    bulkConceptButtons.forEach((btn) => {
      const c = String(btn.dataset.concept || "");
      btn.classList.toggle("is-active", bulkSelectedSet.has(c));
    });
  }

  weekAllBtn.addEventListener("click", () => {
    sortedWeeks.forEach((week) => {
      selectedWeeks.add(week);
      selectedByWeek.set(week, new Set(availableConceptsByWeek.get(week) || []));
    });
    renderState();
    apply();
  });

  weekClearBtn.addEventListener("click", () => {
    selectedWeeks.clear();
    sortedWeeks.forEach((week) => selectedByWeek.set(week, new Set()));
    renderState();
    apply();
  });

  weekButtons.forEach((btn, week) => {
    btn.addEventListener("click", () => {
      if (selectedWeeks.has(week)) {
        selectedWeeks.delete(week);
      } else {
        selectedWeeks.add(week);
        if (!(selectedByWeek.get(week) || new Set()).size) {
          selectedByWeek.set(week, new Set(availableConceptsByWeek.get(week) || []));
        }
      }
      renderState();
      apply();
    });
  });

  bulkConceptButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const c = String(btn.dataset.concept || "");
      if (bulkSelectedSet.has(c)) bulkSelectedSet.delete(c);
      else bulkSelectedSet.add(c);
      renderState();
    });
  });

  bulkApplyBtn.addEventListener("click", () => {
    sortedWeeks.forEach((week) => {
      if (!selectedWeeks.has(week)) return;
      const available = availableConceptsByWeek.get(week) || [];
      const picked = available.filter((c) => bulkSelectedSet.has(c));
      const next = new Set(picked);
      selectedByWeek.set(week, next);
      if (!next.size) selectedWeeks.delete(week);
    });
    renderState();
    apply();
  });

  bulkClearBtn.addEventListener("click", () => {
    selectedWeeks.clear();
    sortedWeeks.forEach((week) => selectedByWeek.set(week, new Set()));
    renderState();
    apply();
  });

  rowRefs.forEach((refs, week) => {
    refs.allBtn.addEventListener("click", () => {
      selectedWeeks.add(week);
      selectedByWeek.set(week, new Set(availableConceptsByWeek.get(week) || []));
      renderState();
      apply();
    });
    refs.conceptBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const c = String(btn.dataset.concept || "");
        const picked = new Set(selectedByWeek.get(week) || []);
        if (picked.has(c)) picked.delete(c);
        else picked.add(c);
        selectedByWeek.set(week, picked);
        if (picked.size) selectedWeeks.add(week);
        else selectedWeeks.delete(week);
        renderState();
        apply();
      });
    });
  });

  renderState();
  apply();

  return {
    applyFilters: () => applyBatchWeekConceptFilter(weekModels, selectedWeeks, selectedByWeek),
  };
}

function setupBatchToolbarLinks() {
  const back = document.getElementById("tp-back-link");
  if (back) back.href = "index.html?track=contest";
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
    const contestArgs = inferContestModeArgs(params);
    const contestLang = contestArgs.contestLang;
    const contestLevel = contestArgs.contestLevel || "all";
    const contestWeeks = contestArgs.contestWeeks;

    if (contestArgs.batchMode) {
      const entries = resolveContestTheoryEntries(theoryIndex, contestLang, contestWeeks);
      if (!entries.length) {
        root.textContent = "출력할 경시대회 이론을 찾을 수 없습니다.";
        return;
      }

      const title = document.getElementById("tp-title");
      const subtitle = document.getElementById("tp-subtitle");
      if (title) {
        const langLabel = contestLang === "c" ? "C" : "PY";
        const levelLabel =
          contestLevel === "elementary"
            ? "초등"
            : contestLevel === "middle"
              ? "중등"
              : contestLevel === "high"
                ? "고등"
                : "전체";
        title.textContent = `${langLabel} 경시대회 이론 ${levelLabel} ${entries.length}회차 출력`;
      }
      if (subtitle) subtitle.textContent = "범위: 주차별 이론 통합";

      setupBatchToolbarLinks();
      root.innerHTML = "";
      const weekModels = [];

      for (let i = 0; i < entries.length; i += 1) {
        const entry = entries[i];
        const res = await fetch(entry.mdPath);
        if (!res.ok) throw new Error(`failed to load markdown: ${entry.mdPath}`);
        const mdText = await res.text();
        const weekNo = parseContestWeekFromConceptId(entry.conceptId) || i + 1;

        const section = document.createElement("section");
        section.className = "theory-batch-section";
        section.dataset.week = String(weekNo);
        const head = document.createElement("h1");
        head.className = "theory-batch-title";
        head.textContent = `${weekNo}회차 · ${entry.title || entry.conceptId || "이론"}`;
        const body = document.createElement("article");
        body.className = "theory-batch-body";
        section.append(head, body);
        root.appendChild(section);

        renderTheoryMarkdown(body, mdText);
        groupSectionBlocks(body);
        groupConceptBlocks(body);
        enhanceMiniCheckSection(body);
        enhanceIoBlocks(body);
        enhanceTraceGridBlocks(body);
        enhanceMarkdownTables(body);
        enhanceCodeBlocks(body);
        enhanceExampleBlocks(body);
        attachTrailingExampleBlocks(body);

        weekModels.push({
          week: weekNo,
          section,
          body,
          conceptItems: extractConceptItems(body),
        });
      }

      const batchController = setupContestBatchToolbar(weekModels);

      setupLanguageSelect(
        root,
        contestLang === "c" ? "c" : "python",
        params,
        "",
        setMap,
        {
          disableConceptToggle: true,
          preserveConceptParam: true,
          onAfterFilter: () => {
            if (batchController) batchController.applyFilters();
          },
        }
      );
      return;
    }

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
    groupSectionBlocks(root);
    groupConceptBlocks(root);
    enhanceMiniCheckSection(root);
    enhanceIoBlocks(root);
    enhanceTraceGridBlocks(root);
    enhanceMarkdownTables(root);
    enhanceCodeBlocks(root);
    enhanceExampleBlocks(root);
    attachTrailingExampleBlocks(root);
    setupLanguageSelect(root, langInQuery || entry.lang, params, setIdInQuery, setMap, {
      disableConceptToggle: false,
    });
  } catch (err) {
    console.error(err);
    root.textContent = "개념 출력 페이지를 불러오는 중 오류가 발생했습니다.";
  }
}

document.addEventListener("DOMContentLoaded", initTheoryPrintPage);
