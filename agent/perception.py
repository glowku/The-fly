"""Perception : Wikipedia REST API (gratuit, sans clé) + recherche de titres."""
import requests
from urllib.parse import quote

HEADERS = {"User-Agent": "the-fly-agent/1.2 (knowledge-graph-builder; educational)"}
WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_RELATED = "https://en.wikipedia.org/api/rest_v1/page/related/{}"


def search_titles(query: str, limit: int = 8) -> list:
    """Recherche Wikipedia (opensearch) → titres réels."""
    try:
        params = {
            "action": "opensearch",
            "search": query,
            "limit": limit,
            "namespace": 0,
            "format": "json",
        }
        r = requests.get(WIKI_API, params=params, timeout=15, headers=HEADERS)
        if r.status_code != 200:
            return []
        data = r.json()
        return list(data[1]) if len(data) > 1 else []
    except Exception as e:
        print(f"[perceive] search error: {e}", flush=True)
        return []


def get_summary(title: str):
    """Résumé + métadonnées d\'un article Wikipedia."""
    try:
        r = requests.get(
            WIKI_SUMMARY.format(quote(title, safe="")),
            timeout=20,
            headers=HEADERS,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        if data.get("type") in ("disambiguation", "https://mediawiki.org/wiki/Special:Redirect/new"):
            return None
        extract = data.get("extract") or ""
        if not extract.strip():
            return None
        return {
            "title": data.get("title") or title,
            "extract": extract,
            "description": data.get("description") or "",
            "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
            "thumbnail": (data.get("thumbnail") or {}).get("source"),
            "lang": data.get("lang", "en"),
        }
    except Exception as e:
        print(f"[perceive] summary error for {title}: {e}", flush=True)
        return None


def _score_hit(query: str, hit: str) -> float:
    """Score un hit Wikipedia vs la requête (plus haut = mieux)."""
    q = [w for w in query.lower().replace("-", " ").split() if len(w) > 1]
    h = hit.lower()
    if not q:
        return 0.0
    hits_w = sum(1 for w in q if w in h)
    ratio = hits_w / len(q)
    # bonus si le titre EST un des mots (ex: Fly)
    word_exact = 2.5 if h in q else 0.0
    # pénalité titres longs / composés bizarres
    pen = max(0, len(hit.split()) - 2) * 0.6
    exact = 4.0 if h == query.lower() else 0.0
    return ratio * 4.0 + hits_w + word_exact + exact - pen


def resolve_title(title: str):
    """Résout un titre flou vers une page Wikipedia réelle."""
    if not title or not title.strip():
        return None
    title = title.strip()

    s = get_summary(title)
    if s and (s.get("extract") or ""):
        return s.get("title") or title

    candidates = []
    # recherche full + par mot
    for q in [title] + [w for w in title.replace("-", " ").split() if len(w) > 2]:
        for h in search_titles(q, limit=6):
            candidates.append(h)

    # dédoublonne en gardant le meilleur score
    best_title = None
    best_score = -1.0
    seen = set()
    for h in candidates:
        if h in seen:
            continue
        seen.add(h)
        sc = _score_hit(title, h)
        if sc > best_score:
            # vérifier qu'un résumé existe
            s = get_summary(h)
            if s and len(s.get("extract") or "") > 80:
                best_score = sc
                best_title = s.get("title") or h

    if best_title and best_score >= 1.0:
        print(f"[perceive] resolve « {title} » → « {best_title} » (score={best_score:.1f})", flush=True)
        return best_title

    FALLBACKS = [
        ("fly", "Fly"),
        ("mouche", "Fly"),
        ("ecology", "Ecology"),
        ("ecologie", "Ecology"),
        ("insect", "Insect"),
        ("ai", "Artificial intelligence"),
        ("cybersecurity", "Computer security"),
        ("cyber", "Computer security"),
    ]
    low = title.lower()
    for k, v in FALLBACKS:
        if k in low:
            s = get_summary(v)
            if s:
                print(f"[perceive] fallback « {title} » → « {v} »", flush=True)
                return v
    return best_title


def get_links(title: str, limit: int = 40):
    try:
        params = {
            "action": "query",
            "titles": title,
            "prop": "links",
            "plnamespace": 0,
            "pllimit": min(limit, 50),
            "format": "json",
            "redirects": 1,
        }
        r = requests.get(WIKI_API, params=params, timeout=20, headers=HEADERS)
        if r.status_code != 200:
            return []
        pages = r.json().get("query", {}).get("pages", {})
        links = []
        for page in pages.values():
            for l in page.get("links", []):
                t = l.get("title")
                if t and not t.startswith(("Wikipedia:", "Help:", "Template:", "Category:", "File:")):
                    links.append(t)
        return links[:limit]
    except Exception as e:
        print(f"[perceive] links error for {title}: {e}", flush=True)
        return []


def get_related(title: str, limit: int = 15):
    try:
        r = requests.get(
            WIKI_RELATED.format(quote(title, safe="")),
            timeout=20,
            headers=HEADERS,
        )
        if r.status_code != 200:
            return []
        return [p.get("title") for p in r.json().get("pages", []) if p.get("title")][:limit]
    except Exception as e:
        print(f"[perceive] related error for {title}: {e}", flush=True)
        return []


def get_categories(title: str, limit: int = 10):
    try:
        params = {
            "action": "query",
            "titles": title,
            "prop": "categories",
            "cllimit": limit,
            "clshow": "!hidden",
            "format": "json",
            "redirects": 1,
        }
        r = requests.get(WIKI_API, params=params, timeout=15, headers=HEADERS)
        if r.status_code != 200:
            return []
        pages = r.json().get("query", {}).get("pages", {})
        cats = []
        for page in pages.values():
            for c in page.get("categories", []):
                title_c = c.get("title", "").replace("Category:", "")
                if title_c:
                    cats.append(title_c)
        return cats
    except Exception:
        return []
