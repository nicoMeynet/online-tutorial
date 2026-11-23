"""Date de dernière mise à jour + copyright en bas de chaque page (appelé par liens.py).

La date d'une page ne change que si son CONTENU change : on compare une empreinte du texte sans les
parties générées (navigation, liens, badges, bouton Partager, cette ligne). Les empreintes et les dates
sont gardées dans tools/dates.json. Pour une page inconnue, on remonte l'historique git pour retrouver
depuis quand son contenu est le même. Les accueils prennent la date la plus récente de leurs tutoriels.
"""
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "tools" / "dates.json"
OWNER = "© 2026 Nicolas Meynet"
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
STAMP = re.compile(r"<!--tmaj-->.*?<!--/tmaj-->", re.S)


def norm(src):
    s = re.sub(r"<!--tnav-->.*?<!--/tnav-->", "", src, flags=re.S)
    s = re.sub(r"<!--ticons-->.*?<!--/ticons-->", "", s, flags=re.S)
    s = re.sub(r'<style id="tnav-css">.*?</style>', "", s, flags=re.S)
    s = STAMP.sub("", s)
    s = re.sub(r'<a class="tlink" href="[^"]*">(.*?)</a>', r"\1", s, flags=re.S)
    s = re.sub(r'<span class="diff d\d"[^>]*>[^<]*</span>', "", s)
    s = re.sub(r"/\*diff2?\*/.*?/\*/diff2?\*/", "", s, flags=re.S)
    s = re.sub(r'<span class="tags">|<button type="button" data-share hidden>Partager</button>', "", s)
    s = s.replace(OWNER, "")
    return re.sub(r"\s+", "", s)


def digest(src):
    return hashlib.sha1(norm(src).encode("utf-8")).hexdigest()[:16]


def from_git(name, h):
    """Date du plus ancien commit d'une suite continue de versions de même contenu que maintenant."""
    try:
        log = subprocess.run(["git", "log", "--format=%H %cs", "--", name], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.split("\n")
    except OSError:
        return None
    date = None
    for line in filter(None, log):
        sha, d = line.split()
        old = subprocess.run(["git", "show", f"{sha}:{name}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
        if not old or digest(old) != h:
            break
        date = d
    return date


def fr(d):
    y, m, j = map(int, d.split("-"))
    return f"{'1er' if j == 1 else j} {MOIS[m - 1]} {y}"


def stamp_html(d):
    return ('<!--tmaj--><span class="tmaj" style="display:block;margin-top:6px;font-size:.85rem;opacity:.85">'
            f'Dernière mise à jour : {fr(d)} · {OWNER}</span><!--/tmaj-->')


def put(src, d):
    src = STAMP.sub("", src)
    end = src.rfind("</footer>")
    if end < 0:
        return src
    start = src.rfind("<footer", 0, end)
    inner = src[start:end]
    # le copyright est maintenant dans la ligne de date : on l'enlève ailleurs dans le pied de page
    inner = re.sub(r"\s*·?\s*" + re.escape(OWNER), "", inner)
    return src[:start] + inner + stamp_html(d) + src[end:]


class Dates:
    def __init__(self):
        self.data = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
        self.today = datetime.date.today().isoformat()

    def page(self, name, src):
        """Date de la page (mise à jour si son contenu a changé)."""
        h = digest(src)
        e = self.data.get(name)
        if not e or e["h"] != h:
            d = (from_git(name, h) if not e else None) or self.today
            e = self.data[name] = {"h": h, "d": d}
        return e["d"]

    def save(self):
        STORE.write_text(json.dumps(dict(sorted(self.data.items())), ensure_ascii=False, indent=0) + "\n", encoding="utf-8", newline="\n")
