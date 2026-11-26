"""Génère index.html (accueil : seulement les matières) et a-propos.html (le site, comment ça marche,
outils, recherche dans tous les tutoriels, progression).

Lit les accueils de matière (cartes, catégories, mots-clés de recherche) : relancer après tout ajout
de tutoriel, après difficulte/parcours et avant liens.py :
    python tools/accueil.py
La progression affichée vient du même localStorage que progress.js ; rien n'est envoyé.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SUBJECTS = [
    ("maths.html", "maths", "Maths", "#2346b5", "#8fb0ff",
     "Nombres, algèbre, géométrie, proportions, statistiques… et des curiosités comme π ou les fractales."),
    ("francais.html", "francais", "Français", "#0f5f8a", "#7cc4ec",
     "D'où vient notre langue, la grammaire de la phrase, la conjugaison, le français de Suisse romande et l'orthographe."),
    ("physique.html", "physique", "Physique-chimie", "#0e7490", "#67e8f9",
     "La matière, le mouvement, les forces, l'énergie, l'électricité, la lumière et le son, en simulations."),
    ("numerique.html", "numerique", "Numérique", "#b91c1c", "#fca5a5",
     "Arnaques, manipulation, vie privée, IA, réseaux sociaux, et comment marchent Internet et les ordinateurs."),
    ("religions.html", "religions", "Religions", "#6d28d9", "#c4b5fd",
     "Les religions et les sagesses du monde : croyances, textes, fêtes et lieux, pour mieux comprendre les autres."),
    ("geographie.html", "geographie", "Histoire, géographie et citoyenneté", "#15803d", "#4ade80",
     "Le relief, l'histoire et les cantons de la Suisse, les pays et capitales du monde, comment fonctionne la démocratie suisse, la retraite et les impôts."),
]

ICONS = {
    "maths": '<text x="32" y="49" text-anchor="middle" font-family="Bricolage Grotesque, Segoe UI, sans-serif" font-weight="800" font-size="50" fill="currentColor">π</text>',
    "physique": '<g fill="none" stroke="currentColor" stroke-width="3"><ellipse cx="32" cy="32" rx="25" ry="10"/><ellipse cx="32" cy="32" rx="25" ry="10" transform="rotate(60 32 32)"/><ellipse cx="32" cy="32" rx="25" ry="10" transform="rotate(-60 32 32)"/></g><circle cx="32" cy="32" r="4.5" fill="currentColor"/>',
    "numerique": '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"><rect x="8" y="12" width="48" height="32" rx="4"/><path d="M24 54h16M32 44v10"/></g><path d="M24 23l-6 5 6 5M40 23l6 5-6 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    "francais": '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"><path d="M8 12h48v30H30l-12 10v-10H8z"/></g><text x="32" y="35" text-anchor="middle" font-family="Bricolage Grotesque, Segoe UI, sans-serif" font-weight="800" font-size="20" fill="currentColor">Aa</text>',
    "geographie": '<path d="M4 52 L22 22 L31 35 L40 16 L60 52 Z" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/><path d="M36 23 L40 16 L44 23" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/>',
    "religions": '<g fill="none" stroke="currentColor" stroke-width="3"><circle cx="32" cy="32" r="23"/><ellipse cx="32" cy="32" rx="10" ry="23"/><path d="M9 32h46M13 20h38M13 44h38"/></g>',
}


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def read_landing(fname):
    s = (ROOT / fname).read_text(encoding="utf-8")
    m = re.search(r"var keys = (\{.*?\});", s, re.S)
    keys = json.loads(m.group(1)) if m else {}
    cats, cards = [], []
    for sec in re.finditer(r'<section class="cat" id="([^"]+)"[^>]*>(.*?)</section>', s, re.S):
        cname = strip(re.search(r"<h2[^>]*>(.*?)</h2>", sec.group(2), re.S).group(1))
        cats.append((sec.group(1), cname))
        for c in re.finditer(r'<a class="card" href="([^"]+\.html)">(.*?)</a>', sec.group(2), re.S):
            body = c.group(2)
            g = lambda pat: (lambda x: strip(x.group(1)) if x else "")(re.search(pat, body, re.S))
            cards.append({
                "h": c.group(1), "t": g(r"<strong>(.*?)</strong>"), "d": g(r'<span class="d">(.*?)</span>'),
                "y": g(r'<span class="sym">(.*?)</span>'), "l": g(r'<span class="lvl">(.*?)</span>'),
                "f": g(r'<span class="diff[^"]*"[^>]*>(.*?)</span>'), "c": cname, "k": keys.get(c.group(1), ""),
            })
    return cats, cards


HEAD = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<meta name="description" content="Des tutoriels interactifs en français pour le secondaire I en Suisse romande : maths, français, physique-chimie, numérique, religions, histoire, géographie et citoyenneté.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=JetBrains+Mono:wght@500;600&display=swap">
<style>
/* Généré par tools/accueil.py. Même cahier à carreaux que les tutoriels, une couleur par matière. */
:root {
  --paper: #f6f7fb; --grid: #e2e6f0; --card: #ffffff; --ink: #1d2233; --soft: #545b72; --line: #d6dae6;
  --red: #cf3a52; --acc: #2346b5; --ok: #15803d;
__LIGHT__
  --f-display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --f-body: "Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #10131c; --grid: #1a1f2c; --card: #171b27; --ink: #eceff7; --soft: #a9b0c6; --line: #2b3142; --red: #ff7d92; --acc: #8fb0ff; --ok: #4ade80;
__DARK__
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --paper: #10131c; --grid: #1a1f2c; --card: #171b27; --ink: #eceff7; --soft: #a9b0c6; --line: #2b3142; --red: #ff7d92; --acc: #8fb0ff; --ok: #4ade80;
__DARK__
  color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  margin: 0; background-color: var(--paper);
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 24px 24px; color: var(--ink); font: 17px/1.6 var(--f-body);
  padding: 22px max(16px, env(safe-area-inset-right, 0px)) 48px max(16px, env(safe-area-inset-left, 0px));
}
main { max-width: 1080px; margin: 0 auto; display: flex; flex-direction: column; gap: 26px; }
h1 { margin: 0; font-family: var(--f-display); font-weight: 800; font-size: clamp(1.9rem, 6vw, 3.2rem); line-height: 1.05; }
h2 { margin: 0; font-family: var(--f-display); font-weight: 800; font-size: 1.4rem; line-height: 1.2; }
p { margin: 0; }
a { color: inherit; }
.soft { color: var(--soft); }
.sr { position: absolute; left: -9999px; }
[hidden] { display: none !important; }
.top { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.pill { display: inline-flex; align-items: center; gap: 6px; min-height: 40px; padding: 6px 14px; border: 2px solid var(--ink); border-radius: 999px;
  background: var(--card); color: var(--ink); font: 700 .95rem var(--f-body); text-decoration: none; box-shadow: 2px 2px 0 var(--ink); }
.pill:hover, .pill:focus-visible { transform: translate(-1px, -1px); box-shadow: 3px 3px 0 var(--ink); }
.pill:focus-visible, a:focus-visible, button:focus-visible { outline: 3px solid var(--red); outline-offset: 2px; }
.tools-top { display: flex; gap: 8px; align-items: center; }
header.intro { display: flex; flex-direction: column; gap: 8px; }
.lead { font-size: 1.1rem; color: var(--soft); max-width: 60ch; }
footer { padding-top: 12px; border-top: 2px solid var(--ink); color: var(--soft); font-size: .9rem; display: flex; flex-direction: column; gap: 4px; }
footer a { font-weight: 700; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
__CSS__
</style>
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-title" content="Tutoriels">
<meta name="theme-color" content="#1f2a5c">
<script src="share.js" defer></script>
</head>
<body>
<main>
"""

