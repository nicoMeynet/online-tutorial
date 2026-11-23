"""Génère index.html, la page d'accueil générale (intro + choix de la matière + recherche globale).

Elle lit les quatre accueils de matière (cartes, catégories, mots-clés de recherche) : relancer
après tout ajout de tutoriel, après difficulte/parcours et avant liens.py :
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
    ("physique.html", "physique", "Physique-chimie", "#0e7490", "#67e8f9",
     "La matière, le mouvement, les forces, l'énergie, l'électricité, la lumière et le son, en simulations."),
    ("numerique.html", "numerique", "Numérique", "#b91c1c", "#fca5a5",
     "Arnaques, manipulation, vie privée, IA, réseaux sociaux, et comment marchent Internet et les ordinateurs."),
    ("religions.html", "religions", "Religions", "#6d28d9", "#c4b5fd",
     "Les religions et les sagesses du monde : croyances, textes, fêtes et lieux, pour mieux comprendre les autres."),
]

ICONS = {
    "maths": '<text x="32" y="49" text-anchor="middle" font-family="Bricolage Grotesque, Segoe UI, sans-serif" font-weight="800" font-size="50" fill="currentColor">π</text>',
    "physique": '<g fill="none" stroke="currentColor" stroke-width="3"><ellipse cx="32" cy="32" rx="25" ry="10"/><ellipse cx="32" cy="32" rx="25" ry="10" transform="rotate(60 32 32)"/><ellipse cx="32" cy="32" rx="25" ry="10" transform="rotate(-60 32 32)"/></g><circle cx="32" cy="32" r="4.5" fill="currentColor"/>',
    "numerique": '<g fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"><rect x="8" y="12" width="48" height="32" rx="4"/><path d="M24 54h16M32 44v10"/></g><path d="M24 23l-6 5 6 5M40 23l6 5-6 5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
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


PAGE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tutoriels interactifs</title>
<meta name="description" content="Des tutoriels interactifs en français pour le secondaire I en Suisse romande : maths, physique-chimie, numérique et religions.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=JetBrains+Mono:wght@500;600&display=swap">
<style>
/* Accueil général : même cahier à carreaux que les tutoriels, une couleur par matière. Généré par tools/accueil.py. */
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
  padding: 32px max(16px, env(safe-area-inset-right, 0px)) 64px max(16px, env(safe-area-inset-left, 0px));
}
main { max-width: 1120px; margin: 0 auto; display: flex; flex-direction: column; gap: 34px; }
h1 { margin: 0; font-family: var(--f-display); font-weight: 800; font-size: clamp(2.3rem, 6.5vw, 3.6rem); line-height: 1.05; }
h2 { margin: 0; font-family: var(--f-display); font-weight: 800; font-size: 1.55rem; line-height: 1.2; }
p { margin: 0; }
a { color: inherit; }
.soft { color: var(--soft); }
.eyebrow { font-family: var(--f-mono); font-size: .8rem; letter-spacing: .12em; text-transform: uppercase; color: var(--red); font-weight: 600; }
.sr { position: absolute; left: -9999px; }
[hidden] { display: none !important; }
.toprow { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; justify-content: space-between; }

header.hero { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 28px; align-items: center; }
.hero .txt { display: flex; flex-direction: column; gap: 14px; min-width: 0; }
.lead { font-size: 1.18rem; color: var(--soft); max-width: 60ch; }
.edu { display: flex; flex-direction: column; gap: 4px; border-left: 4px solid var(--acc); padding: 12px 16px; background: var(--card); border-radius: 0 10px 10px 0; max-width: 680px; }
.edu strong { color: var(--acc); font-family: var(--f-display); }
.edu span { color: var(--soft); }
.stats { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
.stat { background: var(--card); border: 2px solid var(--ink); border-radius: 12px; padding: 12px 14px; box-shadow: 3px 3px 0 var(--ink); min-width: 0; }
.stat b { display: block; font: 800 2rem/1.1 var(--f-display); }
.stat span { color: var(--soft); font-size: .92rem; }

/* Reprendre */
#resume { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 18px; padding: 14px 16px; background: var(--card); border: 2px dashed var(--line); border-radius: 12px; }
#resume .go { text-decoration: none; font: 800 1.05rem var(--f-display); padding: 9px 16px; border-radius: 10px; background: var(--ink); color: var(--paper); }
#resume .go:focus-visible { outline: 3px solid var(--red); outline-offset: 2px; }
#resume .bar { flex: 1 1 160px; height: 10px; border-radius: 99px; background: var(--line); overflow: hidden; min-width: 120px; }
#resume .bar i { display: block; height: 100%; width: 0; background: var(--ok); }

/* Matières */
.subjects { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); gap: 18px; }
a.subj { --c: var(--acc); display: flex; flex-direction: column; gap: 10px; min-width: 0; text-decoration: none; color: var(--ink); background: var(--card); border: 2px solid var(--ink); border-top: 8px solid var(--c); border-radius: 14px; padding: 18px 18px 16px; box-shadow: 5px 5px 0 var(--ink); transition: transform .12s, box-shadow .12s; }
a.subj:hover { transform: translate(-2px, -2px); box-shadow: 7px 7px 0 var(--ink); }
a.subj:focus-visible { outline: 3px solid var(--red); outline-offset: 3px; }
a.subj .top { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
a.subj svg { width: 56px; height: 56px; color: var(--c); flex: none; }
a.subj .n { font: 700 .85rem var(--f-mono); padding: 3px 10px; border-radius: 99px; border: 1.5px solid var(--c); color: var(--ink); white-space: nowrap; }
a.subj h3 { margin: 0; font: 800 1.55rem/1.15 var(--f-display); color: var(--c); }
a.subj p { color: var(--soft); font-size: .97rem; }
a.subj ul { margin: 0; padding: 0; list-style: none; display: flex; flex-wrap: wrap; gap: 6px; }
a.subj li { font-size: .8rem; padding: 2px 8px; border-radius: 99px; background: var(--paper); border: 1px solid var(--line); }
a.subj .me { margin-top: auto; font: 700 .85rem var(--f-mono); color: var(--soft); min-height: 1.4em; }
a.subj .cta { font: 800 1rem var(--f-display); color: var(--c); }

/* Recherche */
.search { display: flex; gap: 10px; align-items: center; }
.search input { flex: 1; min-width: 0; font: inherit; padding: 12px 14px; border: 2px solid var(--ink); border-radius: 10px; background: var(--card); color: var(--ink); }
.search input:focus-visible { outline: 3px solid var(--red); outline-offset: 2px; }
.count { font-family: var(--f-mono); font-size: .9rem; color: var(--soft); white-space: nowrap; }
.sugg { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.sugg button { font: 700 .9rem var(--f-body); padding: 6px 12px; min-height: 40px; border-radius: 999px; border: 1.5px solid var(--line); background: var(--card); color: var(--ink); cursor: pointer; }
.sugg button:hover { border-color: var(--ink); }
#results { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 260px), 1fr)); gap: 14px; }
a.res { display: flex; flex-direction: column; gap: 6px; min-width: 0; text-decoration: none; color: var(--ink); background: var(--card); border: 2px solid var(--ink); border-left: 7px solid var(--c); border-radius: 12px; padding: 12px 14px; box-shadow: 3px 3px 0 var(--ink); }
a.res:hover { transform: translate(-1px, -1px); box-shadow: 4px 4px 0 var(--ink); }
a.res:focus-visible { outline: 3px solid var(--red); outline-offset: 2px; }
a.res .m { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 2px 8px; font: 700 .75rem var(--f-mono); color: var(--c); text-transform: uppercase; letter-spacing: .06em; }
a.res .m span:last-child { color: var(--soft); text-transform: none; letter-spacing: 0; white-space: nowrap; }
a.res strong { font: 800 1.1rem/1.2 var(--f-display); }
a.res span.d { color: var(--soft); font-size: .92rem; }
a.res .st { align-self: flex-start; font: 700 .78rem var(--f-mono); padding: 2px 8px; border-radius: 99px; border: 1.5px solid var(--c); }
.more { color: var(--soft); font-style: italic; }

/* Outils */
.extras { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap: 12px; }
.extras a { display: flex; gap: 12px; align-items: center; text-decoration: none; color: var(--ink); background: var(--card); border: 2px solid var(--ink); border-radius: 12px; padding: 12px 14px; box-shadow: 3px 3px 0 var(--ink); min-width: 0; }
.extras a:hover { transform: translate(-1px, -1px); box-shadow: 4px 4px 0 var(--ink); }
.extras a:focus-visible { outline: 3px solid var(--red); outline-offset: 2px; }
.extras .ico { font-size: 1.6rem; line-height: 1; }
.extras a.star { background: var(--ink); color: var(--paper); }
.extras a.star span.d { color: var(--paper); opacity: .85; }
.extras strong { display: block; font-family: var(--f-display); font-weight: 800; }
.extras span.d { font-size: .9rem; color: var(--soft); }

/* Comment ça marche */
.how { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 14px; }
.how div { background: var(--card); border: 1.5px solid var(--line); border-radius: 12px; padding: 14px 16px; display: flex; flex-direction: column; gap: 6px; }
.how b { font: 800 1.08rem var(--f-display); }
.how span { color: var(--soft); font-size: .95rem; }
section { display: flex; flex-direction: column; gap: 14px; }

footer { padding-top: 14px; border-top: 2px solid var(--ink); color: var(--soft); font-size: .9rem; display: flex; flex-direction: column; gap: 6px; }
@media (max-width: 760px) {
  header.hero { grid-template-columns: minmax(0, 1fr); gap: 20px; }
  body { padding-top: 22px; }
}
@media (prefers-reduced-motion: reduce) { a.subj, a.res, .extras a { transition: none; } }
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
  <header class="hero">
    <div class="txt">
      <div class="toprow"><span class="eyebrow">Tutoriels interactifs · secondaire I · Suisse romande</span><button type="button" data-share hidden>Partager</button></div>
      <h1>Apprendre en manipulant</h1>
      <p class="lead">Des tutoriels gratuits en français, de la 8H à la 11H. Sur chaque page, tu bouges des curseurs, tu testes tes idées et la page t'explique ce qui se passe, étape par étape. Choisis une matière ou cherche un thème.</p>
      <div class="edu">
        <strong>Éducation 2.0</strong>
        <span>Ces pages sont générées avec l'aide d'une intelligence artificielle, puis vérifiées. Si quelque chose te paraît faux, parles-en à ton enseignant ou à un adulte : c'est aussi une bonne façon d'apprendre.</span>
      </div>
    </div>
    <div class="stats" aria-label="En chiffres">
      <div class="stat"><b>__TOTAL__</b><span>tutoriels interactifs</span></div>
      <div class="stat"><b>4</b><span>matières</span></div>
      <div class="stat"><b>8</b><span>questions de quiz par tutoriel</span></div>
      <div class="stat"><b>Gratuit</b><span>sans compte ni publicité</span></div>
    </div>
  </header>

  <div id="resume" hidden aria-live="polite">
    <span><strong>Bon retour !</strong> <span class="soft" data-sum></span></span>
    <span class="bar" aria-hidden="true"><i></i></span>
    <a class="go" href="#" data-last>Reprendre</a>
  </div>

  <section aria-labelledby="h-subj">
    <h2 id="h-subj">Choisis une matière</h2>
    <div class="subjects">
__SUBJECTS__
    </div>
  </section>

  <section aria-labelledby="h-search">
    <h2 id="h-search">Tu cherches un thème précis ?</h2>
    <div class="search">
      <label for="q" class="sr">Chercher dans tous les tutoriels</label>
      <input id="q" type="search" placeholder="Chercher : fraction, vitesse, arnaque, Diwali…" autocomplete="off">
      <span class="count" id="count"></span>
    </div>
    <div class="sugg" aria-label="Idées de recherche"><span class="soft">Par exemple :</span>
      <button type="button">pourcentage</button><button type="button">énergie</button><button type="button">mot de passe</button><button type="button">IA</button><button type="button">fêtes</button><button type="button">conversion</button>
    </div>
    <div id="results" aria-live="polite"></div>
    <p class="more" id="more" hidden></p>
  </section>

  <section aria-labelledby="h-tools">
    <h2 id="h-tools">Pour t'organiser</h2>
    <nav class="extras" aria-label="Outils">
      <a href="parcours.html" class="star"><span class="ico" aria-hidden="true">🧭</span><span><strong>Mon parcours</strong><span class="d">Quoi faire ensuite, dans chaque matière, selon ce que tu as déjà réussi.</span></span></a>
      <a href="fiches.html"><span class="ico" aria-hidden="true">🖨</span><span><strong>Fiches à imprimer</strong><span class="d">L'essentiel de chaque tutoriel, à relire avant un test.</span></span></a>
      <a href="revisions-brevet.html"><span class="ico" aria-hidden="true">🎯</span><span><strong>Quiz de révision : maths</strong><span class="d">Des questions de tous les thèmes de maths, avec ton score.</span></span></a>
      <a href="revisions-brevet-physique.html"><span class="ico" aria-hidden="true">🎯</span><span><strong>Quiz de révision : physique</strong><span class="d">Des questions de toute la physique-chimie, avec ton score.</span></span></a>
      <a href="glossaire.html"><span class="ico" aria-hidden="true">📖</span><span><strong>Glossaire de maths</strong><span class="d">Tous les mots de maths expliqués simplement.</span></span></a>
      <a href="glossaire-physique.html"><span class="ico" aria-hidden="true">📖</span><span><strong>Glossaire de physique</strong><span class="d">Les mots de physique-chimie expliqués simplement.</span></span></a>
    </nav>
  </section>

  <section aria-labelledby="h-how">
    <h2 id="h-how">Comment ça marche ?</h2>
    <div class="how">
      <div><b>1. Tu manipules</b><span>Chaque tutoriel avance par étapes courtes, avec des curseurs, des schémas à cliquer et des petits jeux.</span></div>
      <div><b>2. Tu t'entraînes</b><span>Un quiz de 8 questions, des exercices corrigés et une fiche « À retenir » à la fin de chaque page.</span></div>
      <div><b>3. Tu suis tes progrès</b><span>Tes scores sont gardés seulement dans ce navigateur. Rien n'est envoyé, aucun compte, aucune publicité.</span></div>
    </div>
  </section>

  <footer>
    <span>Tutoriels interactifs pour le secondaire I (HarmoS 8H–11H), en français, pour la Suisse romande.</span>
    <span>Besoin de parler à quelqu'un ? Pro Juventute répond au 147, jour et nuit, gratuitement.</span>
  </footer>
</main>
<script>
(function () {
  /* Données générées par tools/accueil.py : une entrée par tutoriel.
     h = page, t = titre, d = description, y = symbole, l = niveau, f = difficulté, c = catégorie, k = mots-clés, s = matière. */
  var SUBJ = __SUBJ_JSON__;
  var DATA = __DATA_JSON__;
  var KEY = 'tutoriels-progression-v1';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; } }
  function norm(s) { return String(s).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, ''); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var bySubj = {};
  SUBJ.forEach(function (s) { bySubj[s.id] = s; });
  DATA.forEach(function (x) { x.n = ' ' + norm([x.t, x.d, x.c, x.k, bySubj[x.s].name].join(' ')).replace(/[^a-z0-9²³]+/g, ' '); });

  function status(p) {
    if (!p) return '';
    if (p.total) return (p.best === p.total ? '★ ' : p.best / p.total >= 0.75 ? '✓ ' : '') + 'Quiz ' + p.best + '/' + p.total;
    return '✓ Lu';
  }

  /* Progression par matière et dernier tutoriel ouvert */
  function progress() {
    var d = load(), seen = 0, last = null;
    SUBJ.forEach(function (s) { s.seen = 0; s.good = 0; });
    DATA.forEach(function (x) {
      var p = d[x.h];
      if (!p) return;
      seen++;
      var s = bySubj[x.s];
      s.seen++;
      if (p.total && p.best / p.total >= 0.75) s.good++;
      if (p.seen && (!last || p.seen > last.when)) last = { x: x, when: p.seen };
    });
    SUBJ.forEach(function (s) {
      var el = document.querySelector('[data-me="' + s.id + '"]');
      if (el) el.textContent = s.seen ? s.seen + ' / ' + s.count + ' ouverts · ' + s.good + ' quiz réussis' : '';
    });
    var box = document.getElementById('resume');
    if (!seen) { box.hidden = true; return { seen: 0, last: null }; }
    box.hidden = false;
    box.querySelector('[data-sum]').textContent = 'Tu as ouvert ' + seen + ' tutoriel' + (seen > 1 ? 's' : '') + ' sur ' + DATA.length + '.';
    box.querySelector('.bar i').style.width = Math.round(100 * seen / DATA.length) + '%';
    var a = box.querySelector('[data-last]');
    a.href = last.x.h;
    a.textContent = 'Reprendre : ' + last.x.t + ' →';
    return { seen: seen, last: last };
  }

  /* Recherche dans les quatre matières */
  var q = document.getElementById('q'), out = document.getElementById('results'), more = document.getElementById('more'), count = document.getElementById('count');
  var MAX = 12;
  function search() {
    var words = norm(q.value).split(/\\s+/).map(function (w) { return w.replace(/[^a-z0-9²³]+/g, ''); }).filter(Boolean);
    if (!words.length) { out.innerHTML = ''; more.hidden = true; count.textContent = DATA.length + ' tutoriels'; return []; }
    var hits = DATA.filter(function (x) { return words.every(function (w) { return x.n.indexOf(' ' + w) >= 0; }); });
    var d = load();
    out.innerHTML = hits.slice(0, MAX).map(function (x) {
      var s = bySubj[x.s], st = status(d[x.h]);
      return '<a class="res" href="' + x.h + '" style="--c:var(--s-' + s.id + ')"><span class="m"><span>' + esc(s.name) + '</span><span>' + esc(x.l) + (x.f ? ' · ' + esc(x.f) : '') + '</span></span>' +
        '<strong>' + esc(x.t) + '</strong><span class="d">' + esc(x.d) + '</span>' + (st ? '<span class="st">' + esc(st) + '</span>' : '') + '</a>';
    }).join('');
    count.textContent = hits.length + (hits.length > 1 ? ' résultats' : ' résultat');
    more.hidden = hits.length > 0 && hits.length <= MAX;
    more.textContent = hits.length ? 'Et ' + (hits.length - MAX) + ' autres : précise ta recherche, ou ouvre une matière.' : 'Aucun tutoriel ne correspond. Essaie un autre mot, ou ouvre une matière.';
    return hits;
  }
  q.addEventListener('input', search);
  document.querySelectorAll('.sugg button').forEach(function (b) {
    b.addEventListener('click', function () { q.value = b.textContent; search(); q.focus(); });
  });

  function refresh() { progress(); search(); }
  window.__accueil = { data: DATA, subjects: SUBJ, search: function (t) { q.value = t; return search(); }, progress: progress };
  refresh();
  window.addEventListener('pageshow', refresh);
})();
</script>
</body>
</html>
"""


