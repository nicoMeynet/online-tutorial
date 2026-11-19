/* Progression enregistrée dans ce navigateur (localStorage), sans compte ni serveur.
   Sur un tutoriel : note la visite et le meilleur score du quiz (ol.quiz ou #quiz, feedback .fb.ok / .fb.no).
   Sur l'accueil : affiche un badge sur chaque carte et un résumé. */
(function () {
  var KEY = 'tutoriels-progression-v1';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) {} }
  var page = (location.pathname.split('/').pop() || 'index.html');
  if (page === '') page = 'index.html';

  function toast(msg) {
    var t = document.createElement('div');
    t.textContent = msg;
    t.setAttribute('role', 'status');
    t.style.cssText = 'position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:50;background:#1f2a5c;color:#fff;' +
      'font:700 15px/1.3 system-ui,sans-serif;padding:10px 16px;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,.25);max-width:90vw;text-align:center';
    document.body.appendChild(t);
    setTimeout(function () { t.style.transition = 'opacity .4s'; t.style.opacity = '0'; }, 2600);
    setTimeout(function () { t.remove(); }, 3100);
  }

  function trackTutorial() {
    var d = load(), p = d[page] || {};
    p.seen = Date.now();
    d[page] = p; save(d);
    var quiz = document.querySelector('ol.quiz') || document.querySelector('.quiz#quiz');
    if (!quiz) return;
    var reported = '';
    function check() {
      var items = quiz.children.length;
      if (!items) return;
      var ok = quiz.querySelectorAll('.fb.ok').length, no = quiz.querySelectorAll('.fb.no').length;
      if (ok + no < items) { reported = ''; return; }
      var sig = ok + '/' + items;
      if (sig === reported) return;
      reported = sig;
      var d2 = load(), q = d2[page] || {};
      var best = q.best != null && q.total === items ? q.best : -1;
      q.last = ok; q.total = items; q.seen = Date.now();
      if (ok > best) q.best = ok;
      d2[page] = q; save(d2);
      toast('Quiz : ' + ok + ' / ' + items + (ok > best && best >= 0 ? ' — nouveau record !' : '') + ' (enregistré)');
    }
    new MutationObserver(function () { clearTimeout(check.t); check.t = setTimeout(check, 150); })
      .observe(quiz, { subtree: true, childList: true, attributes: true, attributeFilter: ['class'] });
  }

  function showOnLanding() {
    var d = load();
    var cards = document.querySelectorAll('a.card');
    var seen = 0, mastered = 0;
    cards.forEach(function (c) {
      var p = d[c.getAttribute('href')];
      var old = c.querySelector('.prog'); if (old) old.remove();
      if (!p) return;
      seen++;
      var b = document.createElement('span');
      b.className = 'prog';
      if (p.total) {
        var full = p.best === p.total;
        var good = p.best / p.total >= 0.75;
        if (good) mastered++;
        b.textContent = (full ? '★ ' : good ? '✓ ' : '') + 'Quiz ' + p.best + '/' + p.total;
        if (full) b.classList.add('full');
      } else {
        b.textContent = '✓ Lu';
      }
      c.appendChild(b);
    });
    ['revisions-brevet.html', 'revisions-brevet-physique.html'].forEach(function (f) {
      var bre = d[f], link = document.querySelector('.extras a[href="' + f + '"] .d');
      if (link) link.textContent = bre && bre.total ? 'Ton meilleur score : ' + bre.best + ' / ' + bre.total + '. Retente ta chance !' : 'Des questions de tous les thèmes, avec ton score.';
    });
    var box = document.getElementById('progress');
    if (!box) return;
    if (!seen) { box.hidden = true; return; }
    box.hidden = false;
    box.querySelector('[data-seen]').textContent = seen + ' / ' + cards.length;
    box.querySelector('[data-mastered]').textContent = mastered;
    box.querySelector('.bar i').style.width = Math.round(100 * seen / cards.length) + '%';
  }

  var LANDING = page === 'index.html' || page === 'physique.html' || page === 'numerique.html';
  window.__progress = { load: load, key: KEY, refresh: function () { if (LANDING) showOnLanding(); } };

  function start() {
    if (LANDING) {
      showOnLanding();
      var r = document.getElementById('progressReset');
      if (r) r.addEventListener('click', function () {
        if (confirm('Effacer ta progression sur cet appareil ?')) { try { localStorage.removeItem(KEY); } catch (e) {} showOnLanding(); }
      });
      window.addEventListener('pageshow', showOnLanding);
    } else if (document.querySelector('main.page')) {
      trackTutorial();
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
