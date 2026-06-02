// 6. Auxiliary UI Enhancers
function enhanceLessonCallouts(root) {
  root.querySelectorAll("blockquote").forEach(q => {
    const m = q.textContent.match(/\[!(\w+)\]/);
    if (m) q.classList.add("lesson-callout", `lesson-callout--${m[1].toLowerCase()}`);
  });
}
function enhanceCodeBlocks(root) {
  root.querySelectorAll("pre > code").forEach(c => {
    const pre = c.closest("pre");
    if (pre) { 
      pre.classList.add("line-numbers", "theory-code"); 
      if (window.Prism) window.Prism.highlightElement(c); 
    }
  });
}
function enhanceTraceGridBlocks(root) {}
function enhanceIoBlocks(root) {}

// 6.5. Section Card Wrapping (H1/H2 → Card containers)
function wrapContentIntoSectionCards(root) {
  const dividers = root.querySelectorAll('.theory-slide-divider');
  // Only wrap if dividers exist (slide-based content)
  if (dividers.length === 0) return;

  const allChildren = Array.from(root.childNodes);
  const sections = [];
  let currentSection = [];

  allChildren.forEach(node => {
    if (node.classList && node.classList.contains('theory-slide-divider')) {
      if (currentSection.length > 0) {
        sections.push(currentSection);
        currentSection = [];
      }
    } else {
      currentSection.push(node);
    }
  });
  if (currentSection.length > 0) sections.push(currentSection);

  root.innerHTML = '';
  sections.forEach((nodes, idx) => {
    if (nodes.length === 0) return;
    // Skip purely whitespace sections
    const hasContent = nodes.some(n => n.textContent?.trim().length > 0);
    if (!hasContent) return;

    const card = document.createElement('div');
    card.className = 'theory-section-card';
    card.dataset.sectionIndex = idx;
    nodes.forEach(n => card.appendChild(n));
    root.appendChild(card);
  });
}

// 6.6. Progress Tracking
function updateSectionProgress() {
  // Count legacy cards, mini-check-cards, and new MCQ cards
  const legacyCards  = document.querySelectorAll('.interactive-problem-card');
  const miniCards    = document.querySelectorAll('.theory-mini-check-card');
  const mcqCards     = document.querySelectorAll('.theory-mcq-card');
  const total  = legacyCards.length + miniCards.length + mcqCards.length;
  const solved = document.querySelectorAll('.interactive-problem-card.is-solved').length
               + document.querySelectorAll('.theory-mini-check-card.is-solved').length
               + document.querySelectorAll('.theory-mcq-card.is-solved').length;

  const milestoneEl = document.getElementById('dashboard-milestone-count');
  if (milestoneEl) milestoneEl.textContent = `${solved}/${total}`;

  const statusEl = document.getElementById('dashboard-status-text');
  if (statusEl) {
    if (total === 0) statusEl.textContent = 'Reading in progress...';
    else if (solved === total) statusEl.textContent = '🎉 All milestones complete!';
    else statusEl.textContent = `${solved} of ${total} milestones completed`;
  }

  const pct = total > 0 ? Math.round((solved / total) * 100) : 0;
  const bar = document.getElementById('roadmap-progress-bar');
  const txt = document.getElementById('roadmap-progress-text');
  if (bar) bar.style.width = pct + '%';
  if (txt) txt.textContent = pct + '% Complete';
}

