"""Construit fiches.html : les fiches « l'essentiel » à imprimer.

Pour chaque tutoriel de l'accueil, on reprend sa section « À retenir »,
dans l'ordre et les catégories de index.html. Relancer après tout ajout :
    python tools/fiches.py && python tools/liens.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Le tutoriel sur les formes construit son tableau en JavaScript : version fixe ici.
FORMES = """<div class="box">
<span>• <strong>Carré</strong> (côté c) : P = 4 × c ; A = c².</span>
<span>• <strong>Rectangle</strong> (L, l) : P = 2 × (L + l) ; A = L × l.</span>
<span>• <strong>Triangle</strong> (base b, hauteur h) : A = b × h ÷ 2.</span>
<span>• <strong>Parallélogramme</strong> : A = b × h. <strong>Losange</strong> : A = D × d ÷ 2. <strong>Trapèze</strong> : A = (B + b) × h ÷ 2.</span>
<span>• <strong>Cercle</strong> (rayon r) : P = 2 × π × r ; A = π × r².</span>
<span>• <strong>Cube</strong> (arête a) : V = a³. <strong>Pavé</strong> : V = L × l × h. <strong>Cylindre</strong> : V = π × r² × h.</span>
<span>• <strong>Pyramide</strong> et <strong>cône</strong> : V = aire de la base × h ÷ 3. <strong>Boule</strong> : V = 4/3 × π × r³.</span>
<span>• Formule d'Euler pour les solides : faces + sommets − arêtes = 2.</span>
</div>"""

CSS = """
:root {
  --paper: #f6f7fb; --card: #ffffff; --ink: #1d2233; --soft: #545b72; --line: #d6dae6; --navy: #1f2a5c; --hl: #ffd34d;
  --f-display: "Bricolage Grotesque", system-ui, sans-serif; --f-body: "Atkinson Hyperlegible", system-ui, sans-serif; --f-mono: "JetBrains Mono", ui-monospace, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --paper: #10131c; --card: #171b27; --ink: #eceff7; --soft: #a9b0c6; --line: #2b3142; --navy: #a9b8ff; } }
:root[data-theme="dark"] { --paper: #10131c; --card: #171b27; --ink: #eceff7; --soft: #a9b0c6; --line: #2b3142; --navy: #a9b8ff; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); font: 16px/1.55 var(--f-body); }
.page { max-width: 1000px; margin: 0 auto; padding: 20px 16px 48px; }
h1 { font-family: var(--f-display); font-weight: 800; font-size: clamp(1.9rem, 6vw, 2.6rem); line-height: 1.1; margin: 8px 0; }
h2 { font-family: var(--f-display); font-weight: 800; font-size: 1.35rem; margin: 0; }
.lead { color: var(--soft); max-width: 60ch; }
.home { display: inline-flex; padding: 6px 14px; border: 2px solid var(--ink); border-radius: 999px; background: var(--card); color: var(--ink); font-weight: 700; text-decoration: none; box-shadow: 2px 2px 0 var(--ink); }
.tools { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px; align-items: center; }
.tools button { font: 700 .95rem var(--f-body); padding: 8px 14px; border: 2px solid var(--ink); border-radius: 10px; background: var(--card); color: var(--ink); cursor: pointer; box-shadow: 2px 2px 0 var(--ink); }
.tools button.main { background: var(--navy); color: var(--paper); border-color: var(--navy); }
.cat { margin: 28px 0 0; }
.subject { font-size: 1.8rem; margin: 36px 0 0; color: var(--navy); }
.cat-head { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; border-bottom: 3px solid var(--navy); padding-bottom: 6px; margin-bottom: 14px; }
.cat-head button { font: 700 .85rem var(--f-body); padding: 4px 10px; border: 1.5px solid var(--soft); border-radius: 8px; background: transparent; color: var(--soft); cursor: pointer; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 14px; }
.fiche { background: var(--card); border: 1.5px solid var(--line); border-radius: 12px; padding: 14px 16px; min-width: 0; break-inside: avoid; }
.fiche h3 { margin: 0 0 8px; font: 800 1.08rem/1.25 var(--f-display); }
.fiche h3 a { color: inherit; text-decoration: none; }
.fiche h3 a:hover { text-decoration: underline; }
.fiche .box { display: flex; flex-direction: column; gap: 6px; }
.fiche .box > span, .fiche p { margin: 0; overflow-wrap: anywhere; }
.fiche strong { font-weight: 700; }
.fiche a { color: inherit; }
.mono, .fiche code { font-family: var(--f-mono); font-size: .92em; }
.soft { color: var(--soft); }
.set { font-weight: 700; }
.v { position: relative; display: inline-block; line-height: 1; padding-top: .34em; white-space: nowrap; }
.v::before { content: ""; position: absolute; left: .06em; right: .12em; top: .1em; border-top: .085em solid currentColor; }
.v::after { content: ""; position: absolute; right: .03em; top: -.01em; width: .22em; height: .22em; border-top: .085em solid currentColor; border-right: .085em solid currentColor; transform: rotate(45deg); }
footer { margin-top: 36px; color: var(--soft); font-size: .9rem; text-align: center; }
@media print {
  :root { --paper: #fff; --card: #fff; --ink: #000; --soft: #333; --line: #999; --navy: #1f2a5c; }
  body { font-size: 11.5pt; background: #fff; }
  .home, .tools, .cat-head button, footer { display: none !important; }
  .page { max-width: none; padding: 0; }
  .cat { break-before: page; margin: 0; }
  .cat:first-of-type { break-before: auto; }
  .subject { break-before: page; }
  .subject:first-of-type { break-before: auto; }
  body[data-only] .subject { display: none; }
  .grid { grid-template-columns: 1fr 1fr; gap: 8px; }
  .fiche { border-color: #999; padding: 8px 10px; }
  .fiche h3 a::after { content: ""; }
  body[data-only] .cat { display: none; }
  body[data-only] .cat.only { display: block; break-before: auto; }
  body[data-only] .intro { display: none; }
}
"""

JS = """<script>
(function () {
  document.getElementById('printAll').addEventListener('click', function () { document.body.removeAttribute('data-only'); window.print(); });
  document.querySelectorAll('.cat-head button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.cat').forEach(function (c) { c.classList.remove('only'); });
      b.closest('.cat').classList.add('only');
      document.body.setAttribute('data-only', '1');
      window.print();
    });
  });
  window.addEventListener('afterprint', function () {
    document.body.removeAttribute('data-only');
    document.querySelectorAll('.cat').forEach(function (c) { c.classList.remove('only'); });
  });
})();
</script>"""


def summary(path):
    if path.name == "les-formes-geometriques.html":
        return FORMES
    if not path.exists():
        return None
    s = path.read_text(encoding="utf-8")
    m = re.search(r'<section[^>]*>\s*<span class="eyebrow">À retenir[^<]*</span>(.*?)</section>', s, re.S)
    if not m:
        return None
    body = m.group(1).strip()
    body = re.sub(r"<(button|input|select|textarea|svg|canvas)\b.*?(</\1>|/?>)", "", body, flags=re.S)
    body = re.sub(r'\s(id|data-[\w-]+)="[^"]*"', "", body)
    return body


def main():
    out = []
    count = 0
    subjects = [("index.html", "maths", "Maths"), ("physique.html", "physique", "Physique-chimie")]
    for landing, sid, sname in subjects:
      if not (ROOT / landing).exists():
          continue
      idx = (ROOT / landing).read_text(encoding="utf-8")
      out.append(f'<h2 class="subject" id="{sid}">{sname}</h2>')
      for sec in re.finditer(r'<section class="cat" id="([^"]+)"[^>]*>(.*?)</section>', idx, re.S):
        cid, inner = sec.group(1), sec.group(2)
        name = html.unescape(re.search(r"<h2[^>]*>(.*?)</h2>", inner).group(1))
        cards = re.findall(r'<a class="card[^"]*" href="([^"]+\.html)".*?<strong>(.*?)</strong>', inner, re.S)
        items = []
        for href, title in cards:
            body = summary(ROOT / href)
            if not body:
                print("pas de « À retenir » :", href)
                continue
            items.append(f'<article class="fiche"><h3><a href="{href}">{title}</a></h3>\n{body}\n</article>')
            count += 1
        if items:
            out.append(f'<section class="cat" id="{cid}"><div class="cat-head"><h2>{html.escape(name)}</h2>'
                       f'<button type="button">Imprimer cette catégorie</button></div>\n<div class="grid">\n'
                       + "\n".join(items) + "\n</div></section>")
    page = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Fiches à imprimer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=JetBrains+Mono:wght@500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<main class="page">
<div class="intro">
<h1>Les fiches « l'essentiel »</h1>
<p class="lead">L'essentiel de chaque tutoriel sur une seule page, à relire avant un contrôle ou à imprimer. Chaque catégorie commence sur une nouvelle feuille.</p>
</div>
<div class="tools"><button type="button" class="main" id="printAll">Imprimer toutes les fiches</button><span class="soft">{count} fiches</span></div>
{chr(10).join(out)}
<footer>Fiches générées à partir des tutoriels · © 2026 Nicolas Meynet</footer>
</main>
{JS}
</body>
</html>
"""
    (ROOT / "fiches.html").write_text(page, encoding="utf-8", newline="\n")
    print(count, "fiches")


if __name__ == "__main__":
    main()
