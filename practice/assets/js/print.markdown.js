/* print.js - A4 landscape worksheet printer (2 columns, 4 problems per page) */

let currentSetData = null;
const SLOTS_PER_PAGE = 2;
let currentShowLineNumbers = false;
const PRINT_PAGE_MARGIN_MM = 3;
const PRINT_PAGE_WIDTH_MM = 297;
const PACKING_SAFETY_MM = 0;
const FIT_TOLERANCE_MM = 3;
const CODE_SPLIT_MIN_LINES = 24;

function ymd(d = new Date()) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function chunk(arr, n) {
  const out = [];
  for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
  return out;
}


/** CSS 길이(mm 등)를 px로 변환 (브라우저가 계산하게 만든 뒤 측정) */
function cssToPx(cssLen) {
  const probe = document.createElement("div");
  probe.style.position = "absolute";
  probe.style.visibility = "hidden";
  probe.style.height = cssLen;
  document.body.appendChild(probe);
  const px = probe.getBoundingClientRect().height;
  probe.remove();
  return px;
}

/** header + gap 등을 제외한 "페이지 본문(문제영역)" 높이(px) 계산 */
function getBodyHeightPx(pageEl) {
  const pageH = cssToPx(`calc(210mm - ${PRINT_PAGE_MARGIN_MM * 2}mm)`);
  const header = pageEl.querySelector(".page-header");
  const h = header ? header.getBoundingClientRect().height : 0;
  const mb = header ? parseFloat(getComputedStyle(header).marginBottom || "0") : 0;
  return pageH - h - mb;
}

/** 카드 하나의 "실제 렌더 높이" 측정 (같은 폭에서) */
function measureCardHeightPx(cardEl, colWidthPx) {
  cardEl.style.width = `${colWidthPx}px`;
  cardEl.style.boxSizing = "border-box";
  // DOM에 붙어 있어야 측정 가능(숨김 컨테이너에 붙여 측정)
  return cardEl.getBoundingClientRect().height;
}

function bucketOfQuestion(set, q, idx) {
  const coreCount = Number(set?.coreCount ?? 6);
  if (q.bucket === "core" || q.bucket === "supp") return q.bucket;
  return idx < coreCount ? "core" : "supp";
}

function isCondBlankQuestion(q) {
  if (!q || q.type !== "code") return false;
  const code = String(q.code ?? "");
  return /(^|\n)\s*(if|elif)\s*#/.test(code);
}

function typeLabel(q) {
  if (q.type === "mcq") return "객관식";
  if (q.type === "short") return "단답";
  if (q.type === "code") return "코드";
  return q.type || "";
}

function getQuestionConceptRefsForPrint(q) {
  if (!q || typeof q !== "object") return [];
  const refs = [];
  if (Array.isArray(q.conceptRefs)) {
    q.conceptRefs.forEach((v) => {
      const s = String(v || "").trim();
      if (s) refs.push(s);
    });
  }
  if (q.conceptRef) {
    const s = String(q.conceptRef || "").trim();
    if (s) refs.push(s);
  }
  return Array.from(new Set(refs));
}

function getQuestionConceptTitlesForPrint(set, q) {
  const refs = getQuestionConceptRefsForPrint(q);
  if (!refs.length) return [];
  const concepts = Array.isArray(set?.concepts) ? set.concepts : [];
  const byId = {};
  concepts.forEach((c) => {
    if (!c || !c.id) return;
    byId[String(c.id)] = c;
  });
  return refs.map((id) => byId[id]?.title || id);
}

function isGridQuestion(q) {
  return q && q.type === "short" && q.answerUi && q.answerUi.kind === "grid";
}

function buildExpectedGridMatrixForPrint(q, rowCount, colCount) {
  if (Array.isArray(q.expectedGrid)) {
    return q.expectedGrid.map((r) => (Array.isArray(r) ? r : []));
  }
  return Array.from({ length: rowCount }, () => Array(colCount).fill(""));
}

function isSkippedGridCellForPrint(q, r, c, expectedMatrix) {
  const ui = q.answerUi || {};
  const explicit = Array.isArray(ui.skipCells) ? ui.skipCells : [];
  const key = `${r},${c}`;
  if (explicit.includes(key)) return true;

  const skipEmptyExpected = ui.skipEmptyExpected !== false;
  if (!skipEmptyExpected) return false;

  const expected = String(
    (expectedMatrix[r] && expectedMatrix[r][c]) ?? ""
  ).trim();
  return expected === "";
}

function extractFirstMarkdownTable(raw) {
  const text = String(raw ?? "").replace(/\r\n?/g, "\n");
  const lines = text.split("\n");
  const isTableRow = (s) => /\|/.test(s);
  const isSepRow = (s) => /^\s*\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)*\s*\|?\s*$/.test(s);

  for (let i = 0; i < lines.length - 1; i++) {
    if (isTableRow(lines[i]) && isSepRow(lines[i + 1])) {
      const out = [lines[i], lines[i + 1]];
      let j = i + 2;
      while (j < lines.length && lines[j].trim() !== "" && isTableRow(lines[j])) {
        out.push(lines[j]);
        j++;
      }
      return out.join("\n");
    }
  }
  return "";
}

function removeFirstMarkdownTable(raw) {
  const text = String(raw ?? "").replace(/\r\n?/g, "\n");
  const lines = text.split("\n");
  const isTableRow = (s) => /\|/.test(s);
  const isSepRow = (s) => /^\s*\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)*\s*\|?\s*:?-{3,}:?\s*\|?\s*$/.test(s);

  for (let i = 0; i < lines.length - 1; i++) {
    if (isTableRow(lines[i]) && isSepRow(lines[i + 1])) {
      let j = i + 2;
      while (j < lines.length && lines[j].trim() !== "" && isTableRow(lines[j])) {
        j++;
      }
      const before = lines.slice(0, i);
      const after = lines.slice(j);
      const merged = before.concat(after).join("\n").replace(/\n{3,}/g, "\n\n").trim();
      return merged;
    }
  }
  return text;
}

function correctForTeacher(q) {
  if (!q) return "";
  if (q.type === "mcq") {
    const i = Number(q.correctIndex);
    const labels = q.optionLabels || [];
    const letter = labels[i] || String.fromCharCode(65 + i);
    return `정답: ${letter}`;
  }
  if (q.type === "short") {
    if (q.expectedText) return `정답: ${q.expectedText}`;
    if (Array.isArray(q.expectedAnyOf)) return `정답(예시): ${q.expectedAnyOf.join(", ")}`;
    return "";
  }
  if (q.type === "code") {
    if (q.expectedCode) return `기대 코드: ${q.expectedCode}`;
    if (Array.isArray(q.expectedCodes) && q.expectedCodes.length) return `기대 코드: ${q.expectedCodes[0]}`;
    return "";
  }
  return "";
}

function splitDescriptionForView(rawText) {
  const text = String(rawText ?? "");
  if (!text) return { main: "", view: "" };

  const lines = text.replace(/\r\n?/g, "\n").split("\n");
  const markerIndex = lines.findIndex((line) =>
    /^\s*보기\s*[:：]?\s*$/.test(line)
  );

  if (markerIndex < 0) return { main: text, view: "" };

  const main = lines.slice(0, markerIndex).join("\n").trim();
  const view = lines.slice(markerIndex + 1).join("\n").trim();
  return { main, view };
}