// 6.7. Mini Check Card Logic (theory-mini-check-card)
function setupMiniCheckCards(root) {
  const cards = root.querySelectorAll('.theory-mini-check-card');
  if (cards.length === 0) return;

  cards.forEach(card => {
    // Prevent double-binding if re-rendered
    if (card.dataset.bound === 'true') return;
    card.dataset.bound = 'true';

    const expectedAnswer = (card.dataset.answer || '').trim();
    const input = card.querySelector('.stage-key-input');
    const btn = card.querySelector('.stage-unlock-btn');

    if (!input || !btn || !expectedAnswer) return;

    // Normalize helper: remove all whitespace for flexible matching
    const normalize = (s) => s.replace(/\s+/g, '').toLowerCase();

    const pageKey = window.location.pathname + window.location.search;
    const storageKey = `stepcode_mini_${pageKey}_${expectedAnswer}`;

    // Restore state
    if (localStorage.getItem(storageKey) === 'solved') {
      card.classList.add('is-solved');
      input.value = expectedAnswer;
      input.disabled = true;
      btn.disabled = true;
      btn.textContent = '✓ 완료!';
      btn.classList.add('is-correct-btn');
    }

    const submit = () => {
      if (card.classList.contains('is-solved')) return; // Already solved

      const val = input.value;
      const isCorrect = normalize(val) === normalize(expectedAnswer);

      if (isCorrect) {
        card.classList.add('is-solved');
        input.disabled = true;
        btn.disabled = true;
        btn.textContent = '✓ 완료!';
        btn.classList.add('is-correct-btn');
        localStorage.setItem(storageKey, 'solved');
        updateSectionProgress();
      } else {
        input.classList.add('is-wrong');
        input.classList.add('shake');
        setTimeout(() => {
          input.classList.remove('is-wrong', 'shake');
        }, 600);
      }
    };

    btn.addEventListener('click', submit);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') submit();
    });
  });
}

function setupMCQCards(root) {
  const cards = root.querySelectorAll('.theory-mcq-card');
  if (cards.length === 0) return;

  cards.forEach((card, index) => {
    if (card.dataset.bound === 'true') return;
    card.dataset.bound = 'true';

    const pageKey = window.location.pathname + window.location.search;
    const storageKey = `stepcode_mcq_${pageKey}_${index}`;
    
    const options = card.querySelectorAll('.mcq-option');
    const hintBox = card.querySelector('.mcq-hint');

    if (localStorage.getItem(storageKey) === 'solved') {
      card.classList.add('is-solved');
      options.forEach(opt => opt.classList.add('is-disabled'));
      const correctOpt = Array.from(options).find(opt => opt.dataset.correct === 'true');
      if (correctOpt) correctOpt.classList.add('is-selected');
    }

    options.forEach(opt => {
      opt.addEventListener('click', () => {
        if (card.classList.contains('is-solved')) return;

        options.forEach(o => o.classList.remove('is-wrong'));
        if (hintBox) {
          hintBox.classList.remove('is-visible');
          hintBox.textContent = '';
        }

        const isCorrect = opt.dataset.correct === 'true';

        if (isCorrect) {
          card.classList.add('is-solved');
          opt.classList.add('is-selected');
          options.forEach(o => o.classList.add('is-disabled'));
          if (hintBox) {
            hintBox.textContent = '✅ 정답입니다!';
            hintBox.classList.add('is-visible');
            hintBox.style.color = '#065f46';
            hintBox.style.backgroundColor = '#ecfdf5';
            hintBox.style.borderColor = '#a7f3d0';
          }
          localStorage.setItem(storageKey, 'solved');
          updateSectionProgress();
        } else {
          opt.classList.add('is-wrong');
          if (hintBox && opt.dataset.hint) {
            hintBox.textContent = '💡 ' + opt.dataset.hint;
            hintBox.classList.add('is-visible');
            hintBox.style.color = '#854d0e';
            hintBox.style.backgroundColor = '#fefce8';
            hintBox.style.borderColor = '#fef08a';
          }
        }
      });
    });
  });
}

function initTeacherMode() {
  const params = new URLSearchParams(window.location.search);
  if (params.get('teacher') === '1') {
    if (document.querySelector('.teacher-toggle-btn')) return;
    
    const btn = document.createElement('button');
    btn.className = 'teacher-toggle-btn is-active';
    btn.innerHTML = '👁️ 정답 보기 ON';
    let isRevealed = true;
    
    document.querySelectorAll('.theory-mcq-card, .theory-mini-check-card').forEach(c => c.classList.add('show-answer'));
    
    btn.onclick = () => {
      isRevealed = !isRevealed;
      if (isRevealed) {
        btn.innerHTML = '👁️ 정답 보기 ON';
        btn.classList.add('is-active');
        document.querySelectorAll('.theory-mcq-card, .theory-mini-check-card').forEach(c => c.classList.add('show-answer'));
      } else {
        btn.innerHTML = '👀 정답 보기 OFF';
        btn.classList.remove('is-active');
        document.querySelectorAll('.theory-mcq-card, .theory-mini-check-card').forEach(c => c.classList.remove('show-answer'));
      }
    };
    
    document.body.appendChild(btn);
  }
}

