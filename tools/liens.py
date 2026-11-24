"""Ajoute la navigation entre tutoriels dans les pages du dépôt.

- un lien « ← Tous les tutoriels » en haut de chaque page ;
- les mentions « le tutoriel sur … » deviennent de vrais liens ;
- en bas de page : tutoriel précédent / suivant (ordre des accueils de matière) et retour à l'accueil.

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
import maj  # noqa: E402

DATES = maj.Dates()

ROOT = Path(__file__).resolve().parent.parent

TOPICS = [
    ("la ponctuation", "la-ponctuation.html"),
    ("l'orthographe", "l-orthographe.html"),
    ("l’orthographe", "l-orthographe.html"),
    ("la grammaire", "la-grammaire.html"),
    ("la grammaire de la phrase", "la-grammaire.html"),
    ("la conjugaison", "la-conjugaison.html"),
    ("la langue française", "la-langue-francaise.html"),
    ("l'histoire de la Suisse", "l-histoire-de-la-suisse.html"),
    ("l’histoire de la Suisse", "l-histoire-de-la-suisse.html"),
    ("la géographie de la Suisse", "la-geographie-de-la-suisse.html"),
    ("la géographie du monde", "la-geographie-du-monde.html"),
    ("les pays et les capitales", "la-geographie-du-monde.html"),
    ("la politique suisse", "la-politique-suisse.html"),
    ("la démocratie suisse", "la-politique-suisse.html"),
    ("le sikhisme", "le-sikhisme.html"),
    ("les religions traditionnelles", "les-religions-traditionnelles.html"),
    ("les conversions avancées", "les-conversions-avancees.html"),
    ("les religions du monde", "les-religions-du-monde.html"),
    ("les religions", "les-religions-du-monde.html"),
    ("l'hindouisme", "l-hindouisme.html"),
    ("l’hindouisme", "l-hindouisme.html"),
    ("le bouddhisme", "le-bouddhisme.html"),
    ("le judaïsme", "le-judaisme.html"),
    ("le christianisme", "le-christianisme.html"),
    ("l'islam", "l-islam.html"),
    ("l’islam", "l-islam.html"),
    ("les sagesses de Chine et du Japon", "les-sagesses-de-chine-et-du-japon.html"),
    ("le taoïsme", "les-sagesses-de-chine-et-du-japon.html"),
    ("le shintoïsme", "les-sagesses-de-chine-et-du-japon.html"),
    ("les mythologies antiques", "les-mythologies-antiques.html"),
    ("les mythologies", "les-mythologies-antiques.html"),
    ("les fêtes et calendriers", "les-fetes-et-calendriers.html"),
    ("les fêtes religieuses", "les-fetes-et-calendriers.html"),
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
    ("vraie ou fausse info", "vraie-ou-fausse-info.html"),
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
         '<script src="progress.js" defer></script><script src="share.js" defer></script><!--/ticons-->\n')

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
.tnav-top [data-share] { margin-left: auto; }
.tnav-short { display: none; }
.tprint-h { display: none; }
@media (max-width: 600px) { header.hero { gap: 8px !important; } header.hero > .fig, header.hero > .box.fig, header.hero .hero-top .fig { display: none !important; }
  header.hero p.lead { font-size: 1rem !important; line-height: 1.5 !important; } header.hero > p.soft { font-size: .88rem !important; line-height: 1.45 !important; }
  header.hero h1 { font-size: clamp(1.7rem, 8vw, 2.2rem) !important; } }
.tprint-row { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; margin: 14px 0 0; }
.tprint-row span { font-size: .9rem; opacity: .8; }
.tprint { display: inline-flex; align-items: center; gap: 8px; min-height: 42px; padding: 8px 16px; border: 2px solid var(--ink, #222); border-radius: 999px;
  background: var(--card, #fff); color: var(--ink, #222); font: inherit; font-weight: 700; cursor: pointer; box-shadow: 2px 2px 0 var(--ink, #222); }
.tprint:hover, .tprint:focus-visible { transform: translate(-1px, -1px); box-shadow: 3px 3px 0 var(--ink, #222); }
@media print { [data-tp-hide] { display: none !important; } html.tp-on, html.tp-on body { background: #fff !important; color: #111 !important; padding: 0 !important; margin: 0 !important; }
  html.tp-on [data-fiche] { color: #111; } html.tp-on [data-fiche] * { color: #111 !important; background: transparent !important; box-shadow: none !important; }
  html.tp-on .tprint-h { display: block; font-size: 1.4rem; font-weight: 800; margin: 0 0 10px; } .tprint-row { display: none !important; } }
@media (max-width: 520px) { .tnav-top .tnav-long { display: none; } .tnav-top .tnav-short { display: inline; } .tnav-top { flex-wrap: nowrap; } .tnav-top > * { flex: none; } }
.tnav-end { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; }
@media (max-width: 520px) { .tnav-pn { grid-template-columns: 1fr; } .tnav-pn a.next { grid-column: 1; } }
</style>
"""
CSS = CSS.replace("</style>", difficulte.BADGE_CSS + "</style>", 1)


