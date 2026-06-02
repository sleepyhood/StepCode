// 1. Core Utilities
function getMdRenderer() {
  if (!window.markdownit || !window.DOMPurify) return null;
  return window.markdownit({ html: true, linkify: true, breaks: true });
}

function stripFrontMatter(mdText) {
  const raw = String(mdText || "").replace(/\r\n?/g, "\n");
  if (!raw.startsWith("---\n")) return raw;
  const end = raw.indexOf("\n---\n", 4);
  return end === -1 ? raw : raw.slice(end + 5);
}

function replaceLangBadges(html) {
  if (!html) return "";
  return html.replace(/\{lang:([^}]+)\}/g, (match, lang) => {
    const l = lang.toLowerCase();
    const map = { "python": "Python", "c": "C", "java": "Java", "csharp": "C#" };
    const label = map[l] || lang.toUpperCase();
    return `<span class="theory-lang-badge theory-lang-badge--${l}">${label}</span>`;
  });
}

function replaceCheckboxes(html) {
  if (!html) return "";
  // Converts [ ] and [x] into interactive-looking checkboxes and wraps text for styling
  return html
    .replace(/(<li>|<p>)\s*\[ \]\s*(.*?)(<\/li>|<\/p>)/g, 
      '$1<label class="theory-task-item"><input type="checkbox" class="theory-checkbox"> <span class="theory-task-text">$2</span></label>$3')
    .replace(/(<li>|<p>)\s*\[x\]\s*(.*?)(<\/li>|<\/p>)/gi, 
      '$1<label class="theory-task-item"><input type="checkbox" class="theory-checkbox" checked> <span class="theory-task-text">$2</span></label>$3');
}

function fixRelativeImagePaths(root, mdPath) {
  if (!mdPath) return;
  const baseDir = mdPath.substring(0, mdPath.lastIndexOf("/"));
  root.querySelectorAll("img").forEach(img => {
    const src = img.getAttribute("src");
    if (src && !src.startsWith("http") && !src.startsWith("data:") && !src.startsWith("/")) {
      img.src = baseDir + (src.startsWith("./") ? src.slice(1) : "/" + src);
    }
  });
}

// 3. Markdown Rendering
async function renderTheoryMarkdown(target, mdText, mdPath = "") {
  const raw = stripFrontMatter(mdText);
  const md = getMdRenderer();
  if (!md) { target.textContent = raw; return; }
  
  // Render as a single comprehensive document
  const rawHtml = md.render(raw);
  const cleanHtml = window.DOMPurify.sanitize(rawHtml);
  let finalHtml = replaceLangBadges(cleanHtml);
  finalHtml = replaceCheckboxes(finalHtml);
  
  // Convert standard <hr> into a stylish slide divider
  finalHtml = finalHtml.replace(/<hr\s*\/?>/gi, '<div class="theory-slide-divider"></div>');
  
  target.innerHTML = finalHtml;
  
  // Flag as section-mode if dividers are detected (useful for roadmap filtering)
  if (finalHtml.includes('theory-slide-divider')) {
    target.classList.add("is-section-mode");
  } else {
    target.classList.remove("is-section-mode");
  }
  
  // Mermaid Detection
  target.querySelectorAll('code.language-mermaid').forEach(c => {
    const pre = c.closest('pre');
    const div = document.createElement('div');
    div.className = 'mermaid';
    div.textContent = c.textContent;
    if (pre) pre.replaceWith(div);
  });

  if (window.mermaid && target.querySelectorAll('.mermaid').length > 0) {
    const renderMermaid = () => {
      // Visibility check to prevent translate(undefined) errors
      if (target.offsetWidth > 0 || target.offsetHeight > 0) {
        try { 
          window.mermaid.init(undefined, target.querySelectorAll('.mermaid')); 
        } catch (e) {
          console.warn("Mermaid init failed, retrying...", e);
        }
      } else {
        setTimeout(renderMermaid, 500);
      }
    };
    setTimeout(renderMermaid, 300);
  }

  fixRelativeImagePaths(target, mdPath);
  enhanceLessonCallouts(target);
  enhanceCodeBlocks(target);
  enhanceTraceGridBlocks(target);
  enhanceIoBlocks(target);
  await enhanceInteractiveProblems(target);
  autoNumberHeadings(target);
  wrapContentIntoSectionCards(target);
  setupMiniCheckCards(target);
  setupMCQCards(target);
  buildFloatingTOC(target);
  buildRoadmap(target);
  updateSectionProgress();
  
  if (!window.teacherModeInitialized) {
    initTeacherMode();
    window.teacherModeInitialized = true;
  }
}