INDEX_CSS = """
/* Matières : grandes cartes sur ordinateur, lignes compactes sur téléphone */
.subjects { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 16px; }
a.subj { --c: var(--acc); display: grid; grid-template-columns: 56px minmax(0, 1fr); grid-template-rows: auto auto; column-gap: 14px; row-gap: 4px; align-items: center;
  min-width: 0; text-decoration: none; color: var(--ink); background: var(--card); border: 2px solid var(--ink); border-left: 8px solid var(--c);
  border-radius: 14px; padding: 16px 18px; box-shadow: 4px 4px 0 var(--ink); transition: transform .12s, box-shadow .12s; }
a.subj:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0 var(--ink); }
a.subj svg { grid-row: 1 / span 2; width: 56px; height: 56px; color: var(--c); }
a.subj h2 { color: var(--c); font-size: 1.35rem; }
a.subj .n { font: 700 .8rem var(--f-mono); color: var(--soft); margin-left: 6px; white-space: nowrap; }
a.subj p { color: var(--soft); font-size: .95rem; line-height: 1.45; }
/* Progression (localStorage) : une fine barre en bas de chaque matière + « Reprendre » */
a.subj { position: relative; }
a.subj .bar { grid-column: 2 / -1; grid-row: 3; display: block; height: 10px; margin-top: 4px; border-radius: 99px; overflow: hidden;
  background: color-mix(in srgb, var(--c) 16%, var(--card)); box-shadow: inset 0 0 0 1.5px color-mix(in srgb, var(--c) 55%, transparent); }
a.subj .bar i { display: block; height: 100%; width: 0; min-width: 10px; border-radius: 99px; background: var(--c); }
a.subj .n.on { color: var(--c); font-size: .85rem; }
a.subj svg { grid-row: 1 / span 3; }
.resume { display: flex; align-items: center; gap: 6px 12px; flex-wrap: wrap; }
.resume a.pill { max-width: 100%; min-width: 0; }
.resume a.pill span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.resume .soft { font-size: .9rem; }
@media (max-width: 600px) {
  main { gap: 18px; }
  .lead { font-size: 1rem; }
  .subjects { gap: 10px; }
  a.subj { grid-template-columns: 40px minmax(0, 1fr) auto; grid-template-rows: auto; padding: 10px 14px; box-shadow: 3px 3px 0 var(--ink); border-radius: 12px; }
  a.subj svg { grid-row: 1 / span 2; width: 40px; height: 40px; }
  a.subj .bar { grid-column: 2; grid-row: 2; height: 8px; margin-top: 2px; }
  a.subj .n.on { font-size: .8rem; }
  a.subj h2 { font-size: 1.1rem; }
  a.subj p { display: none; }
  a.subj .n { margin-left: 8px; font-size: .75rem; }
  a.subj::after { content: "›"; grid-column: 3; grid-row: 1 / span 2; font: 800 1.6rem/1 var(--f-display); color: var(--soft); }
}
"""

