// practice/assets/js/index.js
// Part-first library view: Part -> Language toggle -> Concept / Basic / Challenge / Rounds

function getLangFromCategory(cat) {
  if (cat.lang) return cat.lang;
  if (typeof cat.name === "string") {
    const parts = cat.name.split("-");
    return (parts[0] || "").trim() || "기타";
  }
  return "기타";
}

function getTrackFromCategory(cat) {
  const explicit = String(cat?.track || "").trim().toLowerCase();
  if (explicit) return explicit;

  const id = String(cat?.id || "").toLowerCase();
  const name = String(cat?.name || "").toLowerCase();
  if (
    id.includes("unity") ||
    id.includes("csharp") ||
    name.includes("unity") ||
    name.includes("유니티")
  ) {
    return "unity";
  }
  return "language";
}

function getTrackLabel(track) {
  if (track === "language") return "언어 수업";
  if (track === "unity") return "유니티 수업";
  if (track === "contest") return "경시대회 수업";
  if (track === "canva") return "Canva 가이드";
  return track;
}

function preferredLangSort(langs) {
  const prefer = ["Python", "C", "Java", "JavaScript", "C++", "C#"];
  return langs.slice().sort((a, b) => {
    const ia = prefer.indexOf(a);
    const ib = prefer.indexOf(b);
    if (ia === -1 && ib === -1) return a.localeCompare(b, "ko");
    if (ia === -1) return 1;
    if (ib === -1) return -1;
    return ia - ib;
  });
}