def main():
    subj_json, data, blocks, light, dark = [], [], [], [], []
    for fname, sid, name, col, dcol, desc in SUBJECTS:
        cats, cards = read_landing(fname)
        for c in cards:
            c["s"] = sid
        data += cards
        subj_json.append({"id": sid, "name": name, "href": fname, "count": len(cards)})
        light.append(f"  --s-{sid}: {col};")
        dark.append(f"    --s-{sid}: {dcol};")
        chips = "".join(f"<li>{html.escape(n)}</li>" for _, n in cats)
        blocks.append(
            f'      <a class="subj" href="{fname}" style="--c:var(--s-{sid})">'
            f'<span class="top"><svg viewBox="0 0 64 64" aria-hidden="true">{ICONS[sid]}</svg><span class="n">{len(cards)} tutoriels</span></span>'
            f'<h3>{html.escape(name)}</h3><p>{html.escape(desc)}</p><ul aria-label="Thèmes">{chips}</ul>'
            f'<span class="me" data-me="{sid}"></span><span class="cta">Ouvrir →</span></a>')
    page = (PAGE.replace("__LIGHT__", "\n".join(light))
            .replace("__DARK__", "\n".join(dark))
            .replace("__SUBJECTS__", "\n".join(blocks))
            .replace("__TOTAL__", str(len(data)))
            .replace("__SUBJ_JSON__", json.dumps(subj_json, ensure_ascii=False))
            .replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")))
    (ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print("index.html :", len(data), "tutoriels")


if __name__ == "__main__":
    main()