INDEX_BODY = """  <div class="top">
    <a class="pill" href="a-propos.html">À propos</a>
    <button type="button" data-share hidden>Partager</button>
  </div>
  <header class="intro">
    <h1>Tutoriels interactifs</h1>
    <p class="lead">Choisis une matière. Sur chaque page, tu bouges, tu testes et la page t'explique, étape par étape.</p>
  </header>
  <div class="resume" id="resume" hidden>
    <a class="pill" href="#" data-last>▶ <span>Reprendre</span></a>
    <span class="soft" data-sum></span>
  </div>
  <nav class="subjects" aria-label="Matières">
__SUBJECTS__
  </nav>
  <footer>
    <span>Secondaire I (8H–11H), Suisse romande · <a href="a-propos.html">À propos du site</a></span>
  </footer>
</main>
<script>
(function () {
  /* Progression simple : lue dans ce navigateur (même clé que progress.js), rien n'est envoyé. */
  var PAGES = __PAGES_JSON__;
  var d = {};
  try { d = JSON.parse(localStorage.getItem('tutoriels-progression-v1')) || {}; } catch (e) {}
  var seen = 0, total = 0, last = null;
  Object.keys(PAGES).forEach(function (sid) {
    var list = PAGES[sid], n = 0;
    list.forEach(function (x) {
      var p = d[x[0]];
      if (!p) return;
      n++;
      if (p.seen && (!last || p.seen > last.when)) last = { h: x[0], t: x[1], when: p.seen };
    });
    seen += n; total += list.length;
    var a = document.querySelector('a.subj[data-s="' + sid + '"]');
    if (!a || !n) return;
    var c = a.querySelector('.n'); c.textContent = n + '/' + list.length; c.classList.add('on');
    a.querySelector('.bar').hidden = false;
    a.querySelector('.bar i').style.width = Math.round(100 * n / list.length) + '%';
  });
  if (last) {
    var r = document.getElementById('resume'), l = r.querySelector('[data-last]');
    l.href = last.h; l.querySelector('span').textContent = 'Reprendre : ' + last.t;
    r.querySelector('[data-sum]').textContent = seen + ' tutoriels ouverts sur ' + total;
    r.hidden = false;
  }
  window.__index = { seen: seen, total: total, last: last };
})();
</script>
</body>
</html>
"""

