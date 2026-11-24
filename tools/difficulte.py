"""Difficulté de chaque tutoriel : 1 = facile, 2 = moyen, 3 = difficile.

Une seule source, utilisée par :
- tools/liens.py  : badge en haut de chaque tutoriel, et badges sur les cartes des accueils ;
- tools/parcours.py : badge sur chaque étape de « Mon parcours ».
Pour changer un niveau, modifier ce fichier puis relancer parcours.py et liens.py.
"""
import re
from pathlib import Path

LABELS = {1: "Facile", 2: "Moyen", 3: "Difficile"}

DIFF = {
    # Maths
    "les-priorites-de-calcul": 1, "les-nombres-relatifs": 1, "les-fractions": 2, "les-ensembles-de-nombres": 2,
    "les-puissances": 2, "les-racines-carrees": 2, "les-nombres-premiers": 2, "les-grands-nombres-et-l-infini": 2,
    "les-arrondis-et-ordres-de-grandeur": 1, "le-calcul-litteral": 2, "les-identites-remarquables": 3,
    "les-equations": 2, "l-equation-produit-nul-et-les-systemes": 3, "les-inequations": 2, "les-fonctions": 3,
    "la-proportionnalite": 1, "les-pourcentages": 2, "la-vitesse": 1, "les-grandeurs-composees": 2,
    "les-conversions": 1, "les-conversions-avancees": 2, "les-echelles": 1, "les-formes-geometriques": 1, "la-sphere-et-la-boule": 2,
    "les-angles-et-triangles": 1, "les-nombres-decimaux": 1, "les-triangles-isometriques-et-semblables": 2, "les-operations-posees": 1, "les-constructions-a-la-regle-et-au-compas": 1, "les-projections-et-les-vues": 2, "le-cercle-et-ses-angles": 2, "les-droites-remarquables": 2, "les-quadrilateres": 1,
    "le-theoreme-de-pythagore": 2, "le-theoreme-de-thales": 3, "la-trigonometrie": 3, "les-transformations": 1,
    "le-reperage": 1, "les-statistiques": 1, "les-probabilites": 2, "l-algorithmique": 1, "la-demonstration": 3,
    "le-second-degre": 3, "les-vecteurs": 3, "les-suites": 3, "la-derivee": 3, "l-integrale": 3, "les-nombres-complexes": 3,
    "la-cryptographie": 2, "le-binaire-et-les-bases": 2, "les-paradoxes-de-probabilite": 3, "les-fractales": 2,
    "les-jeux-de-strategie": 1, "les-maths-et-la-musique": 2, "le-nombre-pi": 1, "le-nombre-e": 2,
    "le-nombre-d-or": 1, "revisions-brevet": 3,
    # Physique-chimie
    "les-etats-de-la-matiere": 1, "les-melanges-et-les-solutions": 1, "les-atomes-et-les-molecules": 2,
    "les-transformations-chimiques": 2, "les-acides-et-les-bases": 2, "l-univers-et-le-systeme-solaire": 1,
    "le-mouvement": 1, "les-forces": 2, "le-poids-et-la-masse": 2, "la-gravitation": 3,
    "les-formes-d-energie": 2, "l-energie-cinetique-et-la-securite-routiere": 3, "les-circuits-electriques": 1,
    "la-loi-d-ohm": 2, "la-puissance-et-l-energie-electrique": 2, "la-lumiere": 1, "le-son": 1,
    "les-signaux-et-la-communication": 2, "le-ciel-bleu-et-l-arc-en-ciel": 2, "la-physique-du-sport": 2,
    "le-climat-et-l-effet-de-serre": 2, "revisions-brevet-physique": 3,
    # Géographie et citoyenneté
    "la-langue-francaise": 1, "la-grammaire": 2, "l-orthographe": 1, "la-ponctuation": 1, "la-conjugaison": 2, "la-geographie-de-la-suisse": 1, "l-histoire-de-la-suisse": 2, "la-geographie-du-monde": 1, "la-politique-suisse": 2,
    # Religions
    "les-religions-du-monde": 1, "l-hindouisme": 2, "le-bouddhisme": 2, "le-judaisme": 1, "le-christianisme": 1, "l-islam": 1, "les-sagesses-de-chine-et-du-japon": 2, "les-mythologies-antiques": 1, "les-fetes-et-calendriers": 2, "le-sikhisme": 1, "les-religions-traditionnelles": 1,
    # Numérique
    "reperer-les-arnaques": 1, "les-mots-de-passe": 1,
    "comment-on-te-manipule": 2, "les-virus-et-les-mises-a-jour": 1, "naviguer-en-securite": 2, "les-donnees-personnelles": 2, "le-cyberharcelement": 1, "vraie-ou-fausse-info": 2, "les-images-truquees-et-les-deepfakes": 2, "les-reseaux-sociaux-et-les-algorithmes": 2, "bien-utiliser-l-ia": 1, "comment-une-ia-ecrit": 3, "comment-marche-internet": 2, "les-octets-et-le-stockage": 1, "les-pixels-et-la-compression": 2, "programmer-pas-a-pas": 2, "le-temps-d-ecran-et-l-attention": 1, "les-achats-dans-les-jeux": 1,
}