# Une page d'accueil par matière : chaque tutoriel renvoie vers la sienne,
# et « précédent / suivant » reste dans la même matière.
LANDINGS = [("maths.html", "Tous les tutoriels de maths"), ("physique.html", "Tous les tutoriels de physique"), ("numerique.html", "Tous les tutoriels numériques"), ("religions.html", "Tous les tutoriels de religions"), ("geographie.html", "Tous les tutoriels d'histoire-géo"), ("francais.html", "Tous les tutoriels de français")]
# Pages de révision qui ne sont pas des cartes mais appartiennent à une matière.
SHORT = {"index.html": "Accueil", "maths.html": "Maths", "physique.html": "Physique-chimie", "numerique.html": "Numérique", "religions.html": "Religions", "geographie.html": "Histoire-géo", "francais.html": "Français"}
HOME_OF = {"maths.html": ("glossaire.html", "revisions-brevet.html"), "physique.html": ("glossaire-physique.html", "revisions-brevet-physique.html")}


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


FICHE = re.compile(r"<!--tprint-->.*?<!--/tprint-->\n?", re.S)


def fiche(src):
    """Bouton « Imprimer la fiche » à la fin de la section « À retenir » (inverse exact : FICHE.sub)."""
    src = FICHE.sub("", src).replace(" data-fiche>", ">")
    m = re.search(r'<section([^>]*)>(\s*<span class="eyebrow">À retenir)', src)
    if not m:
        return src
    end = src.index("</section>", m.end())
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S)
    title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else ""
    head = (f'<!--tprint--><p class="tprint-h">Fiche de révision · {title}</p><!--/tprint-->')
    btn = ('<!--tprint--><p class="tprint-row"><button type="button" class="tprint" data-print>'
           '<span aria-hidden="true">🖨</span> Imprimer la fiche</button>'
           '<span>Seulement ce résumé, sur une page.</span></p><!--/tprint-->\n')
    src = src[:end] + btn + src[end:]
    src = src[:m.start()] + f"<section{m.group(1)} data-fiche>" + head + m.group(2) + src[m.end():]
    return src


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

    home, label, seq = "index.html", "Accueil", []
    for landing, lab, cards in order:
        if path.name in HOME_OF.get(landing, ()):
            home, label = landing, lab
        if any(h == path.name for h, _ in cards):
            home, label, seq = landing, lab, cards
    names = [h for h, _ in seq]
    titles = dict(seq)
    top = (f'<!--tnav--><nav class="tnav-top" aria-label="Navigation"><a class="tnav-home" href="{home}">← <span class="tnav-long">{label}</span><span class="tnav-short">{SHORT.get(home, label)}</span></a>'
           f'{difficulte.badge(path.stem)}<button type="button" data-share hidden>Partager</button></nav><!--/tnav-->\n')
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
                  f'<div class="tnav-end"><a class="tnav-home" href="{home}">⌂ {label}</a><button type="button" data-share hidden>Partager</button></div></nav><!--/tnav-->\n')

    src = src.replace('<main class="page">', '<main class="page">\n' + top, 1)
    end = src.index("</main>")
    foot = src.rfind("<footer", 0, end)
    at = foot if foot > src.index('<main class="page">') else end
    src = src[:at] + bottom + src[at:]
    src = src.replace("</head>", ICONS + CSS + "</head>", 1)
    src = fiche(src)
    src = maj.put(src, DATES.page(path.name, src))
    path.write_text(src, encoding="utf-8", newline="\n")


def main():
    difficulte.apply_landings(ROOT)
    order = landing_order()
    files = [ROOT / a for a in sys.argv[1:]] or sorted(p for p in ROOT.glob("*.html") if p.name not in dict(LANDINGS) and p.name not in ("index.html", "a-propos.html"))
    for p in files:
        process(p, order)
        print("ok", p.name)
    # accueils : date la plus récente parmi leurs tutoriels (et leur propre contenu)
    alld = []
    for landing, _, cards in order:
        f = ROOT / landing
        src = f.read_text(encoding="utf-8")
        ds = [DATES.page(landing, src)] + [DATES.data[h]["d"] for h, _ in cards if h in DATES.data]
        alld += ds
        f.write_text(maj.put(src, max(ds)), encoding="utf-8", newline="\n")
    for name in ("index.html", "a-propos.html"):
        idx = ROOT / name
        if idx.exists():
            src = idx.read_text(encoding="utf-8")
            idx.write_text(maj.put(src, max(alld + [DATES.page(name, src)])), encoding="utf-8", newline="\n")
    DATES.save()


if __name__ == "__main__":
    main()