// 8. Auto Numbering & Floating Navigation
function autoNumberHeadings(root) {
  const headings = Array.from(root.querySelectorAll("h1, h2, h3, h4, h5, h6"));
  if (headings.length === 0) return;

  let minLevel = 6;
  headings.forEach(h => {
    const level = parseInt(h.tagName.charAt(1));
    if (level < minLevel) minLevel = level;
  });

  const counters = [0, 0, 0, 0, 0, 0, 0];
  headings.forEach(h => {
    if (h.closest('.interactive-problem-card') || h.closest('.theory-mini-check-card') || h.closest('.theory-toc-popup')) return;
    const level = parseInt(h.tagName.charAt(1));
    if(level > 6 || level < 1) return;

    counters[level]++;
    for (let i = level + 1; i <= 6; i++) counters[i] = 0;

    // Check if the heading already starts with a number (e.g. "1. ", "1.1 ", "1.1. ")
    if (/^\s*\d+(\.\d+)*\.?\s/.test(h.textContent)) {
      return; // Skip adding generated number span
    }

    let numberStr = "";
    for (let i = minLevel; i <= level; i++) numberStr += counters[i] + ".";

    const numSpan = document.createElement("span");
    numSpan.className = "theory-heading-number";
    numSpan.textContent = numberStr + " ";
    h.insertBefore(numSpan, h.firstChild);
  });
}

function buildFloatingTOC(root) {
  let existing = document.querySelector(".theory-floating-widget");
  if (existing) existing.remove();

  const headings = root.querySelectorAll("h1, h2, h3");
  if (headings.length === 0) return;

  const widget = document.createElement("div");
  widget.className = "theory-floating-widget";
  widget.innerHTML = `
    <div id="theory-toc-popup" class="theory-toc-popup hidden">
      <div class="toc-header">목차</div>
      <div class="toc-content" id="theory-toc-content"></div>
    </div>
    <button id="theory-toc-btn" class="floating-btn" title="목차">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
    </button>
    <button id="theory-top-btn" class="floating-btn" title="맨 위로">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
    </button>
    <button id="theory-bottom-btn" class="floating-btn" title="맨 아래로">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M5 12l7 7 7-7"/></svg>
    </button>
  `;
  document.body.appendChild(widget);

  const tocContent = document.getElementById("theory-toc-content");
  headings.forEach((h, i) => {
    if (!h.id) h.id = "heading-" + i;
    const a = document.createElement("a");
    a.href = "#" + h.id;
    a.textContent = h.textContent;
    a.className = "theory-toc-item level-" + h.tagName.charAt(1);
    a.onclick = (e) => {
      e.preventDefault();
      const y = h.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({top: y, behavior: "smooth"});
    };
    tocContent.appendChild(a);
  });

  const tocBtn = document.getElementById("theory-toc-btn");
  const topBtn = document.getElementById("theory-top-btn");
  const bottomBtn = document.getElementById("theory-bottom-btn");
  const popup = document.getElementById("theory-toc-popup");

  tocBtn.onclick = () => popup.classList.toggle("hidden");
  document.addEventListener("click", (e) => { if (!widget.contains(e.target)) popup.classList.add("hidden"); });
  topBtn.onclick = () => window.scrollTo({top: 0, behavior: 'smooth'});
  bottomBtn.onclick = () => window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});
}