function normalizeUiLangToParam(lang) {
  const v = String(lang || "").toLowerCase();
  if (v === "python") return "python";
  if (v === "c") return "c";
  if (v === "java") return "java";
  if (v === "cs" || v === "c#" || v === "csharp") return "csharp";
  return v
    .replace(/\s+/g, "")
    .replace(/[^\w#+-]/g, "")
    .replace(/^c#$/, "csharp");
}

function getPartKey(cat) {
  const id = String(cat?.id || "");
  if (!id.includes("_")) return id || "misc";
  return id.split("_").slice(1).join("_") || id;
}

function cleanPartLabel(raw) {
  const s = String(raw || "").trim();
  if (!s) return "미분류";
  return s.replace(/^lv\s*\d+\s*/i, "").replace(/^LV\s*\d+\s*/i, "").trim();
}

function getLevelFromCategory(cat) {
  const name = String(cat?.name || "");
  const m = name.match(/\b(LV|Lv|lv)\s*(\d+)\b/);
  if (!m) return "";
  return `Lv${m[2]}`;
}

function getPartLabel(cat) {
  if (cat.partName) return cat.partName;
  const name = String(cat?.name || "");
  if (!name.includes("-")) return cleanPartLabel(name);
  const rhs = name.split("-").slice(1).join("-").trim();
  return cleanPartLabel(rhs);
}

function getPriorityInfo(priorityRaw) {
  const n = Number(priorityRaw);
  const value = Number.isFinite(n) ? Math.max(1, Math.min(3, Math.round(n))) : 2;
  if (value >= 3) return { value: 3, stars: "★★★", label: "집중" };
  if (value === 2) return { value: 2, stars: "★★", label: "핵심" };
  return { value: 1, stars: "★", label: "기본" };
}

function createLangButton(lang, active) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "part-lang-btn";
  if (active) btn.classList.add("active");
  btn.dataset.lang = lang;
  btn.textContent = lang;
  return btn;
}

function createTrackButton(track, active) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "part-lang-btn";
  if (active) btn.classList.add("active");
  btn.dataset.track = track;
  btn.textContent = getTrackLabel(track);
  return btn;
}

function createActionLink(label, href, variant) {
  const a = document.createElement("a");
  a.className = `part-action-link ${variant || ""}`.trim();
  a.href = href;
  a.textContent = label;
  return a;
}

function createRoundChip(setMeta) {
  const a = document.createElement("a");
  a.className = "part-round-chip";
  a.href = `practice.html?set=${encodeURIComponent(setMeta.id)}`;
  const diff = setMeta.difficulty === "challenge" ? "Challenge" : "Basic";
  a.textContent = `R${setMeta.round} · ${diff}`;
  return a;
}

function setCardRoundsHidden(cardEl, hidden) {
  const rounds = cardEl.querySelector(".part-rounds");
  const toggle = cardEl.querySelector(".part-rounds-toggle");
  if (!rounds || !toggle) return;
  rounds.hidden = hidden;
  toggle.textContent = hidden ? "자세히 보기" : "접기";
}

function getCardsInSameRow(cardEl) {
  const parent = cardEl.parentElement;
  if (!parent) return [cardEl];
  const cards = Array.from(parent.children).filter((el) =>
    el.classList.contains("part-card")
  );
  const top = cardEl.offsetTop;
  const tolerance = 4;
  const sameRow = cards.filter((el) => Math.abs(el.offsetTop - top) <= tolerance);
  return sameRow.length ? sameRow : [cardEl];
}

function groupByPart(categories, sets) {
  const map = new Map();
  categories.forEach((cat) => {
    const key = getPartKey(cat);
    const part = map.get(key) || {
      key,
      label: getPartLabel(cat),
      level: getLevelFromCategory(cat),
      byLang: {},
      order: Number.MAX_SAFE_INTEGER,
    };
    const lang = getLangFromCategory(cat);
    part.byLang[lang] = {
      category: cat,
      sets: sets
        .filter((s) => s.categoryId === cat.id)
        .sort((a, b) => (a.round || 0) - (b.round || 0)),
    };
    if (!part.level) part.level = getLevelFromCategory(cat);
    part.order = Math.min(part.order, cat.order || Number.MAX_SAFE_INTEGER);
    map.set(key, part);
  });
  function levelRank(part) {
    const m = String(part?.level || "").match(/(\d+)/);
    return m ? Number(m[1]) : Number.MAX_SAFE_INTEGER;
  }

  return Array.from(map.values()).sort((a, b) => {
    const lvDiff = levelRank(a) - levelRank(b);
    if (lvDiff !== 0) return lvDiff;

    const orderDiff = (a.order || Number.MAX_SAFE_INTEGER) - (b.order || Number.MAX_SAFE_INTEGER);
    if (orderDiff !== 0) return orderDiff;

    return String(a.label || "").localeCompare(String(b.label || ""), "ko");
  });
}

function buildPartCard(part, lang, theoryByCategoryId) {
  const langInfo = part.byLang[lang];
  if (!langInfo) return null;
  const theory = theoryByCategoryId[langInfo.category.id];
  const hasTheoryOnly = !langInfo.sets.length && !!theory?.conceptId;
  if (!langInfo.sets.length && !hasTheoryOnly) return null;

  const section = document.createElement("section");
  section.className = "part-card";

  const head = document.createElement("div");
  head.className = "part-card-head";

  const title = document.createElement("h3");
  title.className = "part-card-title";
  title.textContent = part.label;
  if (part.level) {
    const lv = document.createElement("span");
    lv.className = "part-level-badge";
    lv.textContent = part.level;
    title.appendChild(document.createTextNode(" "));
    title.appendChild(lv);
  }

  const meta = document.createElement("p");
  meta.className = "part-card-meta";
  const basicCount = langInfo.sets.filter((s) => s.difficulty !== "challenge").length;
  const challengeCount = langInfo.sets.filter((s) => s.difficulty === "challenge").length;
  const priority = getPriorityInfo(theory?.priority);
  meta.textContent = `${lang}`;

  const priorityBadge = document.createElement("span");
  priorityBadge.className = `part-priority-badge p${priority.value}`;
  priorityBadge.textContent = `${priority.stars} ${priority.label}`;
  meta.appendChild(document.createTextNode(" "));
  meta.appendChild(priorityBadge);

  head.append(title, meta);

  const controls = document.createElement("div");
  controls.className = "part-primary-controls";

  const actions = document.createElement("div");
  actions.className = "part-actions";
  const basics = langInfo.sets.filter((s) => s.difficulty !== "challenge");
  const challenges = langInfo.sets.filter((s) => s.difficulty === "challenge");
  const startHref = (() => {
    if (theory?.conceptId) {
      const q = new URLSearchParams();
      q.set("concept", theory.conceptId);
      const langParam = normalizeUiLangToParam(lang);
      if (langParam) q.set("lang", langParam);
      return `theory.html?${q.toString()}`;
    }
    if (basics[0]) return `practice.html?set=${encodeURIComponent(basics[0].id)}`;
    if (challenges[0]) return `practice.html?set=${encodeURIComponent(challenges[0].id)}`;
    return "#";
  })();
  actions.appendChild(createActionLink("학습 시작", startHref, "start"));
  controls.appendChild(actions);

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "part-rounds-toggle";
  toggle.textContent = "자세히 보기";
  if (langInfo.sets.length) controls.appendChild(toggle);

  const rounds = document.createElement("div");
  rounds.className = "part-rounds";
  rounds.hidden = true;
  const stats = document.createElement("p");
  stats.className = "part-round-stats";
  stats.textContent = `Basics ${basicCount} · Challenges ${challengeCount}`;
  rounds.appendChild(stats);

  const secondary = document.createElement("div");
  secondary.className = "part-secondary-actions";
  if (theory?.conceptId) {
    const q = new URLSearchParams();
    q.set("concept", theory.conceptId);
    const langParam = normalizeUiLangToParam(lang);
    if (langParam) q.set("lang", langParam);
    secondary.appendChild(
      createActionLink("개념 보기", `theory.html?${q.toString()}`, "theory")
    );
  }
  if (basics[0]) {
    secondary.appendChild(
      createActionLink(
        "기초 시작",
        `practice.html?set=${encodeURIComponent(basics[0].id)}`,
        "basic"
      )
    );
  }
  if (challenges[0]) {
    secondary.appendChild(
      createActionLink(
        "챌린지 시작",
        `practice.html?set=${encodeURIComponent(challenges[0].id)}`,
        "challenge"
      )
    );
  }
  if (secondary.childElementCount) rounds.appendChild(secondary);

  if (basics.length) {
    const g = document.createElement("div");
    g.className = "part-round-group";
    const gt = document.createElement("p");
    gt.className = "part-round-title";
    gt.textContent = "Basics";
    const row = document.createElement("div");
    row.className = "part-round-row";
    basics.forEach((s) => row.appendChild(createRoundChip(s)));
    g.append(gt, row);
    rounds.appendChild(g);
  }
  if (challenges.length) {
    const g = document.createElement("div");
    g.className = "part-round-group";
    const gt = document.createElement("p");
    gt.className = "part-round-title";
    gt.textContent = "Challenges";
    const row = document.createElement("div");
    row.className = "part-round-row";
    challenges.forEach((s) => row.appendChild(createRoundChip(s)));
    g.append(gt, row);
    rounds.appendChild(g);
  }

  if (langInfo.sets.length) {
    toggle.addEventListener("click", () => {
      const nextHidden = !rounds.hidden;
      const sameRowCards = getCardsInSameRow(section);
      sameRowCards.forEach((cardEl) => setCardRoundsHidden(cardEl, nextHidden));
    });
  } else {
    rounds.hidden = false;
  }

  section.append(head, controls, rounds);
  return section;
}

document.addEventListener("DOMContentLoaded", async () => {
  const root = document.getElementById("list-root");
  root.textContent = "Loading problem library...";

  try {
    const [categories, sets, theoryIndex] = await Promise.all([
      ProblemService.listCategories(),
      ProblemService.listSets(),
      ProblemService.listTheoryIndex().catch(() => []),
    ]);

    categories.sort((a, b) => (a.order || 0) - (b.order || 0));

    const theoryByCategoryId = {};
    theoryIndex.forEach((item) => {
      if (item?.categoryId) theoryByCategoryId[item.categoryId] = item;
    });

    const tracks = ["language", "unity"]
      .filter((track) => categories.some((cat) => getTrackFromCategory(cat) === track))
      .concat(
        Array.from(
          new Set(categories.map((cat) => getTrackFromCategory(cat)))
        ).filter((track) => !["language", "unity"].includes(track))
      );

    const state = {
      track: tracks.includes("language") ? "language" : tracks[0],
      lang: "",
    };

    root.innerHTML = "";

    const controls = document.createElement("section");
    controls.className = "part-controls";

    const trackLabel = document.createElement("span");
    trackLabel.className = "part-controls-label";
    trackLabel.textContent = "수업";
    controls.appendChild(trackLabel);

    const trackWrap = document.createElement("div");
    trackWrap.className = "part-track-wrap";
    controls.appendChild(trackWrap);

    const langLabel = document.createElement("span");
    langLabel.className = "part-controls-label";
    langLabel.textContent = "언어";
    controls.appendChild(langLabel);

    const langWrap = document.createElement("div");
    langWrap.className = "part-lang-wrap";
    controls.appendChild(langWrap);

    root.appendChild(controls);

    const list = document.createElement("section");
    list.className = "part-list";
    root.appendChild(list);

    function getLanguagesForTrack(track) {
      return preferredLangSort(
        Array.from(
          new Set(
            categories
              .filter((cat) => getTrackFromCategory(cat) === track)
              .map((cat) => getLangFromCategory(cat))
          )
        )
      );
    }

    function syncLanguageState() {
      const langs = getLanguagesForTrack(state.track);
      if (!langs.includes(state.lang)) {
        state.lang = langs.includes("Python") ? "Python" : langs[0] || "";
      }
      return langs;
    }

    function renderTrackButtons() {
      trackWrap.innerHTML = "";
      tracks.forEach((track) =>
        trackWrap.appendChild(createTrackButton(track, track === state.track))
      );
    }

    function renderLanguageButtons(langs) {
      langWrap.innerHTML = "";
      langs.forEach((lang) =>
        langWrap.appendChild(createLangButton(lang, lang === state.lang))
      );
    }

    function render() {
      const langs = syncLanguageState();
      renderTrackButtons();
      renderLanguageButtons(langs);

      list.innerHTML = "";
      const activeCategories = categories.filter(
        (cat) => getTrackFromCategory(cat) === state.track
      );
      const parts = groupByPart(activeCategories, sets);
      const cards = parts
        .map((part) => buildPartCard(part, state.lang, theoryByCategoryId))
        .filter(Boolean);

      if (!cards.length) {
        const empty = document.createElement("p");
        empty.className = "part-empty";
        empty.textContent = `${getTrackLabel(state.track)}에 등록된 파트가 없습니다.`;
        list.appendChild(empty);
        return;
      }
      cards.forEach((card) => list.appendChild(card));
    }

    trackWrap.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-track]");
      if (!btn) return;
      state.track = btn.dataset.track;
      state.lang = "";
      render();
    });

    langWrap.addEventListener("click", (e) => {
      const btn = e.target.closest("[data-lang]");
      if (!btn) return;
      state.lang = btn.dataset.lang;
      render();
    });

    render();
  } catch (err) {
    console.error(err);
    root.textContent = "Failed to load the library.";
  }
});