ABOUT_CSS = """
section { display: flex; flex-direction: column; gap: 12px; }
.how { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 12px; }
.how div { background: var(--card); border: 1.5px solid var(--line); border-radius: 12px; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px; }
.how b { font: 800 1.05rem var(--f-display); }
.how span { color: var(--soft); font-size: .95rem; }
.edu { border-left: 4px solid var(--acc); padding: 10px 14px; background: var(--card); border-radius: 0 10px 10px 0; color: var(--soft); }
.edu strong { color: var(--acc); font-family: var(--f-display); }
.extras { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap: 10px; }
.extras a { display: flex; gap: 12px; align-items: center; text-decoration: none; color: var(--ink); background: var(--card); border: 2px solid var(--ink); border-radius: 12px; padding: 10px 14px; box-shadow: 3px 3px 0 var(--ink); min-width: 0; }
.extras a:hover { transform: translate(-1px, -1px); box-shadow: 4px 4px 0 var(--ink); }
.extras .ico { font-size: 1.5rem; line-height: 1; }
.extras strong { display: block; font-family: var(--f-display); font-weight: 800; }
.extras span.d { font-size: .88rem; color: var(--soft); }
.search { display: flex; gap: 10px; align-items: center; }
.search input { flex: 1; min-width: 0; font: inherit; padding: 10px 14px; border: 2px solid var(--ink); border-radius: 10px; background: var(--card); color: var(--ink); }
.count { font-family: var(--f-mono); font-size: .85rem; color: var(--soft); white-space: nowrap; }
#results { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 10px; }
a.res { display: flex; flex-direction: column; gap: 4px; min-width: 0; text-decoration: none; color: var(--ink); background: var(--card); border: 2px solid var(--ink); border-left: 6px solid var(--c); border-radius: 12px; padding: 10px 12px; }
a.res .m { font: 700 .72rem var(--f-mono); color: var(--c); text-transform: uppercase; letter-spacing: .05em; }
a.res strong { font: 800 1.05rem/1.2 var(--f-display); }
a.res span.d { color: var(--soft); font-size: .9rem; }
.more { color: var(--soft); font-style: italic; }
#prog { background: var(--card); border: 2px dashed var(--line); border-radius: 12px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; }
#prog ul { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 6px; }
#prog li { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 4px 10px; align-items: center; font-size: .95rem; }
#prog .bar { grid-column: 1 / -1; height: 8px; border-radius: 99px; background: var(--line); overflow: hidden; }
#prog .bar i { display: block; height: 100%; width: 0; background: var(--c); }
#prog button { align-self: flex-start; font: 700 .85rem var(--f-body); background: none; border: 0; color: var(--soft); text-decoration: underline; cursor: pointer; padding: 6px 0; min-height: 40px; }
ul.plain { margin: 0; padding-left: 1.2em; display: flex; flex-direction: column; gap: 4px; }
@media (max-width: 600px) { main { gap: 20px; } h2 { font-size: 1.2rem; } }
"""

