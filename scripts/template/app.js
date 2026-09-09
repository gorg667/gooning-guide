(function () {
  // ---------- Age gate ----------
  var gate = document.getElementById('agegate');
  if (gate) {
    if (!localStorage.getItem('age_ok')) gate.hidden = false;
    var yes = document.getElementById('age-yes');
    if (yes) yes.addEventListener('click', function () {
      localStorage.setItem('age_ok', '1');
      gate.hidden = true;
    });
  }

  // ---------- Theme ----------
  var root = document.documentElement;
  var saved = localStorage.getItem('theme');
  if (saved) root.setAttribute('data-theme', saved);
  var tb = document.getElementById('theme-btn');
  if (tb) tb.addEventListener('click', function () {
    var t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', t);
    localStorage.setItem('theme', t);
  });

  // ---------- Mobile menu ----------
  var mb = document.getElementById('menu-btn');
  var sb = document.getElementById('sidebar');
  if (mb && sb) {
    mb.addEventListener('click', function () { sb.classList.toggle('open'); });
    document.addEventListener('click', function (e) {
      if (sb.classList.contains('open') && !sb.contains(e.target) && e.target !== mb) sb.classList.remove('open');
    });
  }

  // ---------- Scroll active nav in sidebar into view ----------
  var act = document.querySelector('.chapters li.active');
  if (act && sb) act.scrollIntoView({ block: 'center' });

  // ---------- Back to top ----------
  var tt = document.getElementById('totop');
  if (tt) {
    window.addEventListener('scroll', function () {
      tt.classList.toggle('show', window.scrollY > 600);
    }, { passive: true });
    tt.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  // ---------- TOC highlight ----------
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc-side a'));
  if (tocLinks.length) {
    var heads = tocLinks.map(function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      return document.getElementById(id);
    }).filter(Boolean);
    var onScroll = function () {
      var y = window.scrollY + 90, cur = null;
      for (var i = 0; i < heads.length; i++) { if (heads[i].offsetTop <= y) cur = heads[i]; }
      tocLinks.forEach(function (a) {
        a.classList.toggle('active', cur && decodeURIComponent(a.getAttribute('href').slice(1)) === cur.id);
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ---------- Search ----------
  var inp = document.getElementById('search');
  var box = document.getElementById('search-results');
  var idx = null;
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function hl(text, terms) {
    var out = esc(text);
    terms.forEach(function (t) {
      if (!t) return;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  }
  function snippet(text, terms) {
    var low = text.toLowerCase(), pos = -1;
    for (var i = 0; i < terms.length; i++) { pos = low.indexOf(terms[i]); if (pos >= 0) break; }
    if (pos < 0) pos = 0;
    var start = Math.max(0, pos - 80), end = Math.min(text.length, pos + 160);
    return (start > 0 ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }
  function run(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(function (t) { return t.length > 1; });
    if (!terms.length) { box.hidden = true; return; }
    var scored = [];
    idx.forEach(function (e) {
      var t = e.t.toLowerCase(), x = e.x.toLowerCase(), c = e.c.toLowerCase(), s = 0;
      terms.forEach(function (term) {
        if (t.indexOf(term) >= 0) s += 6;
        if (c.indexOf(term) >= 0) s += 3;
        var n = x.split(term).length - 1; s += Math.min(n, 5);
      });
      if (s > 0) scored.push([s, e]);
    });
    scored.sort(function (a, b) { return b[0] - a[0]; });
    var top = scored.slice(0, 12);
    if (!top.length) { box.innerHTML = '<div class="sr-empty">No results.</div>'; box.hidden = false; return; }
    box.innerHTML = top.map(function (p) {
      var e = p[1];
      return '<a class="sr" href="' + e.u + '"><div class="sr-ch">' + esc(e.c) + '</div><div class="sr-t">' + hl(e.t, terms) + '</div><div class="sr-x">' + hl(snippet(e.x, terms), terms) + '</div></a>';
    }).join('');
    box.hidden = false;
  }
  if (inp && box) {
    var load = function (cb) {
      if (idx) return cb();
      fetch('search.json').then(function (r) { return r.json(); }).then(function (j) { idx = j; cb(); }).catch(function () { idx = []; cb(); });
    };
    var timer;
    inp.addEventListener('input', function () {
      clearTimeout(timer);
      var q = inp.value.trim();
      if (!q) { box.hidden = true; return; }
      timer = setTimeout(function () { load(function () { run(q); }); }, 120);
    });
    inp.addEventListener('focus', function () { load(function () {}); });
    document.addEventListener('click', function (e) {
      if (!box.contains(e.target) && e.target !== inp) box.hidden = true;
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== inp && !/input|textarea/i.test(document.activeElement.tagName)) { e.preventDefault(); inp.focus(); }
      if (e.key === 'Escape') { box.hidden = true; inp.blur(); }
    });
  }
})();