function buildGridAnswerTable(q, variant) {
  const ui = q.answerUi || {};
  const rows = Array.isArray(ui.rows) && ui.rows.length ? ui.rows : [];
  const cols = Array.isArray(ui.columns) && ui.columns.length ? ui.columns : [];
  const expected = buildExpectedGridMatrixForPrint(q, rows.length, cols.length);

  const wrap = el("div", "grid-answer-wrap");
  const table = el("table", "grid-answer-table");
  let hasSkippedCell = false;

  const thead = document.createElement("thead");
  const trh = document.createElement("tr");
  const corner = el("th", "grid-corner", "");
  trh.appendChild(corner);
  cols.forEach((c) => trh.appendChild(el("th", "grid-col-label", c)));
  thead.appendChild(trh);
  table.appendChild(thead);

  const tbody = document.createElement("tbody");
  rows.forEach((r, rIdx) => {
    const tr = document.createElement("tr");
    tr.appendChild(el("th", "grid-row-label", r));
    cols.forEach((_c, cIdx) => {
      const td = document.createElement("td");
      const skipped = isSkippedGridCellForPrint(q, rIdx, cIdx, expected);
      if (skipped) {
        hasSkippedCell = true;
        td.classList.add("grid-cell-skipped");
      }
      const val =
        variant === "teacher" && expected[rIdx]
          ? String(expected[rIdx][cIdx] ?? "")
          : "";
      td.textContent = skipped ? (val || "N/A") : val;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
  wrap.appendChild(table);
  if (hasSkippedCell) {
    wrap.appendChild(el("div", "grid-answer-note", "회색 칸은 입력하지 않아도 됩니다."));
  }
  return wrap;
}

function makeDocId(setId, bucket, variant) {
  const stamp = ymd().replaceAll("-", "");
  return `${setId}-${stamp}-${bucket}-${variant}`.toUpperCase();
}

function el(tag, cls, text) {
  const x = document.createElement(tag);
  if (cls) x.className = cls;
  if (text != null) x.textContent = text;
  return x;
}

function detectPrismLanguage(set) {
  const raw = String(
    (set && Array.isArray(set.availableLanguages) ? set.availableLanguages[0] : "") || ""
  )
    .trim()
    .toLowerCase();

  if (raw === "python" || raw === "py") return "python";
  if (raw === "java") return "java";
  if (raw === "csharp" || raw === "cs" || raw === "c#") return "csharp";
  if (raw === "c") return "c";
  return "clike";
}

function buildHighlightedCodePre(set, className, source, withLineNumbers = true) {
  const pre = el("pre", className);
  if (currentShowLineNumbers && withLineNumbers) pre.classList.add("line-numbers");
  const code = document.createElement("code");
  code.className = `language-${detectPrismLanguage(set)}`;
  code.textContent = String(source ?? "");
  pre.appendChild(code);
  return pre;
}

function applyPrismHighlight(scopeEl) {
  const prism = window.Prism;
  if (!prism || typeof prism.highlightElement !== "function") return;
  const root = scopeEl || document;
  root.querySelectorAll("pre.p-code code, pre.opt-code code").forEach((node) => {
    prism.highlightElement(node);
  });
}

function shouldMcqOptionsUseTwoColumns(q) {
  const opts = Array.isArray(q?.options) ? q.options : [];
  if (opts.length < 4) return false;
  if (opts.length > 6) return false;

  const MAX_ROWS = 10;
  const MAX_ROW_CHARS = 12;

  const normalize = (s) =>
    String(s ?? "")
      .replace(/\r\n/g, "\n")
      .trim();

  return opts.every((o) => {
    const t = normalize(o);
    if (!t) return true;

    const physicalLines = t.split("\n");
    let estimatedRows = 0;

    for (const line of physicalLines) {
      const tokens = line.split(/\s+/).filter(Boolean);
      const maxTokenLen = tokens.reduce((m, tok) => Math.max(m, tok.length), 0);
      if (maxTokenLen > MAX_ROW_CHARS) return false;

      const len = line.length;
      estimatedRows += Math.max(1, Math.ceil(len / MAX_ROW_CHARS));
      if (estimatedRows > MAX_ROWS) return false;
    }

    return estimatedRows <= MAX_ROWS;
  });
}


// ===== Minimal Markdown renderer (offline-friendly) =====
// Supports: **bold**, `inline code`, [text](url), bullet/number lists, headings (#..###), blockquotes (>), fenced code blocks (```).
// Raw HTML is escaped for safety.
function escapeHtml(s) {
  return String(s ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function mdInline(raw) {
  let s = escapeHtml(raw);

  // links
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, txt, url) =>
    `<a class="md-link" href="${url}" target="_blank" rel="noopener">${txt}</a>`
  );

  // inline code
  s = s.replace(/`([^`]+)`/g, (_m, code) => `<code>${code}</code>`);

  // bold
  s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

  // italic (light)
  s = s.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>");

  return s;
}

function mdBlock(raw) {
  const src = String(raw ?? "").replace(/\r\n?/g, "\n");

  // IMPORTANT: Don't pre-escape the whole block.
  // mdInline() already escapes. If we escape here too, entities like "&quot;" become "&amp;quot;" and show up literally.

  // fence blocks -> placeholders first (on RAW)
  const fences = [];
  let md = src.replace(/```([a-zA-Z0-9_-]+)?\n([\s\S]*?)```/g, (_m, lang, code) => {
    const idx = fences.length;
    const safeLang = String(lang || "").replace(/[^a-zA-Z0-9_-]/g, "");
    fences.push({ lang: safeLang, code: escapeHtml(code) });
    return `@@FENCE${idx}@@`;
  });

  const lines = md.split("\n");
  const out = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (line.trim() === "") {
      i++;
      continue;
    }

    // heading # .. ###
    const hm = line.match(/^(#{1,3})\s+(.*)$/);
    if (hm) {
      const lvl = hm[1].length;
      out.push(`<h${lvl} class="md-h${lvl}">${mdInline(hm[2])}</h${lvl}>`);
      i++;
      continue;
    }

    // blockquote
    if (/^\s*>\s+/.test(line)) {
      const q = [];
      while (i < lines.length && /^\s*>\s+/.test(lines[i])) {
        q.push(lines[i].replace(/^\s*>\s+/, ""));
        i++;
      }
      out.push(
        `<blockquote class="md-quote">${mdInline(q.join("\n")).replace(/\n/g, "<br>")}</blockquote>`
      );
      continue;
    }

    // unordered list
    if (/^\s*[-*]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*[-*]\s+/, ""));
        i++;
      }
      out.push(
        `<ul class="md-ul">${items.map((it) => `<li>${mdInline(it)}</li>`).join("")}</ul>`
      );
      continue;
    }

    // ordered list
    if (/^\s*\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*\d+\.\s+/, ""));
        i++;
      }
      out.push(
        `<ol class="md-ol">${items.map((it) => `<li>${mdInline(it)}</li>`).join("")}</ol>`
      );
      continue;
    }

    // markdown table (simple)
    const isTableRow = (s) => /\|/.test(s);
    const isSepRow = (s) => /^\s*\|?\s*:?-{3,}:?(?:\s*\|\s*:?-{3,}:?)*\s*\|?\s*$/.test(s);
    if (isTableRow(line) && i + 1 < lines.length && isSepRow(lines[i + 1])) {
      const head = line;
      const sep = lines[i + 1];
      i += 2;
      const body = [];
      while (i < lines.length && lines[i].trim() !== "" && isTableRow(lines[i])) {
        body.push(lines[i]);
        i++;
      }

      const parseRow = (row) =>
        row
          .trim()
          .replace(/^\|/, "")
          .replace(/\|$/, "")
          .split("|")
          .map((c) => mdInline(c.trim()));

      const headCells = parseRow(head);
      const bodyRows = body.map(parseRow);

      const thead = `<thead><tr>${headCells
        .map((c) => `<th>${c}</th>`)
        .join("")}</tr></thead>`;
      const tbody = `<tbody>${bodyRows
        .map(
          (r) => `<tr>${r.map((c) => `<td>${c}</td>`).join("")}</tr>`
        )
        .join("")}</tbody>`;

      out.push(`<table class="md-table">${thead}${tbody}</table>`);
      continue;
    }

    // paragraph (until blank line / next block opener)
    const buf = [line];
    i++;
    while (
      i < lines.length &&
      lines[i].trim() !== "" &&
      !/^(#{1,3})\s+/.test(lines[i]) &&
      !/^\s*>\s+/.test(lines[i]) &&
      !/^\s*[-*]\s+/.test(lines[i]) &&
      !/^\s*\d+\.\s+/.test(lines[i])
    ) {
      buf.push(lines[i]);
      i++;
    }
    const p = mdInline(buf.join("\n")).replace(/\n/g, "<br>");
    out.push(`<p class="md-p">${p}</p>`);
  }

  let html = out.join("");

  // restore fences
  html = html.replace(/@@FENCE(\d+)@@/g, (_m, n) => {
    const f = fences[Number(n)];
    const langAttr = f.lang ? ` data-lang="${f.lang}"` : "";
    return `<pre class="md-fence"${langAttr}><code>${f.code}</code></pre>`;
  });

  return html;
}


function setMD(node, raw, mode = "block") {
  node.innerHTML = mode === "inline" ? mdInline(raw) : mdBlock(raw);
}

function buildMediaBlock(media) {
  const items = Array.isArray(media) ? media : [];
  if (!items.length) return null;

  const wrap = el("div", "media-block");
  items.forEach((m) => {
    if (!m || m.type !== "image" || !m.src) return;
    const fig = el("figure", "media-figure");
    const img = document.createElement("img");
    img.src = m.src;
    img.alt = m.alt || "";
    img.addEventListener("error", () => {
      fig.remove();
    });
    fig.appendChild(img);
    if (m.caption) {
      const cap = el("figcaption", "media-caption", m.caption);
      fig.appendChild(cap);
    }
    wrap.appendChild(fig);
  });
  return wrap.childElementCount ? wrap : null;
}

function buildConceptPage(set, variant, bucket) {
  const concepts = Array.isArray(set?.concepts) ? set.concepts : [];
  if (!concepts.length) return null;

  const maxLineLen = concepts.reduce((max, c) => {
    const text = String(c?.algorithm || "")
      .replace(/```[\s\S]*?```/g, (m) => m.replace(/```/g, ""))
      .replace(/\r/g, "");
    const lines = text.split("\n");
    const localMax = lines.reduce((m, line) => Math.max(m, line.length), 0);
    return Math.max(max, localMax);
  }, 0);

  const page = el("div", "concept-page");
  if (maxLineLen > 60) page.classList.add("concept-cols-1");
  else page.classList.add("concept-cols-2");

  const header = el("div", "page-header");
  const left = el("div", "meta-left");
  left.appendChild(el("div", "page-title", `${set.title || "학습지"} · 핵심 개념`));

  const row = el("div", "meta-row");
  row.appendChild(metaField("학생", "name", "w80"));
  row.appendChild(metaField("배부일", "dist", "", ymd()));
  row.appendChild(metaField("제출일", "due", "w80"));
  left.appendChild(row);

  const rowInfo = el("div", "meta-row");
  rowInfo.appendChild(el("div", "", `범위: ${bucket}`));
  rowInfo.appendChild(el("div", "", `유형: ${variant === "teacher" ? "선생님용" : "학생용"}`));
  left.appendChild(rowInfo);

  const right = el("div", "meta-right");
  right.innerHTML = `<div>${ymd()}</div>`;
  header.appendChild(left);
  header.appendChild(right);
  page.appendChild(header);

  const block = el("div", "concept-block");
  concepts.forEach((c) => {
    const item = el("div", "concept-item");
    const title = el("h3", "", c.title || "개념");
    item.appendChild(title);

    const summary = el("div", "concept-summary md");
    setMD(summary, c.summary || "", "block");
    item.appendChild(summary);

    if (c.example) {
      const example = el("div", "concept-example md");
      setMD(example, c.example || "", "block");
      item.appendChild(example);
    }
    if (c.algorithm) {
      const algo = el("div", "concept-algorithm md");
      setMD(algo, c.algorithm || "", "block");
      item.appendChild(algo);
    }
    const media = buildMediaBlock(c.media);
    if (media) item.appendChild(media);
    block.appendChild(item);
  });

  page.appendChild(block);
  return page;
}