ABOUT_BODY = """  <div class="top">
    <a class="pill" href="index.html">← Accueil</a>
    <button type="button" data-share hidden>Partager</button>
  </div>
  <header class="intro">
    <h1>À propos</h1>
    <p class="lead">__TOTAL__ tutoriels interactifs gratuits, en français, pour le secondaire I (HarmoS 8H–11H) en Suisse romande, dans __NSUBJ__ matières.</p>
  </header>

  <section aria-labelledby="h-how">
    <h2 id="h-how">Comment ça marche ?</h2>
    <div class="how">
      <div><b>1. Tu manipules</b><span>Chaque tutoriel avance par étapes courtes, avec des curseurs, des schémas à cliquer et des petits jeux.</span></div>
      <div><b>2. Tu t'entraînes</b><span>Un quiz de 8 questions et des exercices corrigés à la fin de chaque page.</span></div>
      <div><b>3. Tu révises</b><span>Chaque tutoriel se termine par « À retenir », une fiche que tu peux imprimer.</span></div>
      <div><b>4. Tu suis tes progrès</b><span>Tes scores sont gardés seulement dans ce navigateur : aucun compte, rien n'est envoyé.</span></div>
    </div>
  </section>

  <section aria-labelledby="h-search">
    <h2 id="h-search">Chercher un tutoriel</h2>
    <div class="search">
      <label for="q" class="sr">Chercher dans tous les tutoriels</label>
      <input id="q" type="search" placeholder="fraction, vitesse, arnaque, canton…" autocomplete="off">
      <span class="count" id="count"></span>
    </div>
    <div id="results" aria-live="polite"></div>
    <p class="more" id="more" hidden></p>
  </section>

  <section aria-labelledby="h-tools">
    <h2 id="h-tools">Pour t'organiser</h2>
    <nav class="extras" aria-label="Outils">
      <a href="parcours.html"><span class="ico" aria-hidden="true">🧭</span><span><strong>Mon parcours</strong><span class="d">Quoi faire ensuite, selon ce que tu as déjà réussi.</span></span></a>
      <a href="revisions-brevet.html"><span class="ico" aria-hidden="true">🎯</span><span><strong>Quiz de révision : maths</strong><span class="d">Des questions de tous les thèmes de maths.</span></span></a>
      <a href="revisions-brevet-physique.html"><span class="ico" aria-hidden="true">🎯</span><span><strong>Quiz de révision : physique</strong><span class="d">Des questions de toute la physique-chimie.</span></span></a>
      <a href="glossaire.html"><span class="ico" aria-hidden="true">📖</span><span><strong>Glossaire de maths</strong><span class="d">Les mots de maths expliqués simplement.</span></span></a>
      <a href="glossaire-physique.html"><span class="ico" aria-hidden="true">📖</span><span><strong>Glossaire de physique</strong><span class="d">Les mots de physique-chimie expliqués simplement.</span></span></a>
    </nav>
  </section>

  <section aria-labelledby="h-prog">
    <h2 id="h-prog">Ta progression</h2>
    <div id="prog">
      <p class="soft" data-none>Tu n'as encore ouvert aucun tutoriel sur cet appareil.</p>
      <ul data-list hidden></ul>
      <a class="pill" href="#" data-last hidden>Reprendre</a>
      <button type="button" data-reset hidden>Effacer ma progression sur cet appareil</button>
    </div>
  </section>

  <section aria-labelledby="h-site">
    <h2 id="h-site">Le site</h2>
    <p class="edu"><strong>Éducation 2.0.</strong> Ces pages sont générées avec l'aide d'une intelligence artificielle, puis vérifiées. Si quelque chose te paraît faux, parles-en à ton enseignant ou à un adulte : c'est aussi une bonne façon d'apprendre.</p>
    <ul class="plain">
      <li>Gratuit, sans compte et sans publicité.</li>
      <li>Les pages ne demandent et n'envoient aucune information personnelle.</li>
      <li>Pour partager une page, utilise le bouton « Partager » en haut de la page.</li>
      <li>Besoin de parler à quelqu'un ? Pro Juventute répond au 147, jour et nuit, gratuitement.</li>
    </ul>
  </section>

  <footer>
    <span>Tutoriels interactifs pour le secondaire I, en français, pour la Suisse romande.</span>
  </footer>
</main>
<script>
(function () {
  /* Données générées par tools/accueil.py : h page, t titre, d description, l niveau, f difficulté, c catégorie, k mots-clés, s matière. */
  var SUBJ = __SUBJ_JSON__;
  var DATA = __DATA_JSON__;
  var KEY = 'tutoriels-progression-v1';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function norm(s) { return String(s).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var bySubj = {};
  SUBJ.forEach(function (s) { bySubj[s.id] = s; });
  DATA.forEach(function (x) { x.n = ' ' + norm([x.t, x.d, x.c, x.k, bySubj[x.s].name].join(' ')).replace(/[^a-z0-9²³]+/g, ' '); });

  var q = document.getElementById('q'), out = document.getElementById('results'), more = document.getElementById('more'), count = document.getElementById('count');
  var MAX = 12;
  function search() {
    var words = norm(q.value).split(/\\s+/).map(function (w) { return w.replace(/[^a-z0-9²³]+/g, ''); }).filter(Boolean);
    if (!words.length) { out.innerHTML = ''; more.hidden = true; count.textContent = DATA.length + ' tutoriels'; return []; }
    var hits = DATA.filter(function (x) { return words.every(function (w) { return x.n.indexOf(' ' + w) >= 0; }); });
    out.innerHTML = hits.slice(0, MAX).map(function (x) {
      var s = bySubj[x.s];
      return '<a class="res" href="' + x.h + '" style="--c:var(--s-' + s.id + ')"><span class="m">' + esc(s.name) + ' · ' + esc(x.l) + '</span>' +
        '<strong>' + esc(x.t) + '</strong><span class="d">' + esc(x.d) + '</span></a>';
    }).join('');
    count.textContent = hits.length + (hits.length > 1 ? ' résultats' : ' résultat');
    more.hidden = hits.length > 0 && hits.length <= MAX;
    more.textContent = hits.length ? 'Et ' + (hits.length - MAX) + ' autres : précise ta recherche.' : 'Aucun tutoriel ne correspond. Essaie un autre mot.';
    return hits;
  }
  q.addEventListener('input', search);

  var box = document.getElementById('prog');
  function progress() {
    var d = load(), seen = 0, last = null;
    SUBJ.forEach(function (s) { s.seen = 0; s.good = 0; });
    DATA.forEach(function (x) {
      var p = d[x.h];
      if (!p) return;
      seen++; bySubj[x.s].seen++;
      if (p.total && p.best / p.total >= 0.75) bySubj[x.s].good++;
      if (p.seen && (!last || p.seen > last.when)) last = { x: x, when: p.seen };
    });
    var list = box.querySelector('[data-list]'), a = box.querySelector('[data-last]');
    box.querySelector('[data-none]').hidden = seen > 0;
    list.hidden = a.hidden = box.querySelector('[data-reset]').hidden = !seen;
    list.innerHTML = SUBJ.map(function (s) {
      return '<li style="--c:var(--s-' + s.id + ')"><span>' + esc(s.name) + '</span><span class="soft">' + s.seen + ' / ' + s.count + ' · ' + s.good + ' quiz réussis</span>' +
        '<span class="bar" aria-hidden="true"><i style="width:' + Math.round(100 * s.seen / Math.max(1, s.count)) + '%"></i></span></li>';
    }).join('');
    if (last) { a.href = last.x.h; a.textContent = 'Reprendre : ' + last.x.t + ' →'; }
    return { seen: seen, last: last };
  }
  box.querySelector('[data-reset]').addEventListener('click', function () {
    if (confirm('Effacer ta progression sur cet appareil ?')) { try { localStorage.removeItem(KEY); } catch (e) {} progress(); }
  });

  window.__apropos = { data: DATA, subjects: SUBJ, search: function (t) { q.value = t; return search(); }, progress: progress };
  search(); progress();
  window.addEventListener('pageshow', progress);
})();
</script>
</body>
</html>
"""


