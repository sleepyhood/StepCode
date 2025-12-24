/* print.js - A4 landscape worksheet printer (2 columns, 4 problems per page) */

let currentSetData = null;

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

function buildProblemCard(set, q, originalIndex, variant) {
  const card = el("section", "p-card");

  const head = el("div", "p-head");
  head.appendChild(el("div", "p-no", `${originalIndex + 1}번`));
  head.appendChild(el("div", "p-type", typeLabel(q)));
  card.appendChild(head);

  card.appendChild(el("div", "p-title", q.title || ""));

  const desc = el("div", "p-desc");
  desc.textContent = String(q.description || "");
  card.appendChild(desc);

  if (q.code) {
    const pre = el("pre", "p-code");
    pre.textContent = String(q.code);
    card.appendChild(pre);
  }

  if (q.type === "mcq") {
    const opts = el("div", "p-options");
    (q.options || []).forEach((t, i) => {
      const row = el("div", "p-opt");
      const labels = q.optionLabels || [];
      const letter = labels[i] || String.fromCharCode(65 + i);
      row.appendChild(el("div", "bullet", `◯ ${letter}`));
      row.appendChild(el("div", "text", String(t)));
      opts.appendChild(row);
    });
    card.appendChild(opts);
  }

  const answer = el("div", "answer-block");

  if (q.type === "mcq") {
    answer.appendChild(el("div", "answer-label", "이유(간단히):"));
    answer.appendChild(el("div", "answer-lines compact"));
  } else if (q.type === "short") {
    answer.appendChild(el("div", "answer-label", "답:"));
    const lines = el("div", "answer-lines");
    lines.style.setProperty("--n", "4");
    answer.appendChild(lines);
  } else if (q.type === "code") {
    if (isCondBlankQuestion(q)) {
      answer.appendChild(el("div", "answer-label", "조건식(한 줄):"));
      answer.appendChild(el("div", "answer-lines compact"));
    } else {
      answer.appendChild(el("div", "answer-label", "코드:"));
      const box = el("div", "answer-lines codebox");
      box.style.setProperty("--n", "10");
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
      br.appendChild(el("span", "", String(q.hint)));
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

function buildPage(setId, set, pageIndex, pageCount, problems, indexMap, variant, bucket) {
  const page = el("div", "print-page");

  const header = el("div", "page-header");

  const left = el("div", "meta-left");
  left.appendChild(el("div", "page-title", `${set.title || "학습지"} · ${variant === "teacher" ? "선생님용" : "학생용"}`));

  const row = el("div", "meta-row");
  row.appendChild(metaField("학생", "name", "w120"));
  row.appendChild(metaField("반", "class", ""));
  row.appendChild(metaField("번호", "no", ""));
  row.appendChild(metaField("배부일", "dist", "", ymd()));
  row.appendChild(metaField("제출일", "due", "w120"));
  left.appendChild(row);

  const right = el("div", "meta-right");
  right.innerHTML = `
    <div>페이지 ${pageIndex + 1} / ${pageCount}</div>
    <div class="docid">${makeDocId(setId, bucket, variant)}</div>
  `;

  header.appendChild(left);
  header.appendChild(right);
  page.appendChild(header);

  const grid = el("div", "page-grid");
  for (let i = 0; i < 4; i++) {
    const q = problems[i];
    if (!q) { grid.appendChild(el("div", "p-card")); continue; }
    const originalIndex = indexMap.get(q.id) ?? i;
    grid.appendChild(buildProblemCard(set, q, originalIndex, variant));
  }
  page.appendChild(grid);

  return page;
}

function updateToolbarTitle(set, bucket, variant) {
  const t = document.getElementById("pt-set-title");
  const s = document.getElementById("pt-subtitle");
  if (t) t.textContent = set?.title || "학습지";
  if (s) s.textContent = `범위: ${bucket} · 유형: ${variant}`;
}

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

  const pages = chunk(selected, 4);
  const pageCount = Math.max(1, pages.length);

  root.innerHTML = "";
  pages.forEach((probs, i) => {
    root.appendChild(buildPage(setId, currentSetData, i, pageCount, probs, indexMap, variant, bucket));
  });

  updateToolbarTitle(currentSetData, bucket, variant);
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

  const initVariant = qp("variant") || "student";
  const initBucket = qp("bucket") || "all";

  if (variantSel) variantSel.value = (initVariant === "teacher" ? "teacher" : "student");
  if (bucketSel) bucketSel.value = (initBucket === "core" || initBucket === "supp") ? initBucket : "all";

  const applyBtn = document.getElementById("apply-btn");
  if (applyBtn) {
    applyBtn.addEventListener("click", async () => {
      const variant = variantSel ? variantSel.value : "student";
      const bucket = bucketSel ? bucketSel.value : "all";
      setQp("variant", variant);
      setQp("bucket", bucket);
      await renderAll({ setId, bucket, variant });
    });
  }

  const printBtn = document.getElementById("print-btn");
  if (printBtn) printBtn.addEventListener("click", () => window.print());

  const back = document.getElementById("back-link");
  if (back) back.href = `practice.html?set=${encodeURIComponent(setId)}`;

  await renderAll({ setId, bucket: (bucketSel ? bucketSel.value : "all"), variant: (variantSel ? variantSel.value : "student") });
});
