(function () {
  var b = document.querySelector('.burger'), n = document.querySelector('nav.main');
  if (b && n) {
    b.addEventListener('click', function () {
      var open = n.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  // mobile submenu toggles
  document.querySelectorAll('nav.main > ul > li').forEach(function (li) {
    var a = li.querySelector(':scope > a'), sub = li.querySelector(':scope > .sub');
    if (!sub || !a) return;
    a.addEventListener('click', function (e) {
      if (window.matchMedia('(max-width:1100px)').matches) {
        e.preventDefault();
        li.classList.toggle('open');
      }
    });
  });
  // scroll reveal
  var els = document.querySelectorAll('.rv');
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion:reduce)').matches) {
    els.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
  els.forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + 'ms'; io.observe(el); });
})();
