// practice/assets/js/index.js

// 카테고리에서 언어 이름 뽑기 (예: "C - 조건문" → "C")
function getLangFromCategory(cat) {
  if (cat.lang) return cat.lang; // 나중에 categories.json에 lang 필드를 넣으면 이걸 우선 사용
  if (typeof cat.name === "string") {
    const parts = cat.name.split("-");
    return parts[0].trim();
  }
  return "기타";
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
    categories.forEach((cat) => {
      langSet.add(getLangFromCategory(cat));
    });
    const langs = Array.from(langSet);

    const filterBar = document.createElement("div");
    filterBar.className = "filter-bar";

    // "전체" 버튼
    filterBar.appendChild(createFilterButton("전체", "all", true));
    // 언어별 버튼
    langs.forEach((lang) => {
      filterBar.appendChild(createFilterButton(lang, lang, false));
    });

    const listContainer = document.createElement("div");
    listContainer.id = "category-list";

    root.appendChild(filterBar);
    root.appendChild(listContainer);

    // ===== 2) 카테고리 + 세트 목록 렌더링 =====
    for (const cat of categories) {
      const catSets = sets
        .filter((s) => s.categoryId === cat.id)
        .sort((a, b) => (a.round || 0) - (b.round || 0));

      if (catSets.length === 0) continue;

      const section = document.createElement("section");
      section.className = "category-section";
      const lang = getLangFromCategory(cat);
      section.dataset.lang = lang;

      // 헤더(제목 + 접기 버튼)
      const headerRow = document.createElement("div");
      headerRow.className = "category-header-row";

      const h2 = document.createElement("h2");
      h2.textContent = cat.name;

      const toggleBtn = document.createElement("button");
      toggleBtn.type = "button";
      toggleBtn.className = "cat-toggle";
      toggleBtn.innerHTML = "▾";

      headerRow.appendChild(h2);
      headerRow.appendChild(toggleBtn);
      section.appendChild(headerRow);

      // 세트 목록
      const ul = document.createElement("ul");
      ul.className = "set-list";

      for (const s of catSets) {
        const li = document.createElement("li");
        li.className = "set-item";

        const link = document.createElement("a");
        link.href = `practice.html?set=${encodeURIComponent(s.id)}`;

        // 제목 영역
        const titleSpan = document.createElement("span");
        titleSpan.className = "set-title";
        titleSpan.textContent = `${s.round}회차. ${s.title}`;

        // 난이도 뱃지
        const diff = s.difficulty || "basic";
        const badge = document.createElement("span");
        badge.className = "set-badge";
        badge.dataset.diff = diff;
        badge.textContent = diff === "challenge" ? "챌린지" : "기초";

        link.appendChild(titleSpan);
        link.appendChild(badge);

        li.appendChild(link);
        ul.appendChild(li);
      }

      section.appendChild(ul);
      listContainer.appendChild(section);

      // 카테고리 접기/펼치기
      headerRow.addEventListener("click", () => {
        section.classList.toggle("collapsed");
      });
    }

    // ===== 3) 언어 필터 동작 =====
    filterBar.addEventListener("click", (e) => {
      const btn = e.target.closest(".filter-btn");
      if (!btn) return;

      const lang = btn.dataset.lang;

      // 버튼 active 토글
      filterBar.querySelectorAll(".filter-btn").forEach((b) => {
        b.classList.toggle("active", b === btn);
      });

      // 섹션 표시/숨김
      document.querySelectorAll(".category-section").forEach((sec) => {
        if (lang === "all" || sec.dataset.lang === lang) {
          sec.style.display = "";
        } else {
          sec.style.display = "none";
        }
      });
    });

  } catch (err) {
    console.error(err);
    root.textContent = "목록을 불러오는 중 오류가 발생했습니다.";
  }
});
