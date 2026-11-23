/* Bouton « Partager » : WhatsApp, SMS, e-mail, copier le lien, ou le menu de partage du téléphone.
   Le bouton est un <button data-share> ajouté par tools/liens.py (tutoriels), les accueils et tools/accueil.py.
   La page n'envoie rien elle-même : on ouvre seulement l'application choisie, avec un message prêt à envoyer.
   Le lien partagé est toujours l'adresse publique du site (jamais localhost ni un fichier local). */
(function () {
  var BASE = 'https://nicomeynet.github.io/online-tutorial/';

  function pageUrl() {
    var name = location.pathname.split('/').pop() || '';
    return BASE + (name === 'index.html' ? '' : name);
  }
  function pageTitle() {
    var h = document.querySelector('main h1');
    return ((h && h.textContent) || document.title || 'Tutoriels interactifs').replace(/\s+/g, ' ').trim();
  }
  function message() {
    var name = location.pathname.split('/').pop() || 'index.html';
    var landing = /^(index|maths|physique|numerique|religions)\.html$/.test(name);
    return landing ? 'Regarde ces tutoriels interactifs gratuits : ' + pageTitle()
                   : 'Regarde ce tutoriel interactif : « ' + pageTitle() + ' »';
  }

  var CSS = '' +
    '.tshare{display:inline-flex;align-items:center;gap:6px;min-height:40px;padding:6px 14px;border:2px solid var(--ink,#222);border-radius:999px;' +
    'background:var(--card,#fff);color:var(--ink,#222);font:700 .95rem/1.2 inherit;font-family:inherit;cursor:pointer;box-shadow:2px 2px 0 var(--ink,#222)}' +
    '.tshare:hover,.tshare:focus-visible{transform:translate(-1px,-1px);box-shadow:3px 3px 0 var(--ink,#222)}' +
    '.tshare:focus-visible{outline:3px solid var(--red,#cf3a52);outline-offset:2px}' +
    '.tshare svg{width:18px;height:18px;flex:none}' +
    '.tshare-back{position:fixed;inset:0;z-index:60;background:rgba(10,12,20,.45);display:flex;align-items:center;justify-content:center;padding:16px}' +
    '.tshare-box{width:min(100%,380px);background:var(--card,#fff);color:var(--ink,#222);border:2px solid var(--ink,#222);border-radius:14px;' +
    'box-shadow:5px 5px 0 var(--ink,#222);padding:16px;display:flex;flex-direction:column;gap:10px;font-family:inherit}' +
    '.tshare-box h2{margin:0;font-size:1.2rem;line-height:1.2}' +
    '.tshare-box p{margin:0;font-size:.9rem;opacity:.8;overflow-wrap:anywhere}' +
    '.tshare-box .opts{display:grid;grid-template-columns:1fr 1fr;gap:8px}' +
    '.tshare-box a,.tshare-box button{display:flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:8px 10px;border:2px solid var(--ink,#222);' +
    'border-radius:10px;background:var(--paper,#f6f7fb);color:var(--ink,#222);font:700 .95rem/1.2 inherit;font-family:inherit;text-decoration:none;cursor:pointer}' +
    '.tshare-box a:focus-visible,.tshare-box button:focus-visible{outline:3px solid var(--red,#cf3a52);outline-offset:2px}' +
    '.tshare-box .native{grid-column:1/-1;background:var(--ink,#222);color:var(--paper,#fff)}' +
    '.tshare-box .close{background:none;border-color:transparent;text-decoration:underline;min-height:40px}' +
    '.tshare-box .done{font-weight:700;color:var(--ok,#15803d);min-height:1.3em;text-align:center}' +
    '@media (max-width:520px){.tshare-back{align-items:flex-end;padding:0}.tshare-box{width:100%;border-radius:16px 16px 0 0;' +
    'padding-bottom:max(16px,env(safe-area-inset-bottom,0px))}}' +
    '@media print{.tshare{display:none!important}}';

  var ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4"/></svg>';

  function copy(text, done) {
    function fallback() {
      var t = document.createElement('textarea');
      t.value = text; t.setAttribute('readonly', ''); t.style.cssText = 'position:fixed;left:-9999px;top:0';
      document.body.appendChild(t); t.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) {}
      t.remove();
      done(ok);
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
    else fallback();
  }

  var last = null;
  function close() {
    var b = document.querySelector('.tshare-back');
    if (b) b.remove();
    document.removeEventListener('keydown', onKey);
    if (last) last.focus();
  }
  function onKey(e) { if (e.key === 'Escape') close(); }

  function open(btn) {
    last = btn;
    var url = pageUrl(), msg = message(), full = msg + ' ' + url;
    var e = encodeURIComponent;
    var back = document.createElement('div');
    back.className = 'tshare-back';
    back.innerHTML =
      '<div class="tshare-box" role="dialog" aria-modal="true" aria-labelledby="tshare-h">' +
      '<h2 id="tshare-h">Partager cette page</h2><p>' + url.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</p>' +
      '<div class="opts">' +
      (navigator.share ? '<button type="button" class="native" data-act="native">' + ICON + 'Partager avec…</button>' : '') +
      '<a href="https://wa.me/?text=' + e(full) + '" target="_blank" rel="noopener">WhatsApp</a>' +
      '<a href="sms:?&amp;body=' + e(full) + '">SMS</a>' +
      '<a href="mailto:?subject=' + e(pageTitle()) + '&amp;body=' + e(full) + '">E-mail</a>' +
      '<button type="button" data-act="copy">Copier le lien</button>' +
      '</div><span class="done" aria-live="polite"></span>' +
      '<button type="button" class="close" data-act="close">Fermer</button></div>';
    document.body.appendChild(back);
    var status = back.querySelector('.done');
    back.addEventListener('click', function (ev) {
      if (ev.target === back) { close(); return; }
      var t = ev.target.closest('[data-act]');
      if (!t) return;
      var act = t.getAttribute('data-act');
      if (act === 'close') close();
      else if (act === 'copy') copy(url, function (ok) { status.textContent = ok ? 'Lien copié ! Tu peux le coller où tu veux.' : 'Copie impossible : sélectionne le lien au-dessus.'; });
      else if (act === 'native') navigator.share({ title: pageTitle(), text: msg, url: url }).then(close, function () {});
    });
    document.addEventListener('keydown', onKey);
    (back.querySelector('.opts a, .opts button') || back).focus();
  }

  function start() {
    var btns = document.querySelectorAll('button[data-share]');
    if (!btns.length) return;
    var st = document.createElement('style');
    st.id = 'tshare-css'; st.textContent = CSS;
    document.head.appendChild(st);
    btns.forEach(function (b) {
      b.classList.add('tshare');
      if (!b.querySelector('svg')) b.innerHTML = ICON + '<span>Partager</span>';
      b.hidden = false;
      b.addEventListener('click', function () { open(b); });
    });
  }
  window.__share = { url: pageUrl, message: message, open: function () { open(document.querySelector('button[data-share]')); }, close: close };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
