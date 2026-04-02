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
  if (track === "pygame") return "파이게임 수업";
  if (track === "unity") return "유니티 수업";
  if (track === "contest") return "경시대회 수업";
  if (track === "canva") return "Canva 가이드";
  return track;
}

function getSecondaryFilterLabel(track) {
  if (track === "language") return "언어";
  return "분류";
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

const INDEX_VIEW_STATE_KEY = "stepcode:index:view-state";

function normalizeParamLangToUi(langParam) {
  const v = String(langParam || "").trim().toLowerCase();
  if (v === "python") return "Python";
  if (v === "c") return "C";
  if (v === "java") return "Java";
  if (v === "csharp" || v === "c#" || v === "cs") return "C#";
  return "";
}

function readSavedIndexViewState() {
  try {
    const raw = localStorage.getItem(INDEX_VIEW_STATE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") return {};
    return {
      track: String(parsed.track || ""),
      lang: String(parsed.lang || ""),
    };
  } catch (_) {
    return {};
  }
}

function persistIndexViewState(state) {
  try {
    localStorage.setItem(
      INDEX_VIEW_STATE_KEY,
      JSON.stringify({
        track: String(state?.track || ""),
        lang: String(state?.lang || ""),
      })
    );
  } catch (_) {}
}

function withViewStateParams(href, viewState) {
  const raw = String(href || "");
  if (!raw || raw === "#") return raw;

  const hashIdx = raw.indexOf("#");
  const beforeHash = hashIdx >= 0 ? raw.slice(0, hashIdx) : raw;
  const hash = hashIdx >= 0 ? raw.slice(hashIdx) : "";

  const qIdx = beforeHash.indexOf("?");
  const path = qIdx >= 0 ? beforeHash.slice(0, qIdx) : beforeHash;
  const query = qIdx >= 0 ? beforeHash.slice(qIdx + 1) : "";
  const q = new URLSearchParams(query);

  if (viewState?.track) q.set("track", viewState.track);
  const langParam = normalizeUiLangToParam(viewState?.lang);
  if (langParam) q.set("lang", langParam);

  const qs = q.toString();
  return `${path}${qs ? `?${qs}` : ""}${hash}`;
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

function isVisibleSetMeta(setMeta) {
  return String(setMeta?.status || "active").toLowerCase() !== "inactive";
}

function createSegmentButton(value, label, active, key) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "part-segment-btn";
  if (active) btn.classList.add("active");
  btn.dataset[key] = value;
  btn.textContent = label;
  return btn;
}

function createActionLink(label, href, variant, viewState) {
  const a = document.createElement("a");
  a.className = `part-action-link ${variant || ""}`.trim();
  a.href = withViewStateParams(href, viewState);
  a.textContent = label;
  return a;
}

function createRoundChip(setMeta, viewState) {
  const a = document.createElement("a");
  a.className = "part-round-chip";
  a.href = withViewStateParams(
    `practice.html?set=${encodeURIComponent(setMeta.id)}`,
    viewState
  );
  const diff = setMeta.difficulty === "challenge" ? "Challenge" : "Basic";
  a.textContent = `R${setMeta.round} · ${diff}`;
  return a;
}

function createContestBatchPdfPanel() {
  const section = document.createElement("section");
  section.className = "part-card";

  const head = document.createElement("div");
  head.className = "part-card-head";

  const titleRow = document.createElement("div");
  titleRow.className = "part-card-title-row";

  const title = document.createElement("h3");
  title.className = "part-card-title";
  title.textContent = "경시대회 묶음 PDF";
  titleRow.appendChild(title);

  const meta = document.createElement("p");
  meta.className = "part-card-meta";
  meta.textContent = "언어/학년별 11회차 통합 출력";

  head.append(titleRow, meta);

  const actions = document.createElement("div");
  actions.className = "part-rounds";

  const combos = [
    { lang: "c", level: "elem", label: "C 초등 11회차" },
    { lang: "c", level: "mid", label: "C 중등 11회차" },
    { lang: "c", level: "high", label: "C 고등 11회차" },
    { lang: "py", level: "elem", label: "PY 초등 11회차" },
    { lang: "py", level: "mid", label: "PY 중등 11회차" },
    { lang: "py", level: "high", label: "PY 고등 11회차" },
  ];

  combos.forEach((combo) => {
    const row = document.createElement("div");
    row.className = "part-secondary-actions";

    const qProblem = new URLSearchParams();
    qProblem.set("contestLang", combo.lang);
    qProblem.set("contestLevel", combo.level);
    qProblem.set("contestRounds", "11");
    qProblem.set("variant", "student");
    qProblem.set("bucket", "all");
    const problemLink = document.createElement("a");
    problemLink.className = "part-action-link basic";
    problemLink.href = `print.html?${qProblem.toString()}`;
    problemLink.textContent = `${combo.label} 문제`;
    row.appendChild(problemLink);

    const qTheory = new URLSearchParams();
    qTheory.set("contestLang", combo.lang);
    qTheory.set("contestLevel", combo.level);
    qTheory.set("contestWeeks", "11");
    qTheory.set("lang", combo.lang === "c" ? "c" : "python");
    qTheory.set(
      "audience",
      combo.level === "elem" ? "elementary" : combo.level === "mid" ? "middle" : "high"
    );
    qTheory.set("view", "student");
    const theoryLink = document.createElement("a");
    theoryLink.className = "part-action-link theory";
    theoryLink.href = `theory_print.html?${qTheory.toString()}`;
    theoryLink.textContent = `${combo.label} 이론`;
    row.appendChild(theoryLink);

    actions.appendChild(row);
  });

  section.append(head, actions);
  return section;
}

function setCardRoundsHidden(cardEl, hidden) {
  const rounds = cardEl.querySelector(".part-rounds");
  const toggle = cardEl.querySelector(".part-rounds-toggle");
  if (!rounds || !toggle) return;
  rounds.hidden = hidden;
  toggle.textContent = hidden ? "자세히 보기" : "접기";
  toggle.setAttribute("aria-expanded", String(!hidden));
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

    const orderDiff =
      (a.order || Number.MAX_SAFE_INTEGER) - (b.order || Number.MAX_SAFE_INTEGER);
    if (orderDiff !== 0) return orderDiff;

    return String(a.label || "").localeCompare(String(b.label || ""), "ko");
  });
}

