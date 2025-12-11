// practice/assets/js/services/problemService.local.js
const ProblemService = {
  async listCategories() {
    const res = await fetch(`${APP_CONFIG.dataBasePath}/categories.json`);
    if (!res.ok) throw new Error("failed to load categories");
    return res.json();
  },

  async listSets() {
    const res = await fetch(`${APP_CONFIG.dataBasePath}/sets.index.json`);
    if (!res.ok) throw new Error("failed to load sets index");
    return res.json();
  },

  async loadSet(setId) {
    const sets = await this.listSets();
    const meta = sets.find((s) => s.id === setId);
    if (!meta) {
      throw new Error(`Unknown setId: ${setId}`);
    }

    const res = await fetch(
      `${APP_CONFIG.dataBasePath}/sets/${meta.file}`
    );
    if (!res.ok) throw new Error(`failed to load set: ${meta.file}`);
    return res.json();
  }
};