let theoryIndexCache = null;

function normalizeCombinedTheoryCodeLang(raw) {
  const v = String(raw || "").toLowerCase();
  if (v === "py" || v === "python") return "python";
  if (v === "c" || v === "c99" || v === "c11") return "c";
  if (v === "java") return "java";
  if (v === "cs" || v === "c#" || v === "csharp") return "csharp";
  return v;
}

function detectCombinedTheoryLangFromCode(codeEl) {
  const classes = Array.from(codeEl.classList || []);
  for (const cls of classes) {
    if (!cls.startsWith("language-")) continue;
    return normalizeCombinedTheoryCodeLang(cls.replace("language-", ""));
  }
  const pre = codeEl.closest("pre");
  if (pre && pre.dataset && pre.dataset.lang) {
    return normalizeCombinedTheoryCodeLang(pre.dataset.lang);
  }
  return "";
}

function parseCombinedTheoryIoFenceText(rawText) {
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

function parseCombinedTheoryTraceGridFenceText(rawText) {
  const lines = String(rawText || "").replace(/\r\n?/g, "\n").split("\n");
  const conf = { title: "", columns: [], rows: [] };
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

function buildCombinedTheoryIoExampleBlock(io) {
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

function findCombinedLastHeadingInNode(node) {
  if (!node) return null;
  if (/^H[1-6]$/.test(node.tagName || "")) return node;
  if (!node.querySelectorAll) return null;
  const hs = node.querySelectorAll("h1, h2, h3, h4, h5, h6");
  return hs.length ? hs[hs.length - 1] : null;
}

function findCombinedNearestPreviousHeadingText(root, startEl) {
  let cursor = startEl;
  while (cursor && cursor !== root) {
    let prev = cursor.previousElementSibling;
    while (prev) {
      const h = findCombinedLastHeadingInNode(prev);
      if (h) return String(h.textContent || "");
      prev = prev.previousElementSibling;
    }
    cursor = cursor.parentElement;
  }
  return "";
}

function isCombinedPracticeLinkedSectionByHeading(text) {
  return /연계\s*실습/.test(String(text || ""));
}

function isCombinedIoLabelParagraph(el) {
  if (!el || el.tagName !== "P") return false;
  const raw = String(el.textContent || "").trim();
  return /^예상\s*(입력\s*\/\s*출력|출력)\s*[:：]?\s*$/i.test(raw);
}

function buildCombinedTheoryTraceGridBlock(conf) {
  const wrap = document.createElement("div");
  wrap.className = "theory-trace-grid";

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

function enhanceCombinedTheoryIoBlocks(contentEl) {
  const candidates = contentEl.querySelectorAll("pre > code");
  candidates.forEach((codeEl) => {
    const lang = detectCombinedTheoryLangFromCode(codeEl);
    if (!["io", "inout", "exampleio"].includes(lang)) return;
    const pre = codeEl.closest("pre");
    if (!pre) return;
    const headingText = findCombinedNearestPreviousHeadingText(contentEl, pre);
    const inPractice = isCombinedPracticeLinkedSectionByHeading(headingText);
    const io = parseCombinedTheoryIoFenceText(codeEl.textContent || "");
    if (inPractice) {
      const prev = pre.previousElementSibling;
      if (isCombinedIoLabelParagraph(prev)) prev.remove();
      pre.remove();
      return;
    }
    pre.replaceWith(
      buildCombinedTheoryIoExampleBlock(io)
    );
  });
}

function enhanceCombinedTheoryTraceGridBlocks(contentEl) {
  const candidates = contentEl.querySelectorAll("pre > code");
  candidates.forEach((codeEl) => {
    const lang = detectCombinedTheoryLangFromCode(codeEl);
    if (!["tracegrid", "trace-grid", "gridtrace"].includes(lang)) return;
    const pre = codeEl.closest("pre");
    if (!pre) return;
    const conf = parseCombinedTheoryTraceGridFenceText(codeEl.textContent || "");
    if (!conf) return;
    pre.replaceWith(buildCombinedTheoryTraceGridBlock(conf));
  });
}

function isCombinedMiniCheckHeadingText(text) {
  return /미니\s*체크/.test(String(text || ""));
}

function isCombinedMiniCheckLabel(el, kind) {
  if (!el || el.tagName !== "P") return false;
  const raw = String(el.textContent || "").trim();
  if (kind === "questions") return /^문항\s*[:：]?\s*$/i.test(raw);
  if (kind === "answers") return /^답안\s*작성\s*[:：]?\s*$/i.test(raw);
  return false;
}

function buildPrintMiniCheckAnswerSheet(questionList) {
  const wrap = document.createElement("div");
  wrap.className = "theory-mini-check-print-sheet";

  const title = document.createElement("div");
  title.className = "theory-mini-check-print-title";
  title.textContent = "답안 작성란";
  wrap.appendChild(title);

  const items = Array.from(questionList?.querySelectorAll(":scope > li") || []);
  items.forEach((_, idx) => {
    const row = document.createElement("div");
    row.className = "theory-mini-check-print-row";

    const no = document.createElement("span");
    no.className = "theory-mini-check-print-no";
    no.textContent = `${idx + 1}.`;

    const answer = document.createElement("span");
    answer.className = "theory-mini-check-print-line";
    answer.textContent = "정답: ____________________";

    const reason = document.createElement("span");
    reason.className = "theory-mini-check-print-line";
    reason.textContent = "근거: ________________________________";

    row.append(no, answer, reason);
    wrap.appendChild(row);
  });

  return wrap;
}

function enhanceCombinedTheoryMiniCheckSection(contentEl) {
  const heads = Array.from(contentEl.querySelectorAll("h2, h3"));
  const starts = heads.filter((h) =>
    isCombinedMiniCheckHeadingText(h.textContent || "")
  );
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

    const card = document.createElement("section");
    card.className = "theory-mini-check-card theory-mini-check-card--print";
    blockNodes[0].parentNode.insertBefore(card, blockNodes[0]);
    blockNodes.forEach((node) => card.appendChild(node));

    const qLabel = Array.from(card.querySelectorAll("p")).find((p) =>
      isCombinedMiniCheckLabel(p, "questions")
    );
    const qList =
      qLabel && qLabel.nextElementSibling && qLabel.nextElementSibling.tagName === "OL"
        ? qLabel.nextElementSibling
        : null;

    const aLabel = Array.from(card.querySelectorAll("p")).find((p) =>
      isCombinedMiniCheckLabel(p, "answers")
    );
    const aList =
      aLabel && aLabel.nextElementSibling && aLabel.nextElementSibling.tagName === "OL"
        ? aLabel.nextElementSibling
        : null;

    if (qLabel) qLabel.remove();
    if (aLabel) aLabel.remove();
    if (aList) aList.remove();

    if (qList) {
      const answerSheet = buildPrintMiniCheckAnswerSheet(qList);
      card.appendChild(answerSheet);
    }
  });
}

function enhanceCombinedTheoryCodeBlocks(contentEl) {
  const codeBlocks = contentEl.querySelectorAll("pre > code");
  codeBlocks.forEach((codeEl) => {
    const lang = detectCombinedTheoryLangFromCode(codeEl);
    const pre = codeEl.closest("pre");
    if (!pre) return;
    pre.classList.add("theory-code");
    if (lang === "python" || lang === "c" || lang === "java" || lang === "csharp") {
      codeEl.className = `language-${lang}`;
    }
  });

  if (window.Prism && typeof window.Prism.highlightAllUnder === "function") {
    window.Prism.highlightAllUnder(contentEl);
  }
}

function isCombinedTheoryExampleHeader(el) {
  if (!el || el.tagName !== "P") return false;
  const strong = el.querySelector("strong:only-child");
  if (!strong) return false;
  const txt = String(strong.textContent || "").trim();
  return /예시/.test(txt);
}

function enhanceCombinedTheoryExampleBlocks(contentEl) {
  const containers = [contentEl, ...Array.from(contentEl.querySelectorAll(".theory-section-block"))];
  containers.forEach((root) => {
    const nodes = Array.from(root.children || []);
    if (!nodes.length) return;

    let i = 0;
    while (i < nodes.length) {
      const cur = nodes[i];
      if (!isCombinedTheoryExampleHeader(cur)) {
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
        if (isCombinedTheoryExampleHeader(next)) break;
        if (/^H[1-6]$/.test(next.tagName)) break;
        wrap.appendChild(next);
      }

      i += 1;
    }
  });
}

function attachCombinedTrailingExampleBlocks(contentEl) {
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

function enhanceCombinedTheoryMarkdownTables(contentEl) {
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

function applyCombinedTheoryViewFilter(contentEl, variant) {
  const children = Array.from(contentEl.children || []);
  let currentView = "student";

  children.forEach((el) => {
    const tag = String(el.tagName || "").toUpperCase();
    if (/^H[1-6]$/.test(tag)) {
      const raw = String(el.textContent || "").trim();
      const m = raw.match(/^\{view:(teacher|student)\}\s*/i);
      if (m) {
        currentView = m[1].toLowerCase();
        el.textContent = raw.replace(/^\{view:(teacher|student)\}\s*/i, "");
      } else if (/^\s*메타\s*$/i.test(raw)) {
        currentView = "teacher";
      }
    }
    el.dataset.view = currentView;
  });

  const hideTeacher = String(variant || "student").toLowerCase() !== "teacher";
  if (!hideTeacher) return;
  children.forEach((el) => {
    if (el.dataset.view === "teacher") el.remove();
  });
}

function renderCombinedTheoryMarkdown(target, mdText, variant) {
  const raw = String(mdText || "");
  if (!window.markdownit || !window.DOMPurify) {
    setMD(target, raw, "block");
  } else {
    const md = window.markdownit({
      html: true,
      linkify: true,
      breaks: true,
    });
    const safe = window.DOMPurify.sanitize(md.render(raw));
    target.innerHTML = safe;
  }

  applyCombinedTheoryViewFilter(target, variant);
  applyCombinedTheoryDataImageFallbacks(target);
  enhanceCombinedTheoryMiniCheckSection(target);
  enhanceCombinedTheoryIoBlocks(target);
  enhanceCombinedTheoryTraceGridBlocks(target);
  enhanceCombinedTheoryMarkdownTables(target);
  enhanceCombinedTheoryCodeBlocks(target);
  enhanceCombinedTheoryExampleBlocks(target);
  attachCombinedTrailingExampleBlocks(target);
}

function resolveCombinedTheoryDataPathSuffix(src) {
  const s = String(src || "").trim();
  if (s.startsWith("./data/")) return s.slice("./data/".length);
  if (s.startsWith("/data/")) return s.slice("/data/".length);
  if (s.startsWith("/practice/data/")) return s.slice("/practice/data/".length);
  if (s.startsWith("data/")) return s.slice("data/".length);
  return "";
}

function buildCombinedTheoryDataPathCandidates(src) {
  const suffix = resolveCombinedTheoryDataPathSuffix(src);
  if (!suffix) return [];
  return [`./data/${suffix}`, `/data/${suffix}`, `/practice/data/${suffix}`];
}

function applyCombinedTheoryDataImageFallbacks(root) {
  const imgs = root.querySelectorAll("img[src]");
  imgs.forEach((img) => {
    const original = String(img.getAttribute("src") || "").trim();
    const candidates = buildCombinedTheoryDataPathCandidates(original).filter((v) => v !== original);
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

async function loadTheoryIndexCached() {
  if (theoryIndexCache) return theoryIndexCache;
  try {
    theoryIndexCache = await ProblemService.listTheoryIndex();
  } catch (_) {
    theoryIndexCache = [];
  }
  return theoryIndexCache;
}

async function loadTheoryMarkdownForSet(set) {
  const categoryId = String(set?.categoryId || "");
  if (!categoryId) return null;

  const index = await loadTheoryIndexCached();
  const entry = (Array.isArray(index) ? index : []).find(
    (item) => item && item.categoryId === categoryId && item.mdPath
  );
  if (!entry || !entry.mdPath) return null;

  try {
    const res = await fetch(entry.mdPath);
    if (!res.ok) return null;
    const mdText = await res.text();
    return {
      title: entry.title || "이론",
      mdText,
    };
  } catch (_) {
    return null;
  }
}

function buildTheoryMarkdownPage(set, theory, variant, bucket, theoryLayout) {
  if (!theory || !theory.mdText) return null;

  const page = el("div", "concept-page theory-md-page");
  if (theoryLayout === "double") page.classList.add("theory-layout-double");
  else page.classList.add("theory-layout-single");

  const header = el("div", "page-header");
  const left = el("div", "meta-left");
  left.appendChild(el("div", "page-title", `${theory.title || set?.title || "이론"} · 이론`));

  const row = el("div", "meta-row");
  row.appendChild(metaField("학생", "name", "w80"));
  row.appendChild(metaField("배부일", "dist", "", ymd()));
  row.appendChild(metaField("제출일", "due", "w80"));
  left.appendChild(row);

  const rowInfo = el("div", "meta-row");
  rowInfo.appendChild(el("div", "", `범위: ${bucket}`));
  rowInfo.appendChild(el("div", "", `유형: ${variant === "teacher" ? "선생님용" : "학생용"}`));
  rowInfo.appendChild(el("div", "", `레이아웃: ${theoryLayout === "double" ? "2열" : "1열"}`));
  left.appendChild(rowInfo);

  const right = el("div", "meta-right");
  right.innerHTML = `<div>${ymd()}</div>`;
  header.appendChild(left);
  header.appendChild(right);
  page.appendChild(header);

  const block = el("section", "theory-md-block md");
  renderCombinedTheoryMarkdown(block, theory.mdText, variant);
  page.appendChild(block);
  return page;
}

function shouldMcqCodeOptionsUseTwoColumns(q) {
  const opts = Array.isArray(q?.options) ? q.options : [];
  if (opts.length < 4) return false;
  if (opts.length > 6) return false;

  // ✅ 코드박스는 2열에서 폭이 더 좁아지므로 텍스트보다 보수적으로
  const MAX_ROWS = 18;          // (래핑 포함) 옵션 1개당 허용 "보이는 줄" 총합
  const MAX_ROW_CHARS = 28;    // 한 줄이 이 길이를 넘으면 래핑된다고 가정
  const MAX_TOKEN_CHARS = 28;  // 공백 없는 덩어리(긴 식별자/문자열)가 너무 길면 2열 금지
  const MAX_PHYSICAL_LINES = 18; // 실제 개행 줄 수 하드캡

  const normalize = (s) =>
    String(s ?? "")
      .replace(/\r\n/g, "\n")
      .trim();

  return opts.every((o) => {
    const t = normalize(o);
    if (!t) return true;

    const physicalLines = t.split("\n");
    if (physicalLines.length > MAX_PHYSICAL_LINES) return false;

    let estimatedRows = 0;
    for (const line of physicalLines) {
      const tokens = line.split(/\s+/).filter(Boolean);
      const maxTokenLen = tokens.reduce((m, tok) => Math.max(m, tok.length), 0);
      if (maxTokenLen > MAX_TOKEN_CHARS) return false;

      const len = line.length;
      estimatedRows += Math.max(1, Math.ceil(len / MAX_ROW_CHARS));
      if (estimatedRows > MAX_ROWS) return false;
    }
    return true;
  });
}


function buildProblemCard(set, q, originalIndex, variant) {
  const card = el("section", "p-card");

  const head = el("div", "p-head");
  const headMain = el("div", "p-head-main");
  const title = el("div", "p-head-title md md-inline");
  setMD(title, `${originalIndex + 1}. ${q.title || "문제"}`, "inline");
  headMain.appendChild(title);

  const conceptTitles = getQuestionConceptTitlesForPrint(set, q);
  if (conceptTitles.length) {
    const conceptChip = el("div", "p-concept-chip md md-inline");
    setMD(conceptChip, conceptTitles.join(", "), "inline");
    headMain.appendChild(conceptChip);
  }

  head.appendChild(headMain);
  head.appendChild(el("div", "p-type", typeLabel(q)));
  card.appendChild(head);


  const rawDesc = q.description || "";
  const tableOnly = extractFirstMarkdownTable(rawDesc);
  const descText = tableOnly ? removeFirstMarkdownTable(rawDesc) : rawDesc;
  const { main: descMain, view: descView } = splitDescriptionForView(descText);

  if (descMain) {
    const desc = el("div", "p-desc md");
    setMD(desc, descMain, "block");
    card.appendChild(desc);
  }

  if (descView) {
    const viewWrap = el("div", "p-view");
    viewWrap.appendChild(el("div", "p-view-title", "보기"));
    const viewBody = el("div", "p-view-body md");
    setMD(viewBody, descView, "block");
    viewWrap.appendChild(viewBody);
    card.appendChild(viewWrap);
  }

  if (tableOnly) {
    const tableBlock = el("div", "p-desc p-desc--table md");
    setMD(tableBlock, tableOnly, "block");
    card.appendChild(tableBlock);
  }

  if (q.code) {
    const pre = buildHighlightedCodePre(set, "p-code", q.code, true);
    card.appendChild(pre);
  }

  if (q.ioExample && (q.ioExample.input || q.ioExample.output)) {
    const io = el("div", "p-io");
    io.appendChild(el("div", "p-io-title", "입력/출력 예시"));

    const grid = el("div", "p-io-grid");
    const inBox = el("div", "p-io-box");
    inBox.appendChild(el("div", "p-io-label", "입력"));
    const inPre = el("pre", "p-io-pre", q.ioExample.input || "(입력 없음)");
    inBox.appendChild(inPre);

    const outBox = el("div", "p-io-box");
    outBox.appendChild(el("div", "p-io-label", "출력"));
    const outPre = el("pre", "p-io-pre", q.ioExample.output || "(출력 없음)");
    outBox.appendChild(outPre);

    grid.appendChild(inBox);
    grid.appendChild(outBox);
    io.appendChild(grid);
    card.appendChild(io);
  }

  const media = buildMediaBlock(q.media);
  if (media) card.appendChild(media);

if (q.type === "mcq") {
  const opts = el("div", "p-options");

  // ✅ 이미 있는 코드: 옵션에 줄바꿈이 하나라도 있으면 코드박스 모드
  const forceOptCodeBox = (q.options || []).some(v => String(v ?? "").includes("\n"));

  // ✅ (추가) grid2 판단: 텍스트면 기존 룰, 코드박스면 코드박스 전용 룰
  const useGrid2 = forceOptCodeBox
    ? shouldMcqCodeOptionsUseTwoColumns(q)
    : shouldMcqOptionsUseTwoColumns(q);

  if (useGrid2) opts.classList.add("p-options--grid2");

  (q.options || []).forEach((t, i) => {
    const row = el("div", "p-opt");
    const labels = q.optionLabels || [];
    const letter = labels[i] || String.fromCharCode(65 + i);

    row.appendChild(el("div", "bullet", `◯ ${letter}`));

    const tdiv = el("div", "text md");
    const opt = String(t ?? "");

    if (forceOptCodeBox || opt.includes("\n")) {
      const pre = buildHighlightedCodePre(set, "p-code opt-code", opt, false);
      tdiv.appendChild(pre);
    } else {
      tdiv.classList.add("md-inline");
      setMD(tdiv, opt, "inline");
    }

    row.appendChild(tdiv);
    opts.appendChild(row);
  });

  card.appendChild(opts);
}
  const answer = el("div", "answer-block");

if (q.type === "mcq") {
  answer.appendChild(el("div", "answer-label", "이유(간단히):"));
  const lines = el("div", "answer-lines");
  lines.style.setProperty("--n", "1.2");
  answer.appendChild(lines);

} else if (q.type === "short") {
  if (isGridQuestion(q)) {
    answer.appendChild(el("div", "answer-label", "표:"));
    answer.appendChild(buildGridAnswerTable(q, variant));
  } else {
    answer.appendChild(el("div", "answer-label", "답:"));
    const lines = el("div", "answer-lines");
    lines.style.setProperty("--n", "1.5");
    answer.appendChild(lines);
  }

} else if (q.type === "code") {
  if (isCondBlankQuestion(q)) {
    answer.appendChild(el("div", "answer-label", "조건식(한 줄):"));
    const lines = el("div", "answer-lines");
    lines.style.setProperty("--n", "1.5");
    answer.appendChild(lines);
  } else {
    answer.appendChild(el("div", "answer-label", "코드:"));
    const box = el("div", "answer-lines codebox");
    box.style.setProperty("--n", "3");
    answer.appendChild(box);
  }
}

  if (variant === "teacher") {
    const note = el("div", "teacher-note");
    const a = correctForTeacher(q);
    if (a) {
      const k = el("span", "k", "정답/기준: ");
      const v = el("span", "", a.replace(/^정답:\s*/, ""));
      note.appendChild(k);
      note.appendChild(v);
    }
    if (q.hint) {
      const br = document.createElement("div");
      br.style.marginTop = "1mm";
      br.appendChild(el("span", "k", "힌트: "));
      const h = el("span", "md md-inline");
      setMD(h, String(q.hint), "inline");
      br.appendChild(h);
      note.appendChild(br);
    }
    card.appendChild(note);
  }

  card.appendChild(answer);
  return card;
}

function buildProblemSplitCards(set, q, originalIndex, variant) {
  const codeText = String(q?.code || "");
  const codeLines = codeText ? codeText.replace(/\r\n?/g, "\n").split("\n") : [];
  const useCodeContinuation = codeLines.length >= CODE_SPLIT_MIN_LINES;
  const splitAt = useCodeContinuation ? Math.ceil(codeLines.length / 2) : codeLines.length;
  const leftCode = useCodeContinuation ? codeLines.slice(0, splitAt).join("\n") : codeText;
  const rightCode = useCodeContinuation ? codeLines.slice(splitAt).join("\n") : "";

  const left = buildProblemCard(set, q, originalIndex, variant);
  left.classList.add("p-card--split", "p-card--split-left");
  if (useCodeContinuation) {
    const leftCodeNode = left.querySelector("pre.p-code code");
    if (leftCodeNode) leftCodeNode.textContent = leftCode;
  }
  left.querySelectorAll(".p-options, .answer-block").forEach((n) => n.remove());
  const leftTeacher = left.querySelector(".teacher-note");
  if (leftTeacher) leftTeacher.remove();

  const right = buildProblemCard(set, q, originalIndex, variant);
  right.classList.add("p-card--split", "p-card--split-right");
  right.querySelectorAll(".p-desc, .p-view, .p-desc--table, .p-io, .media-block").forEach((n) => n.remove());
  if (useCodeContinuation) {
    const existingCodeWrap = right.querySelector(".p-code");
    if (existingCodeWrap) existingCodeWrap.remove();
    if (rightCode.trim()) {
      const rightCodePre = buildHighlightedCodePre(set, "p-code p-code--cont", rightCode, true);
      if (currentShowLineNumbers) {
        rightCodePre.setAttribute("data-start", String(splitAt + 1));
      }
      const options = right.querySelector(".p-options");
      if (options) right.insertBefore(rightCodePre, options);
      else right.appendChild(rightCodePre);
    }
  } else {
    right.querySelectorAll(".p-code").forEach((n) => n.remove());
  }
  const t = right.querySelector(".p-head-title");
  if (t) t.textContent = `${originalIndex + 1}. 선택지`;
  const chip = right.querySelector(".p-concept-chip");
  if (chip) chip.remove();
  const tp = right.querySelector(".p-type");
  if (tp) tp.textContent = "분할";

  return { left, right };
}

function buildProblemSplitCard(set, q, originalIndex, variant, side) {
  const pair = buildProblemSplitCards(set, q, originalIndex, variant);
  return side === "right" ? pair.right : pair.left;
}

function metaField(label, key, extraClass, defaultValue = "") {
  const wrap = el("div", "meta-field");
  wrap.appendChild(el("span", "", `${label}:`));
  const input = document.createElement("input");
  input.className = `meta-input ${extraClass || ""}`.trim();
  input.type = "text";
  input.value = defaultValue;
  input.setAttribute("data-meta", key);
  wrap.appendChild(input);
  return wrap;
}

// (2) buildPage() : 메타(학생/반/번호/배부일/제출일) + docid는 1페이지에만
/* [print.markdown.js] 위치: buildPage()를 "2열 컬럼 컨테이너" 방식으로 수정 */

function buildPage(setId, set, pageIndex, pageCount, problems, indexMap, variant, bucket, layout = "double") {
  const page = el("div", "print-page");

  const header = el("div", "page-header");
  const left = el("div", "meta-left");
  left.appendChild(el("div", "page-title", `${set.title || "학습지"} · ${variant === "teacher" ? "선생님용" : "학생용"}`));

  // (원하면) 1페이지만 상세 메타, 나머지는 타이틀+페이지번호만 남기는 로직을 여기에 적용
  const row = el("div", "meta-row");
  // ✅ 1페이지만 상세 메타 출력
  if (pageIndex === 0) {
    const row = el("div", "meta-row");
    row.appendChild(metaField("학생", "name", "w80"));
    // row.appendChild(metaField("반", "class", ""));
    // row.appendChild(metaField("번호", "no", ""));
    row.appendChild(metaField("배부일", "dist", "", ymd()));
    row.appendChild(metaField("제출일", "due", "w80"));
    left.appendChild(row);
  } else {
    header.classList.add("page-header--compact"); // (선택) CSS로 높이 줄이기
  }

  // [print.markdown.js] buildPage() 안에서 right.innerHTML 부분만 교체 (docid는 1페이지만)
  const right = el("div", "meta-right");
  if (pageIndex === 0) {
    right.innerHTML = `
      <div>페이지 ${pageIndex + 1} / ${pageCount}</div>
      <div class="docid">${makeDocId(setId, bucket, variant)}</div>
    `;
  } else {
    right.innerHTML = `<div>페이지 ${pageIndex + 1} / ${pageCount}</div>`;
  }

  header.appendChild(left);
  header.appendChild(right);
  page.appendChild(header);

  // ✅ grid 대신 "2열 컬럼 컨테이너"
  const grid = el("div", "page-grid");
  if (layout === "single") grid.classList.add("page-grid--single");

  const colL = el("div", "page-col");
  if (layout === "single") colL.classList.add("page-col--single");
  grid.appendChild(colL);

  if (layout !== "single") {
    const colR = el("div", "page-col");
    grid.appendChild(colR);
  }
  page.appendChild(grid);

  // problems는 이제 "페이지에 들어갈 카드들"만 넘긴다고 가정(렌더는 여기서만)
  problems.forEach((q) => {
    const originalIndex = indexMap.get(q.id) ?? 0;
    const card = buildProblemCard(set, q, originalIndex, variant);
    // 실제로는 renderAll에서 colL/colR에 꽂아주게 될 거라 여기서는 넣지 않음
    // (buildPage는 빈 컬럼만 만든다)
  });

  return page;
}


function updateToolbarTitle(set, bucket, variant) {
  const t = document.getElementById("pt-set-title");
  const s = document.getElementById("pt-subtitle");
  if (t) t.textContent = set?.title || "학습지";
  if (s) s.textContent = `범위: ${bucket} · 유형: ${variant}`;
}

/* [print.markdown.js] 위치: renderAll()에서 chunk(selected, 2) 부분을 "높이 기반 패킹"으로 교체 */

async function renderAll({ setId, bucket, variant }) {
  const root = document.getElementById("print-root");
  if (!root) return;

  root.innerHTML = "불러오는 중...";
  currentSetData = await ProblemService.loadSet(setId);

  const indexMap = new Map();
  (currentSetData.problems || []).forEach((q, idx) => indexMap.set(q.id, idx));

  let selected = (currentSetData.problems || []).slice();
  if (bucket === "core" || bucket === "supp") {
    selected = selected.filter((q, idx) => bucketOfQuestion(currentSetData, q, idx) === bucket);
  }

  else if (bucket === "custom") {
  const spec = qp("range"); // apply가 setQp로 넣어줌
  const parsed = parseRangeSpec(spec, (currentSetData.problems || []).length);

  if (!parsed.ok) {
    // 화면 힌트만 표시하고(인쇄물은 영향 없음), 안전하게 전체로 fallback
    const hint = document.getElementById("range-hint");
    if (hint) hint.textContent = parsed.msg;
    selected = (currentSetData.problems || []).slice();
  } else {
    const hint = document.getElementById("range-hint");
    if (hint) hint.textContent = parsed.msg;
    selected = (currentSetData.problems || []).filter((_q, idx) => parsed.set.has(idx + 1));
  }
}

  root.innerHTML = "";
  root.classList.remove("variant-student", "variant-teacher");
  root.classList.add(variant === "teacher" ? "variant-teacher" : "variant-student");

  // 문제 출력 화면은 문제만 렌더한다.

  const probeFirst = buildPage(setId, currentSetData, 0, 99, [], indexMap, variant, bucket, "double");
  root.appendChild(probeFirst);
  const bodyHFirst = getBodyHeightPx(probeFirst);

  const probeOther = buildPage(setId, currentSetData, 1, 99, [], indexMap, variant, bucket, "double");
  root.appendChild(probeOther);
  const bodyHOther = getBodyHeightPx(probeOther);

  root.removeChild(probeFirst);
  root.removeChild(probeOther);

  // 1) "빈 페이지" 하나 만들어서 폭/높이 측정
  const probePage = buildPage(setId, currentSetData, 0, 1, [], indexMap, variant, bucket, "double");
  root.appendChild(probePage);
  const probeSinglePage = buildPage(setId, currentSetData, 0, 1, [], indexMap, variant, bucket, "single");
  root.appendChild(probeSinglePage);

  const grid = probePage.querySelector(".page-grid");
  const colProbe = probePage.querySelector(".page-col");
  const singleColProbe = probeSinglePage.querySelector(".page-col");

  // 인쇄 폭(mm) 기준으로 측정 폭을 고정해 viewport 영향 제거
  const printableW = cssToPx(`calc(${PRINT_PAGE_WIDTH_MM}mm - ${PRINT_PAGE_MARGIN_MM * 2}mm)`);
  const gapPx = parseFloat(getComputedStyle(grid).gap || "0");
  const colW = colProbe ? colProbe.getBoundingClientRect().width : (printableW - gapPx) / 2;
  const fullW = singleColProbe ? singleColProbe.getBoundingClientRect().width : printableW;
  const packSafetyPx = cssToPx(`${PACKING_SAFETY_MM}mm`);
  const fitTolerancePx = cssToPx(`${FIT_TOLERANCE_MM}mm`);

  // 측정용 숨김 컨테이너
  const meas = document.createElement("div");
  meas.style.position = "absolute";
  meas.style.visibility = "hidden";
  meas.style.left = "-10000px";
  meas.style.top = "0";
  meas.style.width = `${colW}px`;
  document.body.appendChild(meas);

  // 2) 카드 높이 측정
  const heights = new Map();
  const heightsFull = new Map();
  const splitHeights = new Map();
  for (const q of selected) {
    const originalIndex = indexMap.get(q.id) ?? 0;
    const card = buildProblemCard(currentSetData, q, originalIndex, variant);
    meas.appendChild(card);
    // Measure with the same Prism-rendered DOM shape used in final output.
    applyPrismHighlight(card);
    const h = measureCardHeightPx(card, colW);
    heights.set(q.id, h);
    const hf = measureCardHeightPx(card, fullW);
    heightsFull.set(q.id, hf);
    meas.removeChild(card);
  }
  const colGapPx = parseFloat(getComputedStyle(probePage.querySelector(".page-col")).gap || "0");

  const getSplitHeights = (q) => {
    if (!q || q.type !== "mcq") return null;
    if (splitHeights.has(q.id)) return splitHeights.get(q.id);
    const originalIndex = indexMap.get(q.id) ?? 0;
    const pair = buildProblemSplitCards(currentSetData, q, originalIndex, variant);
    meas.appendChild(pair.left);
    applyPrismHighlight(pair.left);
    const lh = measureCardHeightPx(pair.left, colW);
    meas.removeChild(pair.left);
    meas.appendChild(pair.right);
    applyPrismHighlight(pair.right);
    const rh = measureCardHeightPx(pair.right, colW);
    meas.removeChild(pair.right);
    const v = { left: lh, right: rh };
    splitHeights.set(q.id, v);
    return v;
  };


  // probe 제거
  root.removeChild(probePage);
  root.removeChild(probeSinglePage);
  meas.remove();

    // ✅ vertical gap(열 내부 카드 간격) px 구하기
  // const colGapPx = parseFloat(getComputedStyle(probePage.querySelector(".page-col")).gap || "0");

  // ✅ 3) 순차 배치 기반 패킹
  // - 새 페이지는 1번(왼쪽 상단) -> 2번(오른쪽 상단) 우선
  // - 이후는 "마지막 배치된 컬럼 아래" 우선
  // - 단, 왼쪽 2행이 비어 있으면(좌 1개 + 우 1개) 왼쪽 아래 우선
  const pages = [];

  const makeDoublePage = () => ({
    layout: "double",
    left: [],
    right: [],
    leftH: 0,
    rightH: 0,
    lastCol: null
  });

  const makeNormalItem = (q) => ({ kind: "normal", q });
  const makeSplitItem = (q, side) => ({ kind: "split", q, side });

  const pageFitLimit = (pageIndex) => {
    const bodyHPage = pageIndex === 0 ? bodyHFirst : bodyHOther;
    return Math.max(0, bodyHPage - packSafetyPx) + fitTolerancePx;
  };

  const colNextHeight = (curH, curCount, qh) => {
    return curH + (curCount > 0 ? colGapPx : 0) + qh;
  };

  const isWideCandidate = (q, fitLimit) => {
    if (!q) return false;
    const hCol = heights.get(q.id) ?? 0;
    const hFull = heightsFull.get(q.id) ?? 0;
    return hCol > fitLimit && hFull <= fitLimit;
  };

  const canPlaceSplitPair = (page, q, fitLimit) => {
    if (!q || q.type !== "mcq" || page.layout === "single") return false;
    const sh = getSplitHeights(q);
    if (!sh) return false;
    const nextLeft = colNextHeight(page.leftH, page.left.length, sh.left);
    const nextRight = colNextHeight(page.rightH, page.right.length, sh.right);
    return nextLeft <= fitLimit && nextRight <= fitLimit;
  };

  const placeIntoColumn = (page, col, item, h) => {
    if (col === "left") {
      page.left.push(item);
      page.leftH = colNextHeight(page.leftH, page.left.length - 1, h);
      page.lastCol = "left";
      return;
    }
    page.right.push(item);
    page.rightH = colNextHeight(page.rightH, page.right.length - 1, h);
    page.lastCol = "right";
  };

  for (let qi = 0; qi < selected.length; qi++) {
    const q = selected[qi];
    const isLastQuestion = qi === selected.length - 1;
    let placed = false;
    while (!placed) {
      if (!pages.length) pages.push(makeDoublePage());
      let page = pages[pages.length - 1];
      const pageIndex = pages.length - 1;
      const fitLimit = pageFitLimit(pageIndex);
      const qh = heights.get(q.id) ?? 0;

      if (page.layout === "single") {
        pages.push(makeDoublePage());
        continue;
      }

      if (isWideCandidate(q, fitLimit)) {
        if (!page.left.length && !page.right.length) {
          pages[pages.length - 1] = { layout: "single", single: [q] };
          placed = true;
          break;
        }
        pages.push({ layout: "single", single: [q] });
        placed = true;
        break;
      }

      const canLeft = colNextHeight(page.leftH, page.left.length, qh) <= fitLimit;
      const canRight = colNextHeight(page.rightH, page.right.length, qh) <= fitLimit;
      const canSplitPair = canPlaceSplitPair(page, q, fitLimit);

      // 긴 문항: 1열로는 안 들어갈 때 split 우선, 그 다음 single(전체폭) 사용
      if (!canLeft && !canRight) {
        if (canSplitPair) {
          const sh = getSplitHeights(q);
          placeIntoColumn(page, "left", makeSplitItem(q, "left"), sh.left);
          placeIntoColumn(page, "right", makeSplitItem(q, "right"), sh.right);
          placed = true;
          break;
        }
        if (isWideCandidate(q, fitLimit)) {
          if (!page.left.length && !page.right.length) {
            pages[pages.length - 1] = { layout: "single", single: [q] };
          } else {
            pages.push({ layout: "single", single: [q] });
          }
          placed = true;
          break;
        }
      }

      // 새 페이지 첫 행은 좌->우를 우선
      if (!page.left.length && !page.right.length) {
        if (canLeft) {
          placeIntoColumn(page, "left", makeNormalItem(q), qh);
          placed = true;
          break;
        }
      }
      if (page.left.length === 1 && page.right.length === 0) {
        if (canRight) {
          placeIntoColumn(page, "right", makeNormalItem(q), qh);
          placed = true;
          break;
        }
        if (canLeft) {
          placeIntoColumn(page, "left", makeNormalItem(q), qh);
          placed = true;
          break;
        }
      } else {
        let chosen = null;
        const leftSecondRowEmpty = page.left.length === 1 && page.right.length >= 1;
        if (leftSecondRowEmpty && canLeft) {
          chosen = "left";
        } else if (page.lastCol === "left") {
          if (canLeft) chosen = "left";
          else if (canRight) chosen = "right";
        } else if (page.lastCol === "right") {
          if (canRight) chosen = "right";
          else if (canLeft) chosen = "left";
        } else {
          if (canLeft) chosen = "left";
          else if (canRight) chosen = "right";
        }

        if (chosen) {
          placeIntoColumn(page, chosen, makeNormalItem(q), qh);
          placed = true;
          break;
        }
      }

      // 예외: 마지막 문항이고 단일 칸 배치가 안 되며, 현재 페이지 2행 양쪽이 모두 비어 있으면 분할 배치
      if (
        isLastQuestion &&
        q.type === "mcq" &&
        page.left.length === 1 &&
        page.right.length === 1
      ) {
        const sh = getSplitHeights(q);
        if (sh) {
          const canSplitLeft = colNextHeight(page.leftH, page.left.length, sh.left) <= fitLimit;
          const canSplitRight = colNextHeight(page.rightH, page.right.length, sh.right) <= fitLimit;
          if (canSplitLeft && canSplitRight) {
            placeIntoColumn(page, "left", makeSplitItem(q, "left"), sh.left);
            placeIntoColumn(page, "right", makeSplitItem(q, "right"), sh.right);
            placed = true;
            break;
          }
        }
      }

      pages.push(makeDoublePage());
      page = pages[pages.length - 1];
      if (!page.left.length && !page.right.length) {
        const nextFit = pageFitLimit(pages.length - 1);
        if (isWideCandidate(q, nextFit)) {
          pages[pages.length - 1] = { layout: "single", single: [q] };
          placed = true;
        }
      }
    }
  }


  // 4) 실제 렌더
  const pageCount = pages.length;
  pages.forEach((p, i) => {
    const layout = p.layout || "double";
    const pageEl = buildPage(setId, currentSetData, i, pageCount, [], indexMap, variant, bucket, layout);

    const cols = pageEl.querySelectorAll(".page-col");
    const colL = cols[0];
    const colR = cols[1];

    if (layout === "single") {
      (p.single || []).forEach((q) => {
        const originalIndex = indexMap.get(q.id) ?? 0;
        colL.appendChild(buildProblemCard(currentSetData, q, originalIndex, variant));
      });
    } else {
      (p.left || []).forEach((it) => {
        const q = it?.q || it;
        const originalIndex = indexMap.get(q.id) ?? 0;
        if (it && it.kind === "split") {
          colL.appendChild(buildProblemSplitCard(currentSetData, q, originalIndex, variant, "left"));
        } else {
          colL.appendChild(buildProblemCard(currentSetData, q, originalIndex, variant));
        }
      });

      (p.right || []).forEach((it) => {
        const q = it?.q || it;
        const originalIndex = indexMap.get(q.id) ?? 0;
        if (it && it.kind === "split") {
          colR.appendChild(buildProblemSplitCard(currentSetData, q, originalIndex, variant, "right"));
        } else {
          colR.appendChild(buildProblemCard(currentSetData, q, originalIndex, variant));
        }
      });
    }

    root.appendChild(pageEl);
  });

  applyPrismHighlight(root);
  updateToolbarTitle(currentSetData, bucket, variant);
}

// [print.markdown.js] 위치: qp()/setQp() 위쪽(유틸 함수 영역) 아무 데나 추가
function parseRangeSpec(spec, maxN) {
  const raw = String(spec || "").trim();
  if (!raw) return { ok: false, set: new Set(), msg: "범위를 입력하세요. (예: 1-8,10,12-14)" };

  const out = new Set();
  const parts = raw.split(",").map(s => s.trim()).filter(Boolean);

  for (const p of parts) {
    const m = p.match(/^(\d+)\s*-\s*(\d+)$/);
    if (m) {
      let a = Number(m[1]), b = Number(m[2]);
      if (!Number.isFinite(a) || !Number.isFinite(b)) return { ok:false, set:new Set(), msg:`형식 오류: ${p}` };
      if (a > b) [a, b] = [b, a];
      for (let k = a; k <= b; k++) if (k >= 1 && k <= maxN) out.add(k);
      continue;
    }
    const n = Number(p);
    if (!Number.isFinite(n)) return { ok:false, set:new Set(), msg:`형식 오류: ${p}` };
    if (n >= 1 && n <= maxN) out.add(n);
  }

  if (out.size === 0) return { ok:false, set:new Set(), msg:"선택된 문항이 없습니다. (범위가 세트 길이를 넘었을 수 있어요)" };
  return { ok: true, set: out, msg: `선택됨: ${out.size}문항` };
}



function qp(name) {
  const p = new URLSearchParams(location.search);
  return (p.get(name) || "").trim();
}
function setQp(name, value) {
  const url = new URL(location.href);
  url.searchParams.set(name, value);
  history.replaceState(null, "", url.toString());
}

document.addEventListener("DOMContentLoaded", async () => {
  const setId = qp("set");
  if (!setId) {
    document.getElementById("print-root").textContent = "잘못된 접근입니다. (set 파라미터가 없습니다)";
    return;
  }

  const variantSel = document.getElementById("variant-select");
  const bucketSel = document.getElementById("bucket-select");
  const lineNumbersCheck = document.getElementById("line-numbers-check");

const rangeWrap = document.getElementById("range-wrap");
const rangeInput = document.getElementById("range-input");
const rangeHint = document.getElementById("range-hint");

// 초기값(쿼리스트링)
const initBucket = qp("bucket") || "all";
const initRange = qp("range") || "";
const initLineNumbers = qp("lineNumbers");
const hasInitLineNumbers = initLineNumbers === "1" || initLineNumbers === "0";

if (bucketSel) bucketSel.value = (["all","core","supp","custom"].includes(initBucket) ? initBucket : "all");
if (rangeInput) rangeInput.value = initRange;
if (lineNumbersCheck) {
  if (hasInitLineNumbers) {
    lineNumbersCheck.checked = initLineNumbers === "1";
  } else {
    lineNumbersCheck.checked = !!(variantSel && variantSel.value === "teacher");
  }
}
currentShowLineNumbers = !!(lineNumbersCheck && lineNumbersCheck.checked);

if (variantSel && lineNumbersCheck && !hasInitLineNumbers) {
  variantSel.addEventListener("change", () => {
    lineNumbersCheck.checked = variantSel.value === "teacher";
    currentShowLineNumbers = lineNumbersCheck.checked;
  });
}

// bucket 변경 시 입력칸 토글
function syncRangeUI() {
  const isCustom = (bucketSel && bucketSel.value === "custom");
  if (rangeWrap) rangeWrap.classList.toggle("is-hidden", !isCustom);
  if (rangeHint) rangeHint.textContent = "";
}
if (bucketSel) bucketSel.addEventListener("change", syncRangeUI);
syncRangeUI();

  const applyBtn = document.getElementById("apply-btn");
if (applyBtn) {
  applyBtn.addEventListener("click", async () => {
    const variant = variantSel ? variantSel.value : "student";
    const bucket = bucketSel ? bucketSel.value : "all";
    const range = (rangeInput ? rangeInput.value : "").trim();
    const lineNumbers = lineNumbersCheck && lineNumbersCheck.checked ? "1" : "0";
    currentShowLineNumbers = lineNumbers === "1";

    setQp("variant", variant);
    setQp("bucket", bucket);
    if (bucket === "custom") setQp("range", range);
    else setQp("range", "");
    setQp("lineNumbers", lineNumbers);

    await renderAll({ setId, bucket, variant });
  });
}


  const printBtn = document.getElementById("print-btn");
  if (printBtn) printBtn.addEventListener("click", () => window.print());

  const back = document.getElementById("back-link");
  if (back) back.href = `practice.html?set=${encodeURIComponent(setId)}`;

  await renderAll({ setId, bucket: (bucketSel ? bucketSel.value : "all"), variant: (variantSel ? variantSel.value : "student") });
});
