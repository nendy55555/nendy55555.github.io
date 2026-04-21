/* ============================================================
   Shared JS for architecture pages.
   Scroll-progress rail + § copy-link anchors on section-heads.
   Added 2026-04-21. Mirrors index.html patterns.
   ============================================================ */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Inject DOM (rail + toast) once per page --- */
  function ensureDom() {
    if (!document.querySelector('.scroll-rail')) {
      var rail = document.createElement('div');
      rail.className = 'scroll-rail';
      rail.setAttribute('aria-hidden', 'true');
      var fill = document.createElement('div');
      fill.className = 'scroll-rail-fill';
      rail.appendChild(fill);
      document.body.appendChild(rail);
    }
    if (!document.getElementById('uiToast')) {
      var t = document.createElement('div');
      t.className = 'toast';
      t.id = 'uiToast';
      t.setAttribute('role', 'status');
      t.setAttribute('aria-live', 'polite');
      document.body.appendChild(t);
    }
  }

  function showToast(message) {
    var toast = document.getElementById('uiToast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('open');
    if (toast._timer) clearTimeout(toast._timer);
    toast._timer = setTimeout(function () { toast.classList.remove('open'); }, 1200);
  }

  /* --- Scroll-progress rail --- */
  function wireRail() {
    var fill = document.querySelector('.scroll-rail-fill');
    if (!fill || reducedMotion || window.innerWidth <= 900) return;
    var ticking = false;
    function update() {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
      fill.style.transform = 'scaleY(' + p.toFixed(4) + ')';
      ticking = false;
    }
    function onScroll() {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  /* --- § copy-link anchors --- */
  function slugify(text) {
    return String(text)
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .trim()
      .replace(/\s+/g, '-')
      .slice(0, 60);
  }

  function wireAnchors() {
    // Arch pages: target section-heads. Skip doc-title (h1).
    var headings = document.querySelectorAll('h2.section-head, h2:not(.section-head), h3');
    headings.forEach(function (h) {
      // Skip headings inside interactive tooltip widgets or nav
      if (h.closest('.masthead') || h.closest('.pull') || h.closest('.callout')) return;
      if (!h.id) {
        var slug = slugify(h.textContent || '');
        if (!slug) return;
        var base = slug, i = 2;
        while (document.getElementById(slug)) { slug = base + '-' + (i++); }
        h.id = slug;
      }
      h.classList.add('has-anchor');
      var a = document.createElement('a');
      a.className = 'heading-anchor';
      a.href = '#' + h.id;
      a.textContent = '\u00A7';
      a.setAttribute('aria-label', 'Copy link to: ' + (h.textContent || '').trim());
      a.addEventListener('click', function (e) {
        e.preventDefault();
        var url = window.location.origin + window.location.pathname + '#' + h.id;
        history.replaceState(null, '', '#' + h.id);
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(
            function () { showToast('Link copied'); },
            function () { showToast('Copy failed'); }
          );
        } else {
          var ta = document.createElement('textarea');
          ta.value = url;
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); showToast('Link copied'); }
          catch (err) { showToast('Copy failed'); }
          document.body.removeChild(ta);
        }
      });
      h.appendChild(a);
    });

    // Hash-scroll after anchors wired
    if (window.location.hash) {
      var target = document.getElementById(window.location.hash.slice(1));
      if (target) {
        setTimeout(function () {
          target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
        }, 50);
      }
    }
  }

  function init() {
    ensureDom();
    wireRail();
    wireAnchors();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
