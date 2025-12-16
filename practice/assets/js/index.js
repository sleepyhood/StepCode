// practice/assets/js/index.js
// 개선: 카테고리는 카드/아코디언(기본 접힘), 회차는 '칩'으로 압축, 검색 추가

// 카테고리에서 언어 이름 뽑기 (예: "C - 조건문" → "C")
function getLangFromCategory(cat) {
  if (cat.lang) return cat.lang; // (선택) categories.json에 lang 필드를 넣으면 이걸 우선 사용
  if (typeof cat.name === "string") {
    const parts = cat.name.split("-");
    return parts[0].trim();
  }
  return "기타";
}

function normalize(s) {
  return String(s || "").toLowerCase().replace(/\s+/g, " ").trim();
}

// 언어 필터 버튼 생성
function createFilterButton(label, lang, isActive) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = "filter-btn";
  if (isActive) btn.classList.add("active");
  btn.dataset.lang = lang;
  btn.textContent = label;
  return btn;
}

// 회차 칩 생성 (세로 리스트 대신)
function createSetChip(setItem, shortLabel, diffLabel) {
  const a = document.createElement("a");
  a.className = "set-chip";
  a.href = `practice.html?set=${encodeURIComponent(setItem.id)}`;
  a.dataset.diff = setItem.difficulty || "basic";

  const main = document.createElement("span");
  main.className = "set-chip-main";
  main.textContent = shortLabel;

  const sub = document.createElement("span");
  sub.className = "set-chip-sub";
  sub.textContent = diffLabel;

  const tiny = document.createElement("span");
  tiny.className = "set-chip-tiny";
  if (typeof setItem.numProblems === "number") {
    tiny.textContent = `${setItem.numProblems}문항`;
  } else {
    tiny.textContent = "";
  }

  a.title = setItem.title;
  // 검색용 텍스트(제목/회차/라벨)
  a.dataset.search = `${shortLabel} ${diffLabel} ${setItem.round ?? ""}회차 ${setItem.title ?? ""}`;

  a.appendChild(main);
  a.appendChild(sub);
  if (tiny.textContent) a.appendChild(tiny);

  return a;
}

