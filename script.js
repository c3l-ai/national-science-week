/* Future Minds - map and card linking */
(function () {
  'use strict';

  var pins = Array.prototype.slice.call(document.querySelectorAll('.pin'));
  var stops = Array.prototype.slice.call(document.querySelectorAll('.stop'));

  function setActive(key, on) {
    pins.forEach(function (p) {
      if (p.dataset.stop === key) p.classList.toggle('is-active', on);
    });
    stops.forEach(function (s) {
      if (s.dataset.stop === key) s.classList.toggle('is-active', on);
    });
  }

  pins.forEach(function (pin) {
    var key = pin.dataset.stop;
    pin.setAttribute('tabindex', '0');
    pin.setAttribute('role', 'link');

    pin.addEventListener('mouseenter', function () { setActive(key, true); });
    pin.addEventListener('mouseleave', function () { setActive(key, false); });
    pin.addEventListener('focus', function () { setActive(key, true); });
    pin.addEventListener('blur', function () { setActive(key, false); });

    function go() {
      var card = document.getElementById('stop-' + key);
      if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    pin.addEventListener('click', go);
    pin.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); }
    });
  });

  stops.forEach(function (stop) {
    var key = stop.dataset.stop;
    stop.addEventListener('mouseenter', function () { setActive(key, true); });
    stop.addEventListener('mouseleave', function () { setActive(key, false); });
  });

  /* Reveal sections on scroll, once. */
  var motionOK = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (motionOK && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -6% 0px' });

    document.querySelectorAll('.questions .wrap, .tour .wrap, .pcard, .vcard')
      .forEach(function (el) { el.classList.add('will-rise'); io.observe(el); });
  }
})();
