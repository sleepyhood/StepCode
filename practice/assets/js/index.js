// practice/assets/js/index.js
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

    for (const cat of categories) {
      const catSets = sets
        .filter((s) => s.categoryId === cat.id)
        .sort((a, b) => (a.round || 0) - (b.round || 0));

      if (catSets.length === 0) continue;

      const section = document.createElement("section");
      section.className = "category-section";

      const h2 = document.createElement("h2");
      h2.textContent = cat.name;
      section.appendChild(h2);

      const ul = document.createElement("ul");
      ul.className = "set-list";

      for (const s of catSets) {
        const li = document.createElement("li");
        li.className = "set-item";

        const link = document.createElement("a");
        link.href = `practice.html?set=${encodeURIComponent(s.id)}`;
        link.textContent = `${s.round}회차. ${s.title}`;
        li.appendChild(link);

        ul.appendChild(li);
      }

      section.appendChild(ul);
      root.appendChild(section);
    }
  } catch (err) {
    console.error(err);
    root.textContent = "목록을 불러오는 중 오류가 발생했습니다.";
  }
});
