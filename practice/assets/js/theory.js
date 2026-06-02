/**
 * StepCode - Theory Page Logic (Controller)
 * Modularized version: UI, problems, slide, and markdown logic moved to /theory/ directory.
 */

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

// 7. Related Problems Rendering
function renderRelatedProblems(entry, setMap) {
  const listEl = document.getElementById("theory-related-list");
  const startBtn = document.getElementById("theory-start-btn");
  if (!listEl) return;

  listEl.innerHTML = "";

  if (entry.recommendedSetId && startBtn) {
    startBtn.hidden = false;
    startBtn.href = `practice.html?set=${encodeURIComponent(entry.recommendedSetId)}`;
  } else if (startBtn) {
    startBtn.hidden = true;
  }

  let relatedSets = [];
  if (Array.isArray(entry.relatedSetIds) && entry.relatedSetIds.length > 0) {
    relatedSets = entry.relatedSetIds.map(id => setMap[id]).filter(Boolean);
  } else if (entry.categoryId) {
    relatedSets = Object.values(setMap).filter(s => s.categoryId === entry.categoryId);
  }

  relatedSets.sort((a, b) => (a.round || 0) - (b.round || 0));

  if (relatedSets.length === 0) {
    const emptyMsg = document.createElement("p");
    emptyMsg.style.fontSize = "14px";
    emptyMsg.style.color = "var(--color-gray-500)";
    emptyMsg.textContent = "관련 문제가 없습니다.";
    listEl.appendChild(emptyMsg);
    return;
  }

  const row = document.createElement("div");
  row.className = "part-round-row";
  row.style.display = "flex";
  row.style.flexWrap = "wrap";
  row.style.gap = "8px";
  row.style.marginTop = "10px";

  relatedSets.forEach(setMeta => {
    const a = document.createElement("a");
    a.className = "part-round-chip";
    a.href = `practice.html?set=${encodeURIComponent(setMeta.id)}`;
    a.style.textDecoration = "none";
    const diff = setMeta.difficulty === "challenge" ? "Challenge" : "Basic";
    a.textContent = `R${setMeta.round || 1} · ${diff}`;
    if (setMeta.title) a.title = setMeta.title;
    row.appendChild(a);
  });

  listEl.appendChild(row);
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
  toast.querySelector(".resume-yes").onclick = () => {
    window.scrollTo({ top: yPosition, behavior: "smooth" });
    toast.classList.remove("visible"); setTimeout(() => toast.remove(), 300);
  };
  toast.querySelector(".resume-no").onclick = () => {
    toast.classList.remove("visible"); setTimeout(() => toast.remove(), 300);
  };
  setTimeout(() => toast.classList.add("visible"), 50);
}

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
    if (!res.ok) throw new Error("MD fetch failed");
    const mdText = await res.text();
    await renderTheoryMarkdown(contentEl, mdText, entry.mdPath);
    if (entry.slidePath) setupSlideMode(entry.slidePath);
    
    renderRelatedProblems(entry, setMap);

    const savedPos = localStorage.getItem(`readPosition_${location.search}`);
    if (savedPos && parseInt(savedPos) > 150) {
      setTimeout(() => showResumeToast(parseInt(savedPos)), 1000);
    }
  } catch (e) { console.error("Initialization failed:", e); }
}

document.addEventListener("DOMContentLoaded", initTheoryPage);
