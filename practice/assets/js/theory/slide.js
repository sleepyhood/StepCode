// 5. Marp Slide Mode
async function setupSlideMode(slidePath) {
  const toggleBtn = document.getElementById("theory-mode-toggle");
  const slideViewer = document.getElementById("theory-slide-viewer");
  const docContent = document.getElementById("theory-content");
  const marpContainer = document.getElementById("marp-container");
  if (!toggleBtn || !slideViewer || !marpContainer) return;

  let slides = [];
  let currentIndex = 0;
  let isSlideMode = false;

  try {
    const res = await fetch(slidePath.startsWith("./") ? slidePath.slice(2) : slidePath);
    if (!res.ok) return;
    const mdText = await res.text();
    const baseDir = slidePath.substring(0, slidePath.lastIndexOf("/"));

    const styleMatch = mdText.match(/style:\s*\|?\s*([\s\S]*?)(?=\n---)/);
    if (styleMatch) {
      const css = styleMatch[1].trim().replace(/@import\s+['"](.+?)['"]/g, (m, p) => `@import "${baseDir}/${p}"`);
      let styleTag = document.getElementById("marp-injected-style") || document.createElement("style");
      styleTag.id = "marp-injected-style";
      styleTag.textContent = css.replace(/section/g, "#marp-container section");
      document.head.appendChild(styleTag);
    }

    const md = getMdRenderer();
    const slideChunks = stripFrontMatter(mdText).split(/\n---\n/);
    let lastStage = "1";
    slides = slideChunks.map(chunk => {
      const sec = document.createElement("section");
      const mClass = chunk.match(/<!--\s*_class:\s*([\w-]+)\s*-->/);
      if (mClass) sec.className = mClass[1];
      
      const mStage = chunk.match(/<!--\s*_stage:\s*(\d+)\s*-->/);
      if (mStage) lastStage = mStage[1];
      sec.dataset.stage = lastStage;
      
      const mLocked = chunk.match(/<!--\s*_locked:\s*(true|false)\s*-->/);
      if (mLocked && mLocked[1] === "true") sec.dataset.locked = "true";
      
      const html = window.DOMPurify.sanitize(md.render(chunk));
      sec.innerHTML = replaceLangBadges(html);
      
      sec.querySelectorAll('code.language-mermaid').forEach(c => {
        const pre = c.closest('pre');
        const div = document.createElement('div');
        div.className = 'mermaid'; div.textContent = c.textContent;
        if (pre) pre.replaceWith(div);
      });
      
      fixRelativeImagePaths(sec, slidePath);
      enhanceCodeBlocks(sec);
      return sec;
    });

    if (slides.length > 0) {
      toggleBtn.hidden = false;
      // Option: Start in document mode by default if it's a lesson
      // enterSlideMode();
    }
  } catch (e) { console.error("Slide setup failed:", e); }

  function renderSlide(idx) {
    if (!isSlideMode) return;
    if (idx < 0 || idx >= slides.length) return;
    currentIndex = idx;
    marpContainer.innerHTML = "";
    
    const node = slides[currentIndex].cloneNode(true);
    const sw = slideViewer.clientWidth ? slideViewer.clientWidth - 40 : 1080;
    const scale = sw / 1280;
    
    node.style.cssText = `width:1280px;height:720px;transform:scale(${scale});transform-origin:top left;display:block;margin:0;position:absolute;top:0;left:0;`;
    marpContainer.style.height = `${720 * scale}px`;
    marpContainer.appendChild(node);
    
    // Mermaid render inside slide
    if (window.mermaid) {
      setTimeout(() => { 
        try { window.mermaid.init(undefined, node.querySelectorAll('.mermaid')); } catch (e) {} 
      }, 100);
    }
    
    const info = document.getElementById("slide-page-info");
    if (info) info.textContent = `${currentIndex + 1} / ${slides.length}`;
  }

  function enterSlideMode() {
    isSlideMode = true;
    const layout = document.querySelector(".theory-layout");
    const sidebar = document.querySelector(".theory-side");
    if (layout) { layout.style.display = "block"; layout.style.padding = "0"; }
    if (sidebar) sidebar.style.display = "none";
    slideViewer.style.display = "flex"; slideViewer.hidden = false;
    docContent.style.display = "none";
    const fw = document.getElementById("theory-filter-wrap"); if (fw) fw.style.display = "none";
    toggleBtn.textContent = "문서로 보기"; toggleBtn.classList.add("is-active");
    window.scrollTo(0, 0); renderSlide(currentIndex);
  }

  function enterDocumentMode() {
    isSlideMode = false;
    const layout = document.querySelector(".theory-layout");
    const sidebar = document.querySelector(".theory-side");
    if (layout) { layout.style.display = "grid"; layout.style.padding = ""; }
    if (sidebar) sidebar.style.display = "block";
    slideViewer.style.display = "none"; slideViewer.hidden = true;
    docContent.style.display = "block";
    const fw = document.getElementById("theory-filter-wrap"); if (fw) fw.style.display = "block";
    toggleBtn.textContent = "슬라이드 보기"; toggleBtn.classList.remove("is-active");
  }

  toggleBtn.onclick = (e) => { e.preventDefault(); if (isSlideMode) enterDocumentMode(); else enterSlideMode(); };
  document.getElementById("slide-prev").onclick = () => renderSlide(currentIndex - 1);
  document.getElementById("slide-next").onclick = () => renderSlide(currentIndex + 1);
  
  document.addEventListener("keydown", (e) => {
    if (!isSlideMode) return;
    if (e.key === "ArrowLeft") renderSlide(currentIndex - 1);
    if (e.key === "ArrowRight") renderSlide(currentIndex + 1);
  });
}
