/* print.js - A4 landscape worksheet printer (2 columns, 4 problems per page) */

let currentSetData = null;
const SLOTS_PER_PAGE = 2;

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
  const pageH = cssToPx("calc(210mm - 20mm)"); // A4 landscape의 content height = 210-상하마진(10mm*2)=190mm
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

function shouldMcqCodeOptionsUseTwoColumns(q) {
  const opts = Array.isArray(q?.options) ? q.options : [];
  if (opts.length < 4) return false;
  if (opts.length > 6) return false;

  // ✅ 코드박스는 2열에서 폭이 더 좁아지므로 텍스트보다 보수적으로
  const MAX_ROWS = 15;          // (래핑 포함) 옵션 1개당 허용 "보이는 줄" 총합
  const MAX_ROW_CHARS = 28;    // 한 줄이 이 길이를 넘으면 래핑된다고 가정
  const MAX_TOKEN_CHARS = 28;  // 공백 없는 덩어리(긴 식별자/문자열)가 너무 길면 2열 금지
  const MAX_PHYSICAL_LINES = 15; // 실제 개행 줄 수 하드캡

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
  head.appendChild(el("div", "p-no", `${originalIndex + 1}번`));
  head.appendChild(el("div", "p-type", typeLabel(q)));
  card.appendChild(head);

    const title = el("div", "p-title md md-inline");
  setMD(title, q.title || "", "inline");
  card.appendChild(title);


  const desc = el("div", "p-desc md");
  setMD(desc, q.description || "", "block");
  card.appendChild(desc);

  if (q.code) {
    const pre = el("pre", "p-code");
    pre.textContent = String(q.code);
    card.appendChild(pre);
  }

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
      const pre = el("pre", "p-code opt-code");
      pre.textContent = opt;
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
  lines.style.setProperty("--n", "1.5");
  answer.appendChild(lines);

} else if (q.type === "short") {
  answer.appendChild(el("div", "answer-label", "답:"));
  const lines = el("div", "answer-lines");
  lines.style.setProperty("--n", "1.5");
  answer.appendChild(lines);

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

function buildPage(setId, set, pageIndex, pageCount, problems, indexMap, variant, bucket) {
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
  const colL = el("div", "page-col");
  const colR = el("div", "page-col");
  grid.appendChild(colL);
  grid.appendChild(colR);
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

  const probeFirst = buildPage(setId, currentSetData, 0, 99, [], indexMap, variant, bucket);
  root.appendChild(probeFirst);
  const bodyHFirst = getBodyHeightPx(probeFirst);

  const probeOther = buildPage(setId, currentSetData, 1, 99, [], indexMap, variant, bucket);
  root.appendChild(probeOther);
  const bodyHOther = getBodyHeightPx(probeOther);

  root.removeChild(probeFirst);
  root.removeChild(probeOther);

  // 1) "빈 페이지" 하나 만들어서 폭/높이 측정
  const probePage = buildPage(setId, currentSetData, 0, 1, [], indexMap, variant, bucket);
  root.appendChild(probePage);

  const grid = probePage.querySelector(".page-grid");
  const colL = probePage.querySelector(".page-col");
  const bodyH = getBodyHeightPx(probePage);

  // 컬럼 폭(px): grid의 절반 - gap 고려
  const gridRect = grid.getBoundingClientRect();
  const gapPx = parseFloat(getComputedStyle(grid).gap || "0");
  const colW = (gridRect.width - gapPx) / 2;

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
  for (const q of selected) {
    const originalIndex = indexMap.get(q.id) ?? 0;
    const card = buildProblemCard(currentSetData, q, originalIndex, variant);
    meas.appendChild(card);
    const h = measureCardHeightPx(card, colW);
    heights.set(q.id, h);
    meas.removeChild(card);
  }
  const colGapPx = parseFloat(getComputedStyle(probePage.querySelector(".page-col")).gap || "0");


  // probe 제거
  root.removeChild(probePage);
  meas.remove();

    // ✅ vertical gap(열 내부 카드 간격) px 구하기
  // const colGapPx = parseFloat(getComputedStyle(probePage.querySelector(".page-col")).gap || "0");

  // ✅ 3) 규칙 기반 패킹
  // 1) 기본은 1행 2열(= 2문제)
  // 2) 다음 2문제가 같은 페이지의 2행(= 총 4문제)으로 들어가면 합치기
  const pages = [];
  let i = 0;

  while (i < selected.length) {
    const q1 = selected[i] ?? null;
    const q2 = selected[i + 1] ?? null;

    const page = { left: [], right: [] };
    const bodyHPage = (pages.length === 0) ? bodyHFirst : bodyHOther;

    
    if (q1) page.left.push(q1);
    if (q2) page.right.push(q2);

    i += 2;

    // 다음 2개를 "2행"으로 합칠지 판단
    const q3 = selected[i] ?? null;
    const q4 = selected[i + 1] ?? null;

    // 다음 페이지가 "2문제" 형태로 있을 때만 합치기(네 요구와 동일)
    if (q3 && q4) {
      const h1 = heights.get(q1.id) ?? 0;
      const h2 = q2 ? (heights.get(q2.id) ?? 0) : 0;

      const h3 = heights.get(q3.id) ?? 0;
      const h4 = heights.get(q4.id) ?? 0;
      
      // AFTER
      const fitLeft  = (h1 + colGapPx + h3) <= bodyHPage;
      const fitRight = (h2 + colGapPx + h4) <= bodyHPage;

      // 4칸(2행2열) 조건: q3는 왼쪽 아래, q4는 오른쪽 아래
      const fitLeft3   = (h1 + colGapPx + h3) <= bodyHPage;
      const fitRight4  = (h2 + colGapPx + h4) <= bodyHPage;

      // 3칸 예외(오른쪽 아래에 q3만 넣기) 조건: q3가 오른쪽 아래에 실제로 들어가는지
      const fitRight3  = (h2 + colGapPx + h3) <= bodyHPage;


      if (fitLeft3 && fitRight4) {
        // 1 2 / 3 4
        page.left.push(q3);
        page.right.push(q4);
        i += 2;
      } else if (fitLeft3) {
        // 1 2 / 3 _
        page.left.push(q3);
        i += 1;
      } else if (fitRight3) {
        // 1 2 / _ 3
        page.right.push(q3);
        i += 1;
      }

    }

  // ✅ q4가 없고 q3만 남은 경우도 동일하게 처리 가능
  else if (q3) {
      const h1 = heights.get(q1.id) ?? 0;
      const h2 = q2 ? (heights.get(q2.id) ?? 0) : 0;
      const h3 = heights.get(q3.id) ?? 0;

      const fitLeft  = (h1 + colGapPx + h3) <= bodyHPage;
      const fitRight = (h2 + colGapPx + h3) <= bodyHPage;

      if (fitLeft) {
        page.left.push(q3);   // 1 2 / 3 _
        i += 1;
      } else if (fitRight) {
        page.right.push(q3);  // ✅ 1 2 / _ 3
        i += 1;
      }
  }
  

    pages.push(page);
}


  // 4) 실제 렌더
  const pageCount = pages.length;
  pages.forEach((p, i) => {
    const pageEl = buildPage(setId, currentSetData, i, pageCount, [], indexMap, variant, bucket);
    // ✅ 수정
    const cols = pageEl.querySelectorAll(".page-col");
    const colL = cols[0];
    const colR = cols[1]; 

    p.left.forEach((q) => {
      const originalIndex = indexMap.get(q.id) ?? 0;
      colL.appendChild(buildProblemCard(currentSetData, q, originalIndex, variant));
    });

    p.right.forEach((q) => {
      const originalIndex = indexMap.get(q.id) ?? 0;
      colR.appendChild(buildProblemCard(currentSetData, q, originalIndex, variant));
    });

    root.appendChild(pageEl);
  });

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

// [print.markdown.js] 위치: document.addEventListener("DOMContentLoaded", ...) 내부
// bucket-select/apply-btn 세팅하는 부분에 추가

const rangeWrap = document.getElementById("range-wrap");
const rangeInput = document.getElementById("range-input");
const rangeHint = document.getElementById("range-hint");

// 초기값(쿼리스트링)
const initBucket = qp("bucket") || "all";
const initRange = qp("range") || "";

if (bucketSel) bucketSel.value = (["all","core","supp","custom"].includes(initBucket) ? initBucket : "all");
if (rangeInput) rangeInput.value = initRange;

// bucket 변경 시 입력칸 토글
function syncRangeUI() {
  const isCustom = (bucketSel && bucketSel.value === "custom");
  if (rangeWrap) rangeWrap.classList.toggle("is-hidden", !isCustom);
  if (rangeHint) rangeHint.textContent = "";
}
if (bucketSel) bucketSel.addEventListener("change", syncRangeUI);
syncRangeUI();


  // if (variantSel) variantSel.value = (initVariant === "teacher" ? "teacher" : "student");
  // if (bucketSel) bucketSel.value = (initBucket === "core" || initBucket === "supp") ? initBucket : "all";

  const applyBtn = document.getElementById("apply-btn");
  
// apply 클릭 시 range도 query param에 반영
if (applyBtn) {
  applyBtn.addEventListener("click", async () => {
    const variant = variantSel ? variantSel.value : "student";
    const bucket = bucketSel ? bucketSel.value : "all";
    const range = (rangeInput ? rangeInput.value : "").trim();

    setQp("variant", variant);
    setQp("bucket", bucket);
    if (bucket === "custom") setQp("range", range);
    else setQp("range", ""); // custom 아니면 비워두기(혼선 방지)

    await renderAll({ setId, bucket, variant });
  });
}


  const printBtn = document.getElementById("print-btn");
  if (printBtn) printBtn.addEventListener("click", () => window.print());

  const back = document.getElementById("back-link");
  if (back) back.href = `practice.html?set=${encodeURIComponent(setId)}`;

  await renderAll({ setId, bucket: (bucketSel ? bucketSel.value : "all"), variant: (variantSel ? variantSel.value : "student") });
});