function getPartEntry(part, lang, theoryByCategoryId) {
  const langInfo = part.byLang[lang];
  if (!langInfo) return null;

  const theory = theoryByCategoryId[langInfo.category.id];
  const visibleSets = langInfo.sets.filter(isVisibleSetMeta);
  const basics = visibleSets.filter((s) => s.difficulty !== "challenge");
  const challenges = visibleSets.filter((s) => s.difficulty === "challenge");

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

  return {
    theory,
    visibleSets,
    basics,
    challenges,
    startHref,
  };
}

function buildPartCard(part, lang, theoryByCategoryId, viewState) {
  const langInfo = part.byLang[lang];
  if (!langInfo) return null;

  const entry = getPartEntry(part, lang, theoryByCategoryId);
  const theory = entry?.theory;
  const hasTheoryOnly = !entry?.visibleSets.length && !!theory?.conceptId;
  if (!entry || (!entry.visibleSets.length && !hasTheoryOnly)) return null;

  const priority = getPriorityInfo(theory?.priority);

  const section = document.createElement("section");
  section.className = "part-card";

  const head = document.createElement("div");
  head.className = "part-card-head";

  const titleRow = document.createElement("div");
  titleRow.className = "part-card-title-row";

  const title = document.createElement("h3");
  title.className = "part-card-title";
  title.textContent = part.label;
  titleRow.appendChild(title);

  if (part.level) {
    const lv = document.createElement("span");
    lv.className = "part-level-badge";
    lv.textContent = part.level;
    titleRow.appendChild(lv);
  }

  const meta = document.createElement("p");
  meta.className = "part-card-meta";
  meta.append(document.createTextNode(lang));

  const priorityBadge = document.createElement("span");
  priorityBadge.className = `part-priority-badge p${priority.value}`;
  priorityBadge.textContent = `${priority.stars} ${priority.label}`;
  meta.appendChild(priorityBadge);

  head.append(titleRow, meta);

  const controls = document.createElement("div");
  controls.className = "part-primary-controls";

  const actions = document.createElement("div");
  actions.className = "part-actions";
  actions.appendChild(
    createActionLink("학습 시작", entry.startHref, "start", viewState)
  );
  controls.appendChild(actions);

  const rounds = document.createElement("div");
  rounds.className = "part-rounds";
  rounds.hidden = true;

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "part-rounds-toggle";
  toggle.textContent = "자세히 보기";
  toggle.setAttribute("aria-expanded", "false");

  if (langInfo.sets.length) {
    controls.appendChild(toggle);
  } else {
    rounds.hidden = false;
  }

  const stats = document.createElement("p");
  stats.className = "part-round-stats";
  stats.textContent = `Basics ${entry.basics.length} · Challenges ${entry.challenges.length}`;
  rounds.appendChild(stats);

  const secondary = document.createElement("div");
  secondary.className = "part-secondary-actions";
  if (theory?.conceptId) {
    const q = new URLSearchParams();
    q.set("concept", theory.conceptId);
    const langParam = normalizeUiLangToParam(lang);
    if (langParam) q.set("lang", langParam);
    secondary.appendChild(
      createActionLink("개념 보기", `theory.html?${q.toString()}`, "theory", viewState)
    );
  }
  if (entry.basics[0]) {
    secondary.appendChild(
      createActionLink(
        "기초 시작",
        `practice.html?set=${encodeURIComponent(entry.basics[0].id)}`,
        "basic",
        viewState
      )
    );
  }
  if (entry.challenges[0]) {
    secondary.appendChild(
      createActionLink(
        "챌린지 시작",
        `practice.html?set=${encodeURIComponent(entry.challenges[0].id)}`,
        "challenge",
        viewState
      )
    );
  }
  if (secondary.childElementCount) rounds.appendChild(secondary);

  if (entry.basics.length) {
    const basicGroup = document.createElement("div");
    basicGroup.className = "part-round-group";
    const titleBasic = document.createElement("p");
    titleBasic.className = "part-round-title";
    titleBasic.textContent = "Basics";
    const row = document.createElement("div");
    row.className = "part-round-row";
    entry.basics.forEach((setMeta) => row.appendChild(createRoundChip(setMeta, viewState)));
    basicGroup.append(titleBasic, row);
    rounds.appendChild(basicGroup);
  }

  if (entry.challenges.length) {
    const challengeGroup = document.createElement("div");
    challengeGroup.className = "part-round-group";
    const titleChallenge = document.createElement("p");
    titleChallenge.className = "part-round-title";
    titleChallenge.textContent = "Challenges";
    const row = document.createElement("div");
    row.className = "part-round-row";
    entry.challenges.forEach((setMeta) =>
      row.appendChild(createRoundChip(setMeta, viewState))
    );
    challengeGroup.append(titleChallenge, row);
    rounds.appendChild(challengeGroup);
  }

  if (langInfo.sets.length) {
    toggle.addEventListener("click", () => {
      const nextHidden = !rounds.hidden;
      const sameRowCards = getCardsInSameRow(section);
      sameRowCards.forEach((cardEl) => setCardRoundsHidden(cardEl, nextHidden));
    });
  }

  section.append(head, controls, rounds);
  return section;
}