document.addEventListener("DOMContentLoaded", async () => {
  const root = document.getElementById("list-root");
  root.textContent = "문제 목록을 불러오는 중입니다...";

  try {
    const [categories, sets] = await Promise.all([
      ProblemService.listCategories(),
      ProblemService.listSets()
    ]);

    // 카테고리 순서대로 정렬
    categories.sort((a, b) => (a.order || 0) - (b.order || 0));

    root.innerHTML = "";

    // ===== 1) 언어 목록 추출 후 필터 바 만들기 =====
    const langSet = new Set();
    categories.forEach((cat) => langSet.add(getLangFromCategory(cat)));
    const langs = Array.from(langSet);

    const controls = document.createElement("div");
    controls.className = "top-controls";

    const filterBar = document.createElement("div");
    filterBar.className = "filter-bar";
    filterBar.appendChild(createFilterButton("전체", "all", true));
    langs.forEach((lang) => filterBar.appendChild(createFilterButton(lang, lang, false)));

    const searchRow = document.createElement("div");
    searchRow.className = "search-row";

    const searchInput = document.createElement("input");
    searchInput.className = "search-input";
    searchInput.type = "search";
    searchInput.placeholder = "단원/회차 검색 (예: 조건, if, 3회차, 기초2)";
    searchInput.autocomplete = "off";

    const collapseAllBtn = document.createElement("button");
    collapseAllBtn.type = "button";
    collapseAllBtn.className = "action-btn";
    collapseAllBtn.textContent = "모두 접기";

    searchRow.appendChild(searchInput);
    searchRow.appendChild(collapseAllBtn);

    controls.appendChild(filterBar);
    controls.appendChild(searchRow);

    const listContainer = document.createElement("div");
    listContainer.id = "category-list";

    root.appendChild(controls);
    root.appendChild(listContainer);

    // ===== 2) 카테고리 + 세트 목록 렌더링 (기본 접힘 + 칩) =====
    for (const cat of categories) {
      const catSets = sets
        .filter((s) => s.categoryId === cat.id)
        .sort((a, b) => (a.round || 0) - (b.round || 0));

      if (catSets.length === 0) continue;

      const section = document.createElement("section");
      section.className = "category-section collapsed"; // ✅ 기본 접힘
      const lang = getLangFromCategory(cat);
      section.dataset.lang = lang;
      section.dataset.catname = cat.name || "";

      // 헤더(제목 + 메타 + 접기 버튼)
      const headerRow = document.createElement("div");
      headerRow.className = "category-header-row";

      const titleWrap = document.createElement("div");
      titleWrap.className = "category-title-wrap";

      const h2 = document.createElement("h2");
      h2.textContent = cat.name;

      const basicSets = catSets.filter(s => (s.difficulty || "basic") !== "challenge");
      const challengeSets = catSets.filter(s => (s.difficulty || "basic") === "challenge");

      const meta = document.createElement("div");
      meta.className = "category-meta";
      meta.textContent = `기초 ${basicSets.length} · 챌린지 ${challengeSets.length} · 총 ${catSets.length}`;

      titleWrap.appendChild(h2);
      titleWrap.appendChild(meta);

      const toggleBtn = document.createElement("button");
      toggleBtn.type = "button";
      toggleBtn.className = "cat-toggle";
      toggleBtn.innerHTML = "▾";

      headerRow.appendChild(titleWrap);
      headerRow.appendChild(toggleBtn);
      section.appendChild(headerRow);

      // 세트(회차) 영역: 그룹(기초/챌린지) + 칩
      const setContainer = document.createElement("div");
      setContainer.className = "set-container";

      function addGroup(groupTitle, groupSets, prefix) {
        if (!groupSets.length) return;

        const group = document.createElement("div");
        group.className = "set-group";

        const gTitle = document.createElement("div");
        gTitle.className = "set-group-title";
        gTitle.textContent = groupTitle;

        const chips = document.createElement("div");
        chips.className = "set-chip-row";

        groupSets.forEach((s, idx) => {
          // 표시 라벨은 round 대신 그룹 내 순번 기준(B1/B2..., C1/C2...)
          const shortLabel = `${prefix}${idx + 1}`;
          const diffLabel = (s.difficulty === "challenge") ? "챌린지" : "기초";
          chips.appendChild(createSetChip(s, shortLabel, diffLabel));
        });

        group.appendChild(gTitle);
        group.appendChild(chips);
        setContainer.appendChild(group);
      }

      addGroup("기초", basicSets, "B");
      addGroup("챌린지", challengeSets, "C");

      section.appendChild(setContainer);
      listContainer.appendChild(section);

      // 카테고리 접기/펼치기
      headerRow.addEventListener("click", () => {
        section.classList.toggle("collapsed");
      });
    }

    // ===== 3) 필터 + 검색 동작(동시에 적용) =====
    const state = { lang: "all", query: "" };

    function updateVisibility() {
      const q = normalize(state.query);

      document.querySelectorAll(".category-section").forEach((sec) => {
        // 1) 언어 필터
        const langOk = (state.lang === "all" || sec.dataset.lang === state.lang);
        if (!langOk) {
          sec.style.display = "none";
          return;
        }

        // 2) 검색
        const catName = sec.dataset.catname || "";
        const catMatch = q && normalize(catName).includes(q);

        let anyVisible = false;

        sec.querySelectorAll(".set-group").forEach((group) => {
          let groupVisible = false;

          group.querySelectorAll(".set-chip").forEach((chip) => {
            // 카테고리명이 매치면 해당 카테고리의 모든 칩을 보여줌
            const text = chip.dataset.search || "";
            const match = !q || catMatch || normalize(text).includes(q);
            chip.style.display = match ? "" : "none";
            if (match) {
              groupVisible = true;
              anyVisible = true;
            }
          });

          group.style.display = groupVisible ? "" : "none";
        });

        // 카테고리명만 매치했는데 칩을 숨겨버릴 상황을 방지
        if (catMatch) anyVisible = true;

        sec.style.display = (!q || anyVisible) ? "" : "none";

        // 검색 중이면 자동 펼침
        if (q && anyVisible) sec.classList.remove("collapsed");
      });
    }

    // 언어 필터 클릭
    filterBar.addEventListener("click", (e) => {
      const btn = e.target.closest(".filter-btn");
      if (!btn) return;

      state.lang = btn.dataset.lang;

      // 버튼 active 토글
      filterBar.querySelectorAll(".filter-btn").forEach((b) => {
        b.classList.toggle("active", b === btn);
      });

      updateVisibility();
    });

    // 검색 입력
    searchInput.addEventListener("input", (e) => {
      state.query = e.target.value;
      updateVisibility();
    });

    // 모두 접기
    collapseAllBtn.addEventListener("click", () => {
      document.querySelectorAll(".category-section").forEach((sec) => sec.classList.add("collapsed"));
    });

    // 초기 적용
    updateVisibility();

  } catch (err) {
    console.error(err);
    root.textContent = "목록을 불러오는 중 오류가 발생했습니다.";
  }
});