BADGE_CSS = (".diff { font: 700 .72rem/1.2 var(--f-mono, monospace); padding: 2px 8px; border-radius: 99px; border: 1.5px solid; white-space: nowrap; }\n"
             ".diff.d1 { color: #15803d; border-color: #15803d; background: #dcf3e3; }\n"
             ".diff.d2 { color: #a15c07; border-color: #b45309; background: #fbe7cf; }\n"
             ".diff.d3 { color: #b91c1c; border-color: #b91c1c; background: #fde2e2; }\n"
             "@media (prefers-color-scheme: dark) { :root:not([data-theme=\"light\"]) .diff.d1 { color: #86efac; background: #14301f; border-color: #4ade80; }"
             " :root:not([data-theme=\"light\"]) .diff.d2 { color: #fcd34d; background: #3d2e08; border-color: #f5a35c; }"
             " :root:not([data-theme=\"light\"]) .diff.d3 { color: #fca5a5; background: #431a1a; border-color: #f87171; } }\n"
             ":root[data-theme=\"dark\"] .diff.d1 { color: #86efac; background: #14301f; border-color: #4ade80; }"
             " :root[data-theme=\"dark\"] .diff.d2 { color: #fcd34d; background: #3d2e08; border-color: #f5a35c; }"
             " :root[data-theme=\"dark\"] .diff.d3 { color: #fca5a5; background: #431a1a; border-color: #f87171; }\n")


def badge(page_id):
    d = DIFF.get(page_id)
    if not d:
        return ""
    return f'<span class="diff d{d}" title="Difficulté : {LABELS[d].lower()}">{LABELS[d]}</span>'


def apply_landings(root):
    """Ajoute (ou met à jour) le badge de difficulté sur les cartes des accueils."""
    for name in ("maths.html", "physique.html", "numerique.html", "religions.html", "geographie.html", "francais.html"):
        f = Path(root) / name
        if not f.exists():
            continue
        s = f.read_text(encoding="utf-8")
        s = re.sub(r'<span class="tags">(<span class="diff[^>]*>[^<]*</span>)?(<span class="lvl">.*?</span>)</span>', r"\2", s)

        def card(m):
            href, body = m.group(1), m.group(2)
            b = badge(href[:-5])
            if not b:
                return m.group(0)
            body = re.sub(r'(<span class="lvl">.*?</span>)', lambda x: '<span class="tags">' + b + x.group(1) + "</span>", body, count=1)
            return f'<a class="card" href="{href}">{body}'

        s = re.sub(r'<a class="card" href="([^"]+\.html)">(.*?)(?=</a>)', card, s, flags=re.S)
        css = "/*diff*/" + BADGE_CSS.replace("\n", " ") + "/*/diff*/\n" + \
              "/*diff2*/a.card .tags { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; justify-content: flex-end; }/*/diff2*/\n"
        s = re.sub(r"/\*diff\*/.*?/\*/diff\*/\n", "", s, flags=re.S)
        s = re.sub(r"/\*diff2\*/.*?/\*/diff2\*/\n", "", s, flags=re.S)
        s = s.replace("</style>", css + "</style>", 1)
        f.write_text(s, encoding="utf-8", newline="\n")