function buildRoadmap(root) {
  let query = "h1, h2, h3";
  if (root.classList.contains("is-section-mode")) {
    query = "h1, h2"; // Hide h3 in section mode to avoid roadmap overload
  }
  const headings = Array.from(root.querySelectorAll(query));
  if (headings.length === 0) return;

  const container = document.getElementById("theory-roadmap-container");
  if (!container) return;
  container.innerHTML = "";

  const progressLine = document.createElement("div");
  progressLine.className = "roadmap-progress-line";
  progressLine.id = "roadmap-progress-line";
  container.appendChild(progressLine);

  headings.forEach((h, i) => {
    if (!h.id) h.id = "heading-" + i;
    const node = document.createElement("a");
    node.href = "#" + h.id;
    node.className = "roadmap-node";
    const level = parseInt(h.tagName.charAt(1));
    if (level === 3) node.style.marginLeft = "12px";

    node.title = h.textContent;

    const match = h.textContent.match(/^([\d\.]+)\s+(.*)/);
    let num = "", text = h.textContent;
    if (match) { num = match[1]; text = match[2]; }

    node.innerHTML = `
      <div class="roadmap-dot" data-num="${i + 1}"></div>
      <div class="roadmap-text">
        <span class="roadmap-num">${num}</span>
        <span class="roadmap-title-text">${text}</span>
      </div>
    `;
    node.onclick = (e) => {
      e.preventDefault();
      const y = h.getBoundingClientRect().top + window.scrollY - 80;
      window.scrollTo({top: y, behavior: "smooth"});
    };
    container.appendChild(node);
  });

  const toggleBtn = document.getElementById("roadmap-toggle-btn");
  const stickyContainer = document.getElementById("theory-roadmap-sticky");
  if (toggleBtn && stickyContainer && !toggleBtn.dataset.bound) {
    toggleBtn.dataset.bound = "true";
    toggleBtn.onclick = () => {
      stickyContainer.classList.toggle("is-expanded");
      const icon = toggleBtn.querySelector("path");
      icon.setAttribute("d", stickyContainer.classList.contains("is-expanded") ? "M15 18l-6-6 6-6" : "M9 18l6-6-6-6");
    };
  }
  setupRoadmapScrollSpy(headings);
}

function setupRoadmapScrollSpy(headings) {
  const nodes = document.querySelectorAll(".roadmap-node");
  const progressLine = document.getElementById("roadmap-progress-line");
  if(nodes.length === 0) return;

  const updateScroll = () => {
    let currentIndex = 0;
    const scrollY = window.scrollY;
    if (scrollY > 150) localStorage.setItem(`readPosition_${window.location.search}`, scrollY);
    else if (scrollY <= 150) localStorage.removeItem(`readPosition_${window.location.search}`);
    
    headings.forEach((h, i) => {
      const top = h.getBoundingClientRect().top + scrollY - 150;
      if (scrollY >= top) currentIndex = i;
    });

    // Bottom-of-page detection: if scrolled to within 50px of the document bottom,
    // force-activate the last heading so the final node & section are always highlighted.
    const atBottom = (window.innerHeight + scrollY) >= (document.documentElement.scrollHeight - 50);
    if (atBottom && headings.length > 0) {
      currentIndex = headings.length - 1;
    }

    nodes.forEach((node, i) => {
      node.classList.remove("is-active", "is-past");
      if (i < currentIndex) node.classList.add("is-past");
      else if (i === currentIndex) node.classList.add("is-active");
    });

    // Sync active node into view inside the roadmap sidebar
    const activeNode = nodes[currentIndex];
    if (activeNode) {
      const sticky = document.getElementById('theory-roadmap-sticky');
      if (sticky) {
        const nodeTop = activeNode.offsetTop;
        const stickyScroll = sticky.scrollTop;
        const stickyH = sticky.clientHeight;
        if (nodeTop < stickyScroll + 60 || nodeTop > stickyScroll + stickyH - 60) {
          sticky.scrollTo({ top: nodeTop - stickyH / 2, behavior: 'smooth' });
        }
      }
    }

    // Section card active/inactive dim effect
    const sectionCards = document.querySelectorAll('.theory-section-card');
    if (sectionCards.length > 0) {
      const activeHeading = headings[currentIndex];
      sectionCards.forEach(card => {
        if (card.contains(activeHeading)) {
          card.classList.add('is-active');
          card.classList.remove('is-inactive');
        } else {
          card.classList.remove('is-active');
          card.classList.add('is-inactive');
        }
      });
    }

    if (activeNode) progressLine.style.height = (activeNode.offsetTop + 7) + "px";
  };
  window.addEventListener('scroll', updateScroll);
  setTimeout(updateScroll, 100);
}