def main():
    subj_json, data, blocks, light, dark = [], [], [], [], []
    for fname, sid, name, col, dcol, desc in SUBJECTS:
        cats, cards = read_landing(fname)
        lp = ROOT / fname
        lt = lp.read_text(encoding="utf-8")
        lt2 = re.sub(r'(<p class="sub">)\d+ tutoriels?( interactifs?)', lambda m: m.group(1) + str(len(cards)) + (" tutoriels interactifs" if len(cards) > 1 else " tutoriel interactif"), lt)
        if lt2 != lt:
            lp.write_text(lt2, encoding="utf-8", newline="\n")
        for c in cards:
            c["s"] = sid
        data += cards
        subj_json.append({"id": sid, "name": name, "href": fname, "count": len(cards)})
        light.append(f"  --s-{sid}: {col};")
        dark.append(f"    --s-{sid}: {dcol};")
        blocks.append(
            f'    <a class="subj" href="{fname}" data-s="{sid}" style="--c:var(--s-{sid})">'
            f'<svg viewBox="0 0 64 64" aria-hidden="true">{ICONS[sid]}</svg>'
            f'<h2>{html.escape(name)}<span class="n">{len(cards)}</span></h2><p>{html.escape(desc)}</p>'
            f'<span class="bar" hidden aria-hidden="true"><i></i></span></a>')

    def head(title, css):
        return (HEAD.replace("__TITLE__", title).replace("__CSS__", css)
                .replace("__LIGHT__", "\n".join(light)).replace("__DARK__", "\n".join(dark)))

    pages = {sid: [[c["h"], c["t"]] for c in data if c["s"] == sid] for _, sid, *_ in SUBJECTS}
    index = head("Tutoriels interactifs", INDEX_CSS) + (INDEX_BODY.replace("__SUBJECTS__", "\n".join(blocks))
             .replace("__PAGES_JSON__", json.dumps(pages, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
    (ROOT / "index.html").write_text(index, encoding="utf-8", newline="\n")
    about = head("À propos · Tutoriels interactifs", ABOUT_CSS) + (
        ABOUT_BODY.replace("__TOTAL__", str(len(data))).replace("__NSUBJ__", str(len(SUBJECTS)))
        .replace("__SUBJ_JSON__", json.dumps(subj_json, ensure_ascii=False))
        .replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
    (ROOT / "a-propos.html").write_text(about, encoding="utf-8", newline="\n")
    print("index.html + a-propos.html :", len(data), "tutoriels")


if __name__ == "__main__":
    main()
