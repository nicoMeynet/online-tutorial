"""Construit parcours.html : « Mon parcours », une formation personnalisée.

Les parcours (TRACKS) et les prérequis (PRE) sont définis ici ; les titres et
descriptions viennent des pages d'accueil. La progression est lue dans le
navigateur (progress.js, clé tutoriels-progression-v1).
    python tools/parcours.py && python tools/liens.py parcours.html
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import difficulte  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

TRACKS = [
    ("bases", "maths", "Les bases du calcul", "8H–9H", "Calculer sans se tromper, les fractions, la proportionnalité et les premières figures.", [
        "les-priorites-de-calcul", "les-nombres-relatifs", "les-fractions", "les-arrondis-et-ordres-de-grandeur",
        "la-proportionnalite", "les-conversions", "les-angles-et-triangles", "les-formes-geometriques"]),
    ("quatrieme", "maths", "Cap sur la 10H", "9H–10H", "Les lettres entrent en scène : puissances, calcul littéral, équations, Pythagore.", [
        "les-puissances", "le-calcul-litteral", "les-equations", "les-pourcentages", "la-vitesse",
        "le-reperage", "le-theoreme-de-pythagore", "les-transformations", "les-droites-remarquables",
        "les-quadrilateres", "les-statistiques"]),
    ("brevet", "maths", "Objectif 11H", "11H", "Tout le programme de 11H, jusqu'au grand quiz de révision.", [
        "les-identites-remarquables", "l-equation-produit-nul-et-les-systemes", "les-inequations", "les-fonctions",
        "les-racines-carrees", "les-nombres-premiers", "le-theoreme-de-thales", "la-trigonometrie",
        "les-echelles", "la-sphere-et-la-boule", "les-grandeurs-composees", "les-probabilites",
        "l-algorithmique", "la-demonstration", "revisions-brevet"]),
    ("lycee", "maths", "Avant-goût du secondaire II", "11H → secondaire II", "Pour les curieux qui veulent prendre de l'avance.", [
        "les-ensembles-de-nombres", "le-second-degre", "les-vecteurs", "les-suites", "la-derivee", "les-nombres-complexes"]),
    ("curiosites", "maths", "Maths et curiosités", "tous niveaux", "Les nombres célèbres, les codes secrets, les jeux et la musique.", [
        "le-nombre-pi", "le-nombre-d-or", "le-nombre-e", "les-grands-nombres-et-l-infini", "le-binaire-et-les-bases",
        "la-cryptographie", "les-paradoxes-de-probabilite", "les-fractales", "les-jeux-de-strategie", "les-maths-et-la-musique"]),
    ("physique1", "physique", "Découvrir la physique-chimie", "9H–10H", "La matière, le mouvement, l'électricité, la lumière et le son.", [
        "les-etats-de-la-matiere", "les-melanges-et-les-solutions", "les-atomes-et-les-molecules", "le-mouvement",
        "les-circuits-electriques", "la-lumiere", "le-son", "l-univers-et-le-systeme-solaire"]),
    ("physique2", "physique", "Physique-chimie : objectif 11H", "10H–11H", "Réactions, forces, énergie, électricité et signaux, jusqu'au grand quiz de révision.", [
        "les-transformations-chimiques", "les-acides-et-les-bases", "les-forces", "le-poids-et-la-masse", "la-gravitation",
        "les-formes-d-energie", "l-energie-cinetique-et-la-securite-routiere", "la-loi-d-ohm",
        "la-puissance-et-l-energie-electrique", "les-signaux-et-la-communication", "revisions-brevet-physique"]),
    ("securite", "numerique", "Se protéger en ligne", "9H–10H", "Comprendre la manipulation, repérer les arnaques, protéger ses comptes, ses appareils et sa vie privée.", [
        "comment-on-te-manipule", "reperer-les-arnaques", "les-mots-de-passe", "les-virus-et-les-mises-a-jour",
        "naviguer-en-securite", "les-donnees-personnelles", "le-cyberharcelement"]),
    ("sinformer", "numerique", "S'informer à l'ère de l'IA", "9H–11H", "Vraies et fausses infos, images truquées, réseaux sociaux et intelligence artificielle.", [
        "vraie-ou-fausse-info", "les-images-truquees-et-les-deepfakes", "les-reseaux-sociaux-et-les-algorithmes",
        "bien-utiliser-l-ia", "comment-une-ia-ecrit"]),
    ("machines", "numerique", "Comprendre les machines", "9H–10H", "Internet, les octets, les images et la programmation.", [
        "comment-marche-internet", "les-octets-et-le-stockage", "les-pixels-et-la-compression", "programmer-pas-a-pas"]),
    ("ecrans", "numerique", "Bien vivre avec les écrans", "9H", "Ton temps, ton attention et ton argent dans les jeux.", [
        "le-temps-d-ecran-et-l-attention", "les-achats-dans-les-jeux"]),
    ("religions1", "religions", "Découvrir les religions du monde", "9H–11H", "Les grandes religions et sagesses, leurs croyances, leurs textes et leurs fêtes.", [
        "les-religions-du-monde", "le-judaisme", "le-christianisme", "l-islam", "l-hindouisme", "le-bouddhisme",
        "les-sagesses-de-chine-et-du-japon", "les-mythologies-antiques", "les-fetes-et-calendriers"]),
    ("pcurio", "physique", "Physique et curiosités", "tous niveaux", "La physique du ciel, du sport et du climat.", [
        "le-ciel-bleu-et-l-arc-en-ciel", "la-physique-du-sport", "le-climat-et-l-effet-de-serre"]),
]

# Ce qu'il vaut mieux connaître avant (seulement les liens importants).
PRE = {
    "le-bouddhisme": ["l-hindouisme"],
    "les-fetes-et-calendriers": ["les-religions-du-monde"],
    "naviguer-en-securite": ["reperer-les-arnaques"],
    "les-images-truquees-et-les-deepfakes": ["vraie-ou-fausse-info"],
    "comment-une-ia-ecrit": ["bien-utiliser-l-ia"],
    "les-pixels-et-la-compression": ["les-octets-et-le-stockage"],
    "comment-marche-internet": ["les-octets-et-le-stockage"],
    "vraie-ou-fausse-info": ["comment-on-te-manipule"],
    "les-fractions": ["les-priorites-de-calcul"],
    "la-proportionnalite": ["les-fractions"],
    "les-pourcentages": ["la-proportionnalite", "les-fractions"],
    "les-conversions": ["les-arrondis-et-ordres-de-grandeur"],
    "les-puissances": ["les-priorites-de-calcul"],
    "le-calcul-litteral": ["les-priorites-de-calcul", "les-nombres-relatifs"],
    "les-equations": ["le-calcul-litteral"],
    "la-vitesse": ["la-proportionnalite"],
    "le-reperage": ["les-nombres-relatifs"],
    "le-theoreme-de-pythagore": ["les-angles-et-triangles"],
    "les-transformations": ["les-angles-et-triangles"],
    "les-droites-remarquables": ["les-angles-et-triangles"],
    "les-quadrilateres": ["les-angles-et-triangles"],
    "les-statistiques": ["les-fractions"],
    "les-identites-remarquables": ["le-calcul-litteral"],
    "l-equation-produit-nul-et-les-systemes": ["les-equations", "les-identites-remarquables"],
    "les-inequations": ["les-equations"],
    "les-fonctions": ["les-equations", "le-reperage"],
    "les-racines-carrees": ["les-puissances"],
    "le-theoreme-de-thales": ["la-proportionnalite", "les-angles-et-triangles"],
    "la-trigonometrie": ["le-theoreme-de-pythagore", "la-proportionnalite"],
    "les-echelles": ["la-proportionnalite", "les-conversions"],
    "la-sphere-et-la-boule": ["les-formes-geometriques"],
    "les-grandeurs-composees": ["la-vitesse", "les-conversions"],
    "les-probabilites": ["les-fractions"],
    "la-demonstration": ["le-calcul-litteral"],
    "revisions-brevet": ["les-fonctions", "le-theoreme-de-thales", "la-trigonometrie", "les-probabilites"],
    "les-ensembles-de-nombres": ["les-fractions", "les-racines-carrees"],
    "le-second-degre": ["les-identites-remarquables", "les-fonctions", "l-equation-produit-nul-et-les-systemes"],
    "les-vecteurs": ["le-reperage", "les-transformations"],
    "les-suites": ["les-fonctions", "les-puissances"],
    "la-derivee": ["les-fonctions", "la-vitesse"],
    "les-nombres-complexes": ["les-ensembles-de-nombres", "le-second-degre"],
    "le-nombre-pi": ["les-formes-geometriques"],
    "les-grands-nombres-et-l-infini": ["les-puissances"],
    "la-cryptographie": ["les-nombres-premiers"],
    "les-paradoxes-de-probabilite": ["les-probabilites"],
    "les-fractales": ["les-suites"],
    "les-jeux-de-strategie": ["le-binaire-et-les-bases"],
    "les-maths-et-la-musique": ["les-fractions", "les-puissances"],
    "les-atomes-et-les-molecules": ["les-etats-de-la-matiere"],
    "les-melanges-et-les-solutions": ["les-etats-de-la-matiere"],
    "les-transformations-chimiques": ["les-atomes-et-les-molecules"],
    "les-acides-et-les-bases": ["les-transformations-chimiques", "les-melanges-et-les-solutions"],
    "l-univers-et-le-systeme-solaire": ["la-lumiere"],
    "les-forces": ["le-mouvement"],
    "le-poids-et-la-masse": ["les-forces"],
    "la-gravitation": ["le-poids-et-la-masse", "les-puissances"],
    "l-energie-cinetique-et-la-securite-routiere": ["les-formes-d-energie", "la-vitesse"],
    "la-loi-d-ohm": ["les-circuits-electriques"],
    "la-puissance-et-l-energie-electrique": ["la-loi-d-ohm", "les-formes-d-energie"],
    "les-signaux-et-la-communication": ["le-son", "la-lumiere"],
    "revisions-brevet-physique": ["les-transformations-chimiques", "la-gravitation", "la-loi-d-ohm", "les-signaux-et-la-communication"],
    "le-ciel-bleu-et-l-arc-en-ciel": ["la-lumiere"],
    "la-physique-du-sport": ["le-mouvement", "les-formes-d-energie"],
    "le-climat-et-l-effet-de-serre": ["les-formes-d-energie", "les-transformations-chimiques"],
}

# Pages sans quiz noté : les ouvrir suffit.
NOQUIZ = ["le-nombre-pi", "le-nombre-e", "le-theoreme-de-pythagore", "le-theoreme-de-thales", "les-formes-geometriques"]

EXTRA = {
    "revisions-brevet": ("Grand quiz de révision : maths", "Des questions de tous les thèmes, avec ton score par thème.", "🎯"),
    "revisions-brevet-physique": ("Grand quiz de révision : physique", "Des questions de physique-chimie de tous les thèmes.", "🎯"),
}

CSS = r"""
:root {
  --paper: #f6f7fb; --grid: #e2e6f0; --card: #ffffff; --ink: #1d2233; --soft: #545b72; --line: #d6dae6;
  --red: #cf3a52; --navy: #1f2a5c; --hl: #ffd34d; --ok: #15803d; --ok-s: #dcf3e3; --mid: #b45309; --mid-s: #fbe7cf;
  --maths: #2346b5; --physique: #0e7490; --numerique: #b91c1c; --religions: #6d28d9;
  --f-display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --f-body: "Atkinson Hyperlegible", "Segoe UI", system-ui, sans-serif;
  --f-mono: "JetBrains Mono", ui-monospace, Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #10131c; --grid: #1a1f2c; --card: #171b27; --ink: #eceff7; --soft: #a9b0c6; --line: #2b3142; --red: #ff7d92;
  --navy: #a9b8ff; --ok: #4ade80; --ok-s: #14301f; --mid: #f5a35c; --mid-s: #46301a; --maths: #8fb0ff; --physique: #67e8f9; --numerique: #fca5a5; --religions: #c4b5fd; color-scheme: dark; } }
:root[data-theme="dark"] {
  --paper: #10131c; --grid: #1a1f2c; --card: #171b27; --ink: #eceff7; --soft: #a9b0c6; --line: #2b3142; --red: #ff7d92;
  --navy: #a9b8ff; --ok: #4ade80; --ok-s: #14301f; --mid: #f5a35c; --mid-s: #46301a; --maths: #8fb0ff; --physique: #67e8f9; --numerique: #fca5a5; --religions: #c4b5fd; color-scheme: dark; }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; color: var(--ink); font: 17px/1.6 var(--f-body);
  background-color: var(--paper);
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 28px 28px; }
main.page { max-width: 1040px; margin: 0 auto; padding: 24px 16px 56px; display: flex; flex-direction: column; gap: 28px; }
h1 { margin: 0; font-family: var(--f-display); font-weight: 800; font-size: clamp(2.1rem, 6vw, 3.1rem); line-height: 1.1; }
h2 { margin: 0; font-family: var(--f-display); font-weight: 800; font-size: 1.45rem; line-height: 1.2; }
.eyebrow { font-family: var(--f-mono); font-size: .8rem; letter-spacing: .08em; text-transform: uppercase; color: var(--red); }
.lead { font-size: 1.12rem; color: var(--soft); max-width: 62ch; margin: 8px 0 0; }
.soft { color: var(--soft); }
.subjects { display: flex; gap: 6px; flex-wrap: wrap; }
.subjects button { font: 800 .95rem var(--f-display); padding: 7px 16px; border-radius: 999px; border: 2px solid var(--ink); background: var(--card); color: var(--ink); cursor: pointer; }
.subjects button[aria-pressed="true"] { background: var(--ink); color: var(--paper); }
.tracks { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 240px), 1fr)); gap: 14px; }
.track { text-align: left; display: flex; flex-direction: column; gap: 6px; padding: 14px 16px; border: 2px solid var(--ink); border-radius: 12px; background: var(--card); color: var(--ink); cursor: pointer; font: inherit; box-shadow: 3px 3px 0 var(--ink); border-top: 7px solid var(--c); min-width: 0; }
.track:hover { transform: translate(-1px, -1px); box-shadow: 4px 4px 0 var(--ink); }
.track[aria-pressed="true"] { outline: 3px solid var(--c); outline-offset: 2px; }
.track strong { font-family: var(--f-display); font-size: 1.1rem; line-height: 1.2; }
.track .lvl { font: 600 .78rem var(--f-mono); color: var(--soft); }
.bar { height: 9px; border-radius: 99px; background: var(--line); overflow: hidden; }
.bar i { display: block; height: 100%; background: var(--ok); }
.track .count { font: 600 .82rem var(--f-mono); color: var(--soft); }
.next { display: grid; grid-template-columns: 1fr auto; gap: 10px 20px; align-items: center; padding: 18px 20px; border: 2px solid var(--ink); border-radius: 14px; background: var(--card); box-shadow: 5px 5px 0 var(--ink); }
.next .tag { font: 700 .8rem var(--f-mono); color: var(--red); text-transform: uppercase; letter-spacing: .06em; }
.next h3 { margin: 2px 0 4px; font: 800 1.45rem/1.2 var(--f-display); }
.next p { margin: 0; color: var(--soft); }
.next .warn { grid-column: 1 / -1; margin: 0; padding: 10px 12px; border-radius: 10px; background: var(--mid-s); color: var(--ink); }
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; text-decoration: none; font: 800 1rem var(--f-display); padding: 10px 18px; border-radius: 12px; background: var(--navy); color: var(--paper); border: 2px solid var(--navy); white-space: nowrap; }
.btn:hover { filter: brightness(1.08); }
.steps { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px; position: relative; }
.steps li { display: grid; grid-template-columns: 40px 1fr auto; gap: 12px; align-items: center; padding: 10px 14px; background: var(--card); border: 1.5px solid var(--line); border-radius: 12px; min-width: 0; }
.steps li.current { border: 2px solid var(--navy); box-shadow: 3px 3px 0 var(--navy); }
.dot { width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; font: 800 1rem var(--f-display); border: 2px solid var(--line); color: var(--soft); background: var(--paper); }
li.done .dot { background: var(--ok); border-color: var(--ok); color: var(--paper); }
li.started .dot { background: var(--mid-s); border-color: var(--mid); color: var(--mid); }
.steps a.t { color: var(--ink); font-weight: 700; text-decoration: none; overflow-wrap: anywhere; }
.steps a.t:hover { text-decoration: underline; }
.steps .meta { font-size: .88rem; color: var(--soft); }
.steps .meta a { color: inherit; }
.state { font: 700 .78rem var(--f-mono); padding: 3px 9px; border-radius: 99px; border: 1.5px solid var(--line); color: var(--soft); white-space: nowrap; }
li.done .state { border-color: var(--ok); color: var(--ok); background: var(--ok-s); }
li.started .state { border-color: var(--mid); color: var(--mid); background: var(--mid-s); }
.reco { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr)); gap: 12px; }
.reco a { display: flex; flex-direction: column; gap: 4px; padding: 12px 14px; border-radius: 12px; border: 2px solid var(--ink); background: var(--card); color: var(--ink); text-decoration: none; box-shadow: 3px 3px 0 var(--ink); min-width: 0; }
.reco a span { font: 700 .78rem var(--f-mono); color: var(--red); text-transform: uppercase; letter-spacing: .05em; }
.reco a em { font-style: normal; color: var(--soft); font-size: .92rem; }
.empty { color: var(--soft); }
.steps .side { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }
.track .mix { display: flex; flex-wrap: wrap; gap: 4px; }
footer { color: var(--soft); font-size: .9rem; text-align: center; }
@media (max-width: 560px) {
  .tracks { grid-template-columns: 1fr 1fr; gap: 10px; }
  .track { padding: 10px 12px; }
  .track .soft { display: none; }
  .track strong { font-size: .98rem; }
  .next { grid-template-columns: 1fr; }
  .next .btn { justify-self: start; }
  .steps li { grid-template-columns: 34px 1fr; }
  .steps li .side { grid-column: 2; flex-direction: row; justify-self: start; align-items: center; }
  .dot { width: 30px; height: 30px; font-size: .9rem; }
}
"""

JS = r"""
(function () {
  var D = JSON.parse(document.getElementById('data').textContent);
  var KEY = 'tutoriels-progression-v1', TKEY = 'tutoriels-parcours-v1';
  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || null; } catch (e) { return null; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  var P = load(KEY) || {};
  function st(id) {
    var p = P[id + '.html'];
    if (!p) return 'todo';
    if (D.noquiz.indexOf(id) >= 0) return 'done';
    if (p.total) return p.best / p.total >= 0.75 ? 'done' : 'started';
    return 'started';
  }
  var DL = { 1: 'Facile', 2: 'Moyen', 3: 'Difficile' };
  function diffBadge(id) { var d = D.diff[id]; return d ? '<span class="diff d' + d + '">' + DL[d] + '</span>' : ''; }
  function diffMix(steps) { var c = { 1: 0, 2: 0, 3: 0 }; steps.forEach(function (s) { if (D.diff[s]) c[D.diff[s]]++; });
    return [1, 2, 3].filter(function (k) { return c[k]; }).map(function (k) { return '<span class="diff d' + k + '">' + c[k] + ' ' + DL[k].toLowerCase() + '</span>'; }).join(' '); }
  function info(id) { return D.pages[id] || { t: id, d: '' }; }
  function link(id) { return '<a href="' + id + '.html">' + esc(info(id).t) + '</a>'; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function missing(id) { return (D.pre[id] || []).filter(function (x) { return st(x) !== 'done'; }); }
  function nextOf(tr) {
    for (var i = 0; i < tr.steps.length; i++) if (st(tr.steps[i]) !== 'done') return tr.steps[i];
    return null;
  }
  var pref = load(TKEY) || {};
  var subject = pref.subject || (location.hash === '#physique' ? 'physique' : 'maths');
  if (location.hash === '#physique') subject = 'physique';
  if (location.hash === '#maths') subject = 'maths';
  if (location.hash === '#numerique') subject = 'numerique';
  if (location.hash === '#religions') subject = 'religions';
  var current = pref.track;

  function trackById(id) { for (var i = 0; i < D.tracks.length; i++) if (D.tracks[i].id === id) return D.tracks[i]; return null; }
  function pickDefault() {
    var list = D.tracks.filter(function (t) { return t.subject === subject; });
    for (var i = 0; i < list.length; i++) if (nextOf(list[i])) return list[i].id;
    return list[0].id;
  }
  if (!trackById(current) || trackById(current).subject !== subject) current = pickDefault();

  function renderSubjects() {
    document.querySelectorAll('.subjects button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.s === subject));
      b.onclick = function () { subject = b.dataset.s; current = pickDefault(); save(TKEY, { subject: subject, track: current }); render(); };
    });
  }
  function renderTracks() {
    var box = document.getElementById('tracks');
    box.innerHTML = D.tracks.filter(function (t) { return t.subject === subject; }).map(function (t) {
      var done = t.steps.filter(function (s) { return st(s) === 'done'; }).length;
      return '<button type="button" class="track" style="--c:var(--' + t.subject + ')" data-id="' + t.id + '" aria-pressed="' + (t.id === current) + '">' +
        '<span class="lvl">' + esc(t.level) + '</span><strong>' + esc(t.title) + '</strong><span class="soft">' + esc(t.desc) + '</span>' +
        '<span class="bar" aria-hidden="true"><i style="width:' + Math.round(100 * done / t.steps.length) + '%"></i></span>' +
        '<span class="count">' + done + ' / ' + t.steps.length + ' étapes réussies</span><span class="mix">' + diffMix(t.steps) + '</span></button>';
    }).join('');
    box.querySelectorAll('.track').forEach(function (b) {
      b.onclick = function () { current = b.dataset.id; save(TKEY, { subject: subject, track: current }); render(); document.getElementById('trackTitle').scrollIntoView({ behavior: 'smooth', block: 'start' }); };
    });
  }
  function renderNext(tr) {
    var box = document.getElementById('nextBox'), id = nextOf(tr);
    if (!id) {
      box.innerHTML = '<div><span class="tag">Parcours terminé</span><h3>Bravo, tu as réussi tout le parcours « ' + esc(tr.title) + ' » !</h3><p>Choisis un autre parcours ci-dessus, ou refais un quiz pour garder la main.</p></div>';
      return;
    }
    var miss = missing(id), s = st(id), inf = info(id);
    box.innerHTML = '<div><span class="tag">Ta prochaine étape</span> ' + diffBadge(id) + '<h3>' + esc(inf.t) + '</h3><p>' + esc(inf.d) + '</p></div>' +
      '<a class="btn" href="' + id + '.html">' + (s === 'started' ? 'Continuer' : 'Commencer') + ' →</a>' +
      (miss.length ? '<p class="warn">Conseil : avant, revois ' + miss.map(link).join(' et ') + '. Ce sera plus facile.</p>' : '') +
      (s === 'started' && P[id + '.html'] && P[id + '.html'].total ? '<p class="warn">Ton meilleur score au quiz : ' + P[id + '.html'].best + ' / ' + P[id + '.html'].total + '. Vise 6 / 8 pour valider l\'étape.</p>' : '');
  }
  function renderSteps(tr) {
    document.getElementById('trackTitle').textContent = tr.title;
    var nid = nextOf(tr), ol = document.getElementById('steps');
    ol.innerHTML = tr.steps.map(function (id, i) {
      var s = st(id), p = P[id + '.html'], pre = D.pre[id] || [];
      var label = s === 'done' ? 'réussi' : s === 'started' ? (p && p.total ? 'quiz ' + p.best + '/' + p.total : 'commencé') : 'à faire';
      var meta = pre.length ? 'Après : ' + pre.map(link).join(', ') : esc(info(id).d);
      return '<li class="' + s + (id === nid ? ' current' : '') + '"><span class="dot">' + (s === 'done' ? '✓' : i + 1) + '</span>' +
        '<span><a class="t" href="' + id + '.html">' + esc(info(id).t) + '</a><br><span class="meta">' + meta + '</span></span>' +
        '<span class="side">' + diffBadge(id) + '<span class="state">' + label + '</span></span></li>';
    }).join('');
  }
  function renderReco() {
    var out = [], seen = {};
    function add(kind, id, why) { if (seen[id] || out.length >= 6) return; seen[id] = 1; out.push({ kind: kind, id: id, why: why }); }
    D.tracks.forEach(function (t) {
      t.steps.forEach(function (id) {
        var p = P[id + '.html'];
        if (p && p.total && p.best / p.total < 0.75) add('À refaire', id, 'Ton meilleur score : ' + p.best + ' / ' + p.total + '. Refais le quiz pour valider.');
      });
    });
    D.tracks.filter(function (t) { return t.subject === subject; }).forEach(function (t) {
      var id = nextOf(t);
      if (id && !missing(id).length) add(t.id === current ? 'Prochaine étape' : t.title, id, info(id).d);
    });
    D.tracks.forEach(function (t) {
      t.steps.forEach(function (id) {
        if (st(id) === 'todo' && (D.pre[id] || []).length && !missing(id).length) add('Tu es prêt', id, 'Tu as réussi ce qu\'il faut savoir avant.');
      });
    });
    var box = document.getElementById('reco');
    box.innerHTML = out.length ? out.map(function (r) { return '<a href="' + r.id + '.html"><span>' + esc(r.kind) + '</span><strong>' + esc(info(r.id).t) + '</strong><em>' + esc(r.why) + '</em></a>'; }).join('')
      : '<p class="empty">Commence un parcours : tes conseils apparaîtront ici.</p>';
  }
  function renderSummary() {
    var all = [], done = 0;
    D.tracks.forEach(function (t) { t.steps.forEach(function (id) { if (all.indexOf(id) < 0) all.push(id); }); });
    all.forEach(function (id) { if (st(id) === 'done') done++; });
    var opened = all.filter(function (id) { return P[id + '.html']; }).length;
    document.getElementById('summary').textContent = opened
      ? 'Tu as ouvert ' + opened + ' pages sur ' + all.length + ' et réussi ' + done + ' étapes.'
      : 'Tu n\'as encore rien commencé sur cet appareil : choisis un parcours et lance-toi !';
  }
  function render() {
    var tr = trackById(current);
    renderSubjects(); renderTracks(); renderNext(tr); renderSteps(tr); renderReco(); renderSummary();
  }
  window.__parcours = { status: st, nextOf: function (id) { return nextOf(trackById(id)); }, missing: missing, data: D, render: render };
  render();
  window.addEventListener('pageshow', function () { P = load(KEY) || {}; render(); });
})();
"""


def landing_pages():
    pages = {}
    for f in ("index.html", "physique.html", "numerique.html", "religions.html"):
        s = (ROOT / f).read_text(encoding="utf-8")
        for href, title, desc in re.findall(r'<a class="card" href="([^"]+)\.html">.*?<strong>(.*?)</strong><span class="d">(.*?)</span>', s, re.S):
            pages[href] = {"t": html.unescape(re.sub(r"<[^>]+>", "", title)).strip(), "d": html.unescape(re.sub(r"<[^>]+>", "", desc)).strip()}
    for k, (t, d, _) in EXTRA.items():
        pages[k] = {"t": t, "d": d}
    return pages


def main():
    pages = landing_pages()
    used = [s for _, _, _, _, _, steps in TRACKS for s in steps]
    missing = [p for p in pages if p not in used]
    unknown = [s for s in used + list(PRE) + [x for v in PRE.values() for x in v] if s not in pages]
    if missing:
        print("pas dans un parcours :", missing)
    if unknown:
        print("pages inconnues :", sorted(set(unknown)))
    data = {
        "tracks": [{"id": i, "subject": su, "title": t, "level": lv, "desc": d, "steps": st} for i, su, t, lv, d, st in TRACKS],
        "pre": PRE, "noquiz": NOQUIZ, "pages": pages, "diff": difficulte.DIFF,
    }
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Mon parcours</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=JetBrains+Mono:wght@500;600&display=swap">
<style>{CSS}{difficulte.BADGE_CSS}</style>
</head>
<body>
<main class="page">
<header>
  <span class="eyebrow">Formation personnalisée</span>
  <h1>Mon parcours</h1>
  <p class="lead">Choisis un parcours : la page suit ce que tu as déjà réussi, te dit quoi faire ensuite et te conseille de revoir une notion quand il en manque une. Une étape est réussie avec au moins 6 / 8 au quiz.</p>
  <p class="soft" id="summary"></p>
</header>
<nav class="subjects" aria-label="Choisir la matière"><button type="button" data-s="maths">Maths</button><button type="button" data-s="physique">Physique-chimie</button><button type="button" data-s="numerique">Numérique</button><button type="button" data-s="religions">Religions</button></nav>
<section class="next" id="nextBox" aria-live="polite"></section>
<section aria-labelledby="h-tracks"><h2 id="h-tracks" style="margin-bottom:12px">Choisis ton parcours</h2><div class="tracks" id="tracks"></div></section>
<section aria-labelledby="h-reco"><h2 id="h-reco" style="margin-bottom:12px">Conseillé pour toi</h2><div class="reco" id="reco"></div></section>
<section aria-labelledby="trackTitle"><h2 id="trackTitle" style="margin-bottom:12px"></h2><ol class="steps" id="steps"></ol></section>
<footer>Ta progression est enregistrée seulement sur cet appareil, dans ce navigateur. · © 2026 Nicolas Meynet</footer>
</main>
<script type="application/json" id="data">{json.dumps(data, ensure_ascii=False)}</script>
<script>{JS}</script>
</body>
</html>
"""
    (ROOT / "parcours.html").write_text(page, encoding="utf-8", newline="\n")
    print("parcours.html :", len(TRACKS), "parcours,", len(set(used)), "étapes")


if __name__ == "__main__":
    main()
