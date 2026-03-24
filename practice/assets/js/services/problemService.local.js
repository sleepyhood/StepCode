// practice/assets/js/services/problemService.local.js
const ProblemService = {
  async fetchJsonFirst(paths, errorMessage) {
    let lastError = null;
    for (const path of paths) {
      try {
        const res = await fetch(path);
        if (!res.ok) {
          lastError = new Error(`${errorMessage}: ${path}`);
          continue;
        }
        return res.json();
      } catch (err) {
        lastError = err;
      }
    }
    throw lastError || new Error(errorMessage);
  },

  mergeByKey(preferred, legacy, key) {
    const out = [];
    const seen = new Set();
    [preferred || [], legacy || []].forEach((items) => {
      items.forEach((item) => {
        const itemKey = String(item?.[key] || item?.categoryId || "");
        if (!itemKey || seen.has(itemKey)) return;
        seen.add(itemKey);
        out.push(item);
      });
    });
    return out;
  },

  excludeLegacyTrackWhenGeneratedExists(preferred, legacy, track) {
    const target = String(track || "").trim().toLowerCase();
    if (!target) return legacy || [];
    const hasPreferredTrack = (preferred || []).some(
      (item) => String(item?.track || "").trim().toLowerCase() === target
    );
    if (!hasPreferredTrack) return legacy || [];
    return (legacy || []).filter(
      (item) => String(item?.track || "").trim().toLowerCase() !== target
    );
  },

  async listCategories() {
    const [generated, legacy] = await Promise.all([
      this.fetchJsonFirst(
        [`${APP_CONFIG.dataBasePath}/generated/categories.json`],
        "failed to load generated categories"
      ).catch(() => []),
      this.fetchJsonFirst(
        [`${APP_CONFIG.dataBasePath}/categories.json`],
        "failed to load categories"
      ).catch(() => []),
    ]);
    const filteredLegacy = this.excludeLegacyTrackWhenGeneratedExists(
      generated,
      legacy,
      "canva"
    );
    return this.mergeByKey(generated, filteredLegacy, "id");
  },

  async listSets() {
    const [generated, legacy] = await Promise.all([
      this.fetchJsonFirst(
        [`${APP_CONFIG.dataBasePath}/generated/interactive.index.json`],
        "failed to load generated interactive index"
      ).catch(() => []),
      this.fetchJsonFirst(
        [`${APP_CONFIG.dataBasePath}/sets.index.json`],
        "failed to load sets index"
      ).catch(() => []),
    ]);
    return this.mergeByKey(generated, legacy, "id");
  },

  async loadSet(setId) {
    const sets = await this.listSets();
    const meta = sets.find((s) => s.id === setId);
    if (!meta) {
      throw new Error(`Unknown setId: ${setId}`);
    }

    const targetPath = meta.dataPath || `${APP_CONFIG.dataBasePath}/sets/${meta.file}`;
    const res = await fetch(targetPath);
    if (!res.ok) throw new Error(`failed to load set: ${meta.file || targetPath}`);
    return res.json();
  },

  async listTheoryIndex() {
    const [generated, legacy] = await Promise.all([
      this.fetchJsonFirst(
        [`${APP_CONFIG.dataBasePath}/generated/theory.index.json`],
        "failed to load generated theory index"
      ).catch(() => []),
      this.fetchJsonFirst(
        [`${APP_CONFIG.dataBasePath}/theory.index.json`],
        "failed to load theory index"
      ).catch(() => []),
    ]);
    const filteredLegacy = this.excludeLegacyTrackWhenGeneratedExists(
      generated,
      legacy,
      "canva"
    );
    return this.mergeByKey(generated, filteredLegacy, "conceptId");
  },

  async listWorksheetIndex() {
    return this.fetchJsonFirst(
      [`${APP_CONFIG.dataBasePath}/generated/worksheet.index.json`],
      "failed to load worksheet index"
    );
  },

  async getTheoryByConceptId(conceptId) {
    const items = await this.listTheoryIndex();
    return items.find((item) => item.conceptId === conceptId) || null;
  },

  async getTheoryByCategoryId(categoryId) {
    const items = await this.listTheoryIndex();
    return items.find((item) => item.categoryId === categoryId) || null;
  }
};