document.addEventListener("DOMContentLoaded", async () => {
  const root = document.getElementById("list-root");
  const heroStartLink = document.getElementById("hero-start-link");
  const heroBrowseLink = document.getElementById("hero-browse-link");
  const heroLiveTrack = document.getElementById("hero-live-track");
  const heroLiveLang = document.getElementById("hero-live-lang");

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
        Array.from(new Set(categories.map((cat) => getTrackFromCategory(cat)))).filter(
          (track) => !["language", "unity"].includes(track)
        )
      );

    const state = {
      track: tracks.includes("language") ? "language" : tracks[0],
      lang: "",
    };

    root.innerHTML = "";

    const toolbar = document.createElement("section");
    toolbar.className = "part-toolbar";

    const toolbarGroups = document.createElement("div");
    toolbarGroups.className = "part-toolbar-groups";

    const trackGroup = document.createElement("div");
    trackGroup.className = "part-toolbar-group";
    const trackLabel = document.createElement("span");
    trackLabel.className = "part-toolbar-label";
    trackLabel.textContent = "수업";
    const trackWrap = document.createElement("div");
    trackWrap.className = "part-segment";
    trackGroup.append(trackLabel, trackWrap);

    const langGroup = document.createElement("div");
    langGroup.className = "part-toolbar-group";
    const langLabel = document.createElement("span");
    langLabel.className = "part-toolbar-label";
    langLabel.textContent = getSecondaryFilterLabel(state.track);
    const langWrap = document.createElement("div");
    langWrap.className = "part-segment";
    langGroup.append(langLabel, langWrap);

    toolbarGroups.append(trackGroup, langGroup);

    const toolbarMeta = document.createElement("aside");
    toolbarMeta.className = "part-toolbar-meta";

    const toolbarMetaLabel = document.createElement("div");
    toolbarMetaLabel.className = "part-toolbar-meta-label";
    toolbarMetaLabel.textContent = "Current view";

    const toolbarMetaValue = document.createElement("div");
    toolbarMetaValue.className = "part-toolbar-meta-value";

    const toolbarMetaCount = document.createElement("div");
    toolbarMetaCount.className = "part-toolbar-meta-count";

    toolbarMeta.append(toolbarMetaLabel, toolbarMetaValue, toolbarMetaCount);
    toolbar.append(toolbarGroups, toolbarMeta);
    root.appendChild(toolbar);

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

    const savedState = readSavedIndexViewState();
    const params = new URLSearchParams(location.search);
    const trackFromQuery = params.get("track");
    const langFromQuery = normalizeParamLangToUi(params.get("lang"));

    if (tracks.includes(trackFromQuery)) {
      state.track = trackFromQuery;
    } else if (tracks.includes(savedState.track)) {
      state.track = savedState.track;
    }
    state.lang = langFromQuery || normalizeParamLangToUi(savedState.lang);

    function syncLanguageState() {
      const langs = getLanguagesForTrack(state.track);
      if (!langs.includes(state.lang)) {
        state.lang = langs.includes("Python") ? "Python" : langs[0] || "";
      }
      return langs;
    }

    function renderTrackButtons() {
      trackWrap.innerHTML = "";
      tracks.forEach((track) => {
        trackWrap.appendChild(
          createSegmentButton(track, getTrackLabel(track), track === state.track, "track")
        );
      });
    }

    function renderLanguageButtons(langs) {
      langWrap.innerHTML = "";
      langs.forEach((lang) => {
        langWrap.appendChild(
          createSegmentButton(lang, lang, lang === state.lang, "lang")
        );
      });
    }

    function updateHeroSummary(partCardsCount, firstStartHref) {
      if (heroLiveTrack) heroLiveTrack.textContent = getTrackLabel(state.track);
      if (heroLiveLang) heroLiveLang.textContent = state.lang || "기본";

      if (heroStartLink) {
        heroStartLink.href = firstStartHref
          ? withViewStateParams(firstStartHref, state)
          : "#library-shell";
      }

      if (heroBrowseLink) {
        heroBrowseLink.textContent = partCardsCount
          ? `${partCardsCount}개 파트 둘러보기`
          : "파트 둘러보기";
      }

      toolbarMetaValue.textContent = `${getTrackLabel(state.track)} / ${state.lang || "기본"}`;
      toolbarMetaCount.textContent = `${partCardsCount}개 파트`;
    }

    function render() {
      const langs = syncLanguageState();
      persistIndexViewState(state);
      try {
        const q = new URLSearchParams(location.search);
        q.set("track", state.track);
        const langParam = normalizeUiLangToParam(state.lang);
        if (langParam) q.set("lang", langParam);
        else q.delete("lang");
        const qs = q.toString();
        const nextUrl = `${location.pathname}${qs ? `?${qs}` : ""}${location.hash || ""}`;
        history.replaceState(null, "", nextUrl);
      } catch (_) {}

      renderTrackButtons();
      langLabel.textContent = getSecondaryFilterLabel(state.track);
      renderLanguageButtons(langs);

      list.innerHTML = "";
      if (state.track === "contest") {
        list.appendChild(createContestBatchPdfPanel());
      }

      const activeCategories = categories.filter(
        (cat) => getTrackFromCategory(cat) === state.track
      );
      const parts = groupByPart(activeCategories, sets);
      const cards = parts
        .map((part) => ({
          part,
          card: buildPartCard(part, state.lang, theoryByCategoryId, state),
        }))
        .filter((entry) => entry.card);

      const firstStartHref = (() => {
        const first = cards[0];
        if (!first) return "";
        const partEntry = getPartEntry(first.part, state.lang, theoryByCategoryId);
        return partEntry?.startHref || "";
      })();

      updateHeroSummary(cards.length, firstStartHref);

      if (!cards.length) {
        const empty = document.createElement("p");
        empty.className = "part-empty";
        empty.textContent = `${getTrackLabel(state.track)}에 등록된 파트가 없습니다.`;
        list.appendChild(empty);
        return;
      }

      cards.forEach((entry) => list.appendChild(entry.card));
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
