(function() {

// This list is hand-maintained and must match builder/slide-registry.json's order
// exactly. getElementById silently drops any id that doesn't exist on the page, so a
// stale/missing id here doesn't error — it just shortens `views`, which makes PgDn
// jump past slides early (this broke on 2026-09-29 when slides were added/renumbered
// without updating this file). Update both files together.
const views = [
    document.getElementById('title'),
    document.getElementById('slide-cibc-requirements-wrapper'),
    document.getElementById('slide-integration-parts-wrapper'),
    document.getElementById('slide-shared-abstractions-wrapper'),
    document.getElementById('slide-01-posture-wrapper'),
    document.getElementById('slide-02-lifecycle-wrapper'),
    document.getElementById('slide-03-control-types-wrapper'),
    document.getElementById('slide-04-control-sources-wrapper'),
    document.getElementById('slide-05-controls-as-software-wrapper'),
    document.getElementById('slide-06-trace-outcomes-wrapper'),
    document.getElementById('slide-07-three-environments-wrapper'),
    document.getElementById('slide-07b-compliance-wrapper'),
    document.getElementById('slide-08-drift-wrapper'),
    document.getElementById('slide-09-ai-gateway-wrapper'),
    document.getElementById('slide-10-tokenomics-wrapper'),
    document.getElementById('thankyou'),
  ].filter(Boolean);

  function viewTop(el) {
    return el.getBoundingClientRect().top + (window.scrollY || window.pageYOffset);
  }

  function currentViewIndex() {
    var scrollY = window.scrollY || window.pageYOffset;
    var best = 0;
    for (var i = 0; i < views.length; i++) {
      if (viewTop(views[i]) <= scrollY + 10) best = i;
    }
    return best;
  }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === 'PageDown') {
      e.preventDefault();
      var idx = currentViewIndex();
      if (idx < views.length - 1) {
        window.scrollTo({ top: viewTop(views[idx + 1]), behavior: 'smooth' });
      }
    }
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp') {
      e.preventDefault();
      var idx = currentViewIndex();
      var scrollY = window.scrollY || window.pageYOffset;
      // If we're partway into the current view, go to its top first
      if (scrollY > viewTop(views[idx]) + 10 && idx >= 0) {
        window.scrollTo({ top: viewTop(views[idx]), behavior: 'smooth' });
      } else if (idx > 0) {
        window.scrollTo({ top: viewTop(views[idx - 1]), behavior: 'smooth' });
      }
    }
  });
})();
