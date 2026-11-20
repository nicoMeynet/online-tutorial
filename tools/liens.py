"""Ajoute la navigation entre tutoriels dans les pages du dépôt.

- un lien « ← Tous les tutoriels » en haut de chaque page ;
- les mentions « le tutoriel sur … » deviennent de vrais liens ;
- en bas de page : tutoriel précédent / suivant (ordre de index.html) et retour à l'accueil.

Le script peut être relancé autant de fois qu'on veut : il remplace ce qu'il a déjà ajouté.
Usage : python tools/liens.py            (toutes les pages)
        python tools/liens.py page.html  (certaines pages)
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import difficulte  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

TOPICS = [
    ("comment on te manipule", "comment-on-te-manipule.html"),
    ("la manipulation", "comment-on-te-manipule.html"),
    ("les virus", "les-virus-et-les-mises-a-jour.html"),
    ("les virus et les mises à jour", "les-virus-et-les-mises-a-jour.html"),
    ("naviguer en sécurité", "naviguer-en-securite.html"),
    ("le chiffrement", "naviguer-en-securite.html"),
    ("les données personnelles", "les-donnees-personnelles.html"),
    ("la vie privée", "les-donnees-personnelles.html"),
    ("le cyberharcèlement", "le-cyberharcelement.html"),
    ("le harcèlement", "le-cyberharcelement.html"),
    ("les fausses infos", "vraie-ou-fausse-info.html"),
    ("les fake news", "vraie-ou-fausse-info.html"),
    ("les deepfakes", "les-images-truquees-et-les-deepfakes.html"),
    ("les images truquées", "les-images-truquees-et-les-deepfakes.html"),
    ("les réseaux sociaux", "les-reseaux-sociaux-et-les-algorithmes.html"),
    ("les algorithmes de recommandation", "les-reseaux-sociaux-et-les-algorithmes.html"),
    ("bien utiliser l'IA", "bien-utiliser-l-ia.html"),
    ("bien utiliser l’IA", "bien-utiliser-l-ia.html"),
    ("l'intelligence artificielle", "comment-une-ia-ecrit.html"),
    ("l’intelligence artificielle", "comment-une-ia-ecrit.html"),
    ("comment une IA écrit", "comment-une-ia-ecrit.html"),
    ("Internet", "comment-marche-internet.html"),
    ("comment marche Internet", "comment-marche-internet.html"),
    ("les octets", "les-octets-et-le-stockage.html"),
    ("le stockage", "les-octets-et-le-stockage.html"),
    ("les pixels", "les-pixels-et-la-compression.html"),
    ("la compression", "les-pixels-et-la-compression.html"),
    ("la programmation", "programmer-pas-a-pas.html"),
    ("programmer pas à pas", "programmer-pas-a-pas.html"),
    ("le temps d'écran", "le-temps-d-ecran-et-l-attention.html"),
    ("le temps d’écran", "le-temps-d-ecran-et-l-attention.html"),
    ("les achats dans les jeux", "les-achats-dans-les-jeux.html"),
    ("les achats intégrés", "les-achats-dans-les-jeux.html"),
    ("les mots de passe", "les-mots-de-passe.html"),
    ("les arnaques", "reperer-les-arnaques.html"),
    ("l'hameçonnage", "reperer-les-arnaques.html"),
    ("le ciel bleu et l'arc-en-ciel", "le-ciel-bleu-et-l-arc-en-ciel.html"),
    ("l'arc-en-ciel", "le-ciel-bleu-et-l-arc-en-ciel.html"),
    ("la physique du sport", "la-physique-du-sport.html"),
    ("le climat et l'effet de serre", "le-climat-et-l-effet-de-serre.html"),
    ("l'effet de serre", "le-climat-et-l-effet-de-serre.html"),
    ("les acides et les bases", "les-acides-et-les-bases.html"),
    ("le pH", "les-acides-et-les-bases.html"),
    ("la gravitation", "la-gravitation.html"),
    ("l'énergie cinétique et la sécurité routière", "l-energie-cinetique-et-la-securite-routiere.html"),
    ("l'énergie cinétique", "l-energie-cinetique-et-la-securite-routiere.html"),
    ("la loi d'Ohm", "la-loi-d-ohm.html"),
    ("la puissance et l'énergie électrique", "la-puissance-et-l-energie-electrique.html"),
    ("la puissance électrique", "la-puissance-et-l-energie-electrique.html"),
    ("les signaux et la communication", "les-signaux-et-la-communication.html"),
    ("les signaux", "les-signaux-et-la-communication.html"),
    ("les mélanges et les solutions", "les-melanges-et-les-solutions.html"),
    ("les transformations chimiques", "les-transformations-chimiques.html"),
    ("l'Univers et le système solaire", "l-univers-et-le-systeme-solaire.html"),
    ("l'Univers", "l-univers-et-le-systeme-solaire.html"),
    ("les forces", "les-forces.html"),
    ("les formes d'énergie", "les-formes-d-energie.html"),
    ("le son", "le-son.html"),
    ("les états de la matière", "les-etats-de-la-matiere.html"),
    ("les atomes et les molécules", "les-atomes-et-les-molecules.html"),
    ("le mouvement", "le-mouvement.html"),
    ("le poids et la masse", "le-poids-et-la-masse.html"),
    ("les circuits électriques", "les-circuits-electriques.html"),
    ("la lumière", "la-lumiere.html"),
    ("la cryptographie", "la-cryptographie.html"),
    ("le binaire et les bases", "le-binaire-et-les-bases.html"),
    ("le binaire", "le-binaire-et-les-bases.html"),
    ("les paradoxes de probabilité", "les-paradoxes-de-probabilite.html"),
    ("les fractales", "les-fractales.html"),
    ("les jeux de stratégie", "les-jeux-de-strategie.html"),
    ("les maths et la musique", "les-maths-et-la-musique.html"),
    ("la sphère et la boule", "la-sphere-et-la-boule.html"),
    ("la sphère", "la-sphere-et-la-boule.html"),
    ("les droites remarquables", "les-droites-remarquables.html"),
    ("les quadrilatères", "les-quadrilateres.html"),
    ("la démonstration", "la-demonstration.html"),
    ("l'équation produit nul", "l-equation-produit-nul-et-les-systemes.html"),
    ("les systèmes", "l-equation-produit-nul-et-les-systemes.html"),
    ("les arrondis", "les-arrondis-et-ordres-de-grandeur.html"),
    ("les grandeurs composées", "les-grandeurs-composees.html"),
    ("le second degré", "le-second-degre.html"),
    ("les vecteurs", "les-vecteurs.html"),
    ("les suites", "les-suites.html"),
    ("la dérivée", "la-derivee.html"),
    ("les nombres complexes", "les-nombres-complexes.html"),
    ("les formes géométriques", "les-formes-geometriques.html"),
    ("les angles et les triangles", "les-angles-et-triangles.html"),
    ("la trigonométrie", "la-trigonometrie.html"),
    ("les racines carrées", "les-racines-carrees.html"),
    ("les nombres premiers", "les-nombres-premiers.html"),
    ("les statistiques", "les-statistiques.html"),
    ("les probabilités", "les-probabilites.html"),
    ("les inéquations", "les-inequations.html"),
    ("les conversions", "les-conversions.html"),
    ("les échelles", "les-echelles.html"),
    ("le repérage", "le-reperage.html"),
    ("l'algorithmique", "l-algorithmique.html"),
    ("le nombre d'or", "le-nombre-d-or.html"),
    ("l'infini", "les-grands-nombres-et-l-infini.html"),
    ("les grands nombres et l'infini", "les-grands-nombres-et-l-infini.html"),
    ("le nombre π", "le-nombre-pi.html"),
    ("le théorème de Pythagore", "le-theoreme-de-pythagore.html"),
    ("Pythagore", "le-theoreme-de-pythagore.html"),
    ("le théorème de Thalès", "le-theoreme-de-thales.html"),
    ("Thalès", "le-theoreme-de-thales.html"),
    ("les identités remarquables", "les-identites-remarquables.html"),
    ("le calcul littéral", "le-calcul-litteral.html"),
    ("les ensembles de nombres", "les-ensembles-de-nombres.html"),
    ("les priorités de calcul", "les-priorites-de-calcul.html"),
    ("les nombres relatifs", "les-nombres-relatifs.html"),
    ("la proportionnalité", "la-proportionnalite.html"),
    ("les transformations", "les-transformations.html"),
    ("les pourcentages", "les-pourcentages.html"),
    ("les puissances", "les-puissances.html"),
    ("les équations", "les-equations.html"),
    ("les fonctions", "les-fonctions.html"),
    ("les fractions", "les-fractions.html"),
    ("les angles", "les-angles-et-triangles.html"),
    ("la vitesse", "la-vitesse.html"),
    ("le nombre e", "le-nombre-e.html"),
    ("π", "le-nombre-pi.html"),
    ("e", "le-nombre-e.html"),
]
T = "|".join(re.escape(n) for n, _ in sorted(TOPICS, key=lambda t: -len(t[0])))  # longest first
MENTION = re.compile(r"(tutoriels? sur )(" + T + r")(?!\w)(\s*\([^)<]*\))?(?:(\s+et sur )(" + T + r")(?!\w))?")
FILE = dict(TOPICS)

ICONS = ('<!--ticons--><link rel="icon" href="icon.svg" type="image/svg+xml">'
         '<link rel="apple-touch-icon" href="apple-touch-icon.png">'
         '<link rel="manifest" href="manifest.webmanifest">'
         '<meta name="apple-mobile-web-app-title" content="Tutoriels">'
         '<script src="progress.js" defer></script><!--/ticons-->\n')

CSS = """<style id="tnav-css">
.tnav-top { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: center; margin: 0 0 4px; }
.tnav-home { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border: 2px solid var(--ink, #222); border-radius: 999px;
  background: var(--card, #fff); color: var(--ink, #222); font-weight: 700; font-size: .95rem; text-decoration: none; box-shadow: 2px 2px 0 var(--ink, #222); }
.tnav-home:hover, .tnav-home:focus-visible { transform: translate(-1px, -1px); box-shadow: 3px 3px 0 var(--ink, #222); }
a.tlink { color: inherit; font-weight: 700; text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 3px; }
.tnav-bottom { margin-top: 8px; display: flex; flex-direction: column; gap: 12px; }
.tnav-bottom h2 { margin: 0; }
.tnav-pn { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.tnav-pn a { display: flex; flex-direction: column; gap: 2px; padding: 12px 14px; border: 2px solid var(--ink, #222); border-radius: 10px;
  background: var(--card, #fff); color: var(--ink, #222); text-decoration: none; box-shadow: 3px 3px 0 var(--ink, #222); min-width: 0; }
.tnav-pn a span { font-size: .85rem; color: var(--ink-soft, #666); }
.tnav-pn a strong { overflow-wrap: anywhere; }
.tnav-pn a.next { text-align: right; grid-column: 2; }
.tnav-bottom .tnav-home { align-self: center; }
@media (max-width: 520px) { .tnav-pn { grid-template-columns: 1fr; } .tnav-pn a.next { grid-column: 1; } }
</style>
"""
CSS = CSS.replace("</style>", difficulte.BADGE_CSS + "</style>", 1)


# Une page d'accueil par matière : chaque tutoriel renvoie vers la sienne,
# et « précédent / suivant » reste dans la même matière.
LANDINGS = [("index.html", "Tous les tutoriels"), ("physique.html", "Tous les tutoriels de physique"), ("numerique.html", "Tous les tutoriels numériques")]
# Pages de révision qui ne sont pas des cartes mais appartiennent à une matière.
HOME_OF = {"physique.html": ("glossaire-physique.html", "revisions-brevet-physique.html")}


def landing_order():
    orders = []
    for landing, label in LANDINGS:
        f = ROOT / landing
        if not f.exists():
            continue
        cards = re.findall(r'<a class="card[^"]*" href="([^"]+\.html)".*?<strong>(.*?)</strong>', f.read_text(encoding="utf-8"), re.S)
        orders.append((landing, label, [(h, html.unescape(re.sub(r"<[^>]+>", "", t)).strip()) for h, t in cards]))
    return orders


def linkify(text, self_name):
    def one(name):
        f = FILE[name]
        return name if f == self_name else f'<a class="tlink" href="{f}">{name}</a>'

    def rep(m):
        before = text[:m.start()]
        if before.rfind("<a ") > before.rfind("</a>"):
            return m.group(0)  # déjà dans un lien
        out = m.group(1) + one(m.group(2)) + (m.group(3) or "")
        if m.group(5):
            out += m.group(4) + one(m.group(5))
        return out

    return MENTION.sub(rep, text)


def process(path, order):
    src = path.read_text(encoding="utf-8")
    src = re.sub(r'<style id="tnav-css">.*?</style>\n', "", src, flags=re.S)
    src = re.sub(r"<!--ticons-->.*?<!--/ticons-->\n", "", src, flags=re.S)
    # exact inverse of the insertions below, so reruns don't add blank lines
    src = re.sub(r'\n<!--tnav--><nav class="tnav-top".*?<!--/tnav-->\n', "", src, flags=re.S)
    src = re.sub(r'<!--tnav--><nav class="tnav-bottom".*?<!--/tnav-->\n', "", src, flags=re.S)
    assert src.count('<main class="page">') == 1 and src.count("</main>") == 1, path.name

    cut = src.rfind("<script>")
    body, tail = (src[:cut], src[cut:]) if cut > 0 else (src, "")
    body = linkify(body, path.name)
    src = body + tail

    home, label, seq = order[0][0], order[0][1], []
    for landing, lab, cards in order:
        if path.name in HOME_OF.get(landing, ()):
            home, label = landing, lab
        if any(h == path.name for h, _ in cards):
            home, label, seq = landing, lab, cards
    names = [h for h, _ in seq]
    titles = dict(seq)
    top = (f'<!--tnav--><nav class="tnav-top" aria-label="Navigation"><a class="tnav-home" href="{home}">← {label}</a>'
           f'{difficulte.badge(path.stem)}</nav><!--/tnav-->\n')
    bottom = ""
    if path.name in names:
        i = names.index(path.name)
        prev = names[i - 1] if i > 0 else None
        nxt = names[i + 1] if i + 1 < len(names) else None
        links = ""
        if prev:
            links += f'<a class="prev" href="{prev}"><span>← Précédent</span><strong>{html.escape(titles[prev])}</strong></a>'
        if nxt:
            links += f'<a class="next" href="{nxt}"><span>Suivant →</span><strong>{html.escape(titles[nxt])}</strong></a>'
        bottom = ('<!--tnav--><nav class="tnav-bottom" aria-label="Autres tutoriels"><h2>Continuer</h2>'
                  f'<div class="tnav-pn">{links}</div>'
                  f'<a class="tnav-home" href="{home}">⌂ {label}</a></nav><!--/tnav-->\n')

    src = src.replace('<main class="page">', '<main class="page">\n' + top, 1)
    end = src.index("</main>")
    foot = src.rfind("<footer", 0, end)
    at = foot if foot > src.index('<main class="page">') else end
    src = src[:at] + bottom + src[at:]
    src = src.replace("</head>", ICONS + CSS + "</head>", 1)
    path.write_text(src, encoding="utf-8", newline="\n")


def main():
    difficulte.apply_landings(ROOT)
    order = landing_order()
    files = [ROOT / a for a in sys.argv[1:]] or sorted(p for p in ROOT.glob("*.html") if p.name not in dict(LANDINGS))
    for p in files:
        process(p, order)
        print("ok", p.name)


if __name__ == "__main__":
    main()
