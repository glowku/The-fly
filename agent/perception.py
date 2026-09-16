"""Perception : Wikipedia + recherche multi-mots intelligente."""
import requests
from urllib.parse import quote
from itertools import combinations

HEADERS = {"User-Agent": "the-fly-agent/1.3 (knowledge-graph-builder; educational)"}
WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_RELATED = "https://en.wikipedia.org/api/rest_v1/page/related/{}"


def search_titles(query: str, limit: int = 8) -> list:
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


def multi_search(query: str, limit_per: int = 5) -> list:
    """
    Recherche intelligente multi-mots.
    Ex: "la mouche evolution" → queries:
      - full phrase
      - bigrams: "mouche evolution", "la mouche"
      - unigrams significatifs
    """
    stop = {"la", "le", "les", "de", "des", "du", "un", "une", "the", "a", "an", "of", "and", "et", "or", "sur", "pour"}
    raw = query.replace("-", " ").strip()
    words = [w for w in raw.split() if w.lower() not in stop and len(w) > 1]
    queries = []
    if raw:
        queries.append(raw)
    # bigrams / trigrams
    for n in (3, 2):
        if len(words) >= n:
            for i in range(len(words) - n + 1):
                queries.append(" ".join(words[i:i+n]))
    # single words (longest first)
    for w in sorted(words, key=len, reverse=True):
        queries.append(w)

    seen = set()
    results = []
    for q in queries:
        ql = q.lower()
        if ql in seen:
            continue
        seen.add(ql)
        for h in search_titles(q, limit=limit_per):
            if h not in results:
                results.append(h)
        if len(results) >= 20:
            break
    return results


def get_summary(title: str):
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
    q = [w for w in query.lower().replace("-", " ").split() if len(w) > 1]
    h = hit.lower()
    if not q:
        return 0.0
    hits_w = sum(1 for w in q if w in h)
    ratio = hits_w / len(q)
    word_exact = 2.5 if h in q else 0.0
    pen = max(0, len(hit.split()) - 2) * 0.6
    exact = 4.0 if h == query.lower() else 0.0
    return ratio * 4.0 + hits_w + word_exact + exact - pen


def resolve_title(title: str):
    if not title or not title.strip():
        return None
    title = title.strip()

    s = get_summary(title)
    if s and (s.get("extract") or ""):
        return s.get("title") or title

    candidates = multi_search(title, limit_per=6)
    best_title = None
    best_score = -1.0
    for h in candidates:
        sc = _score_hit(title, h)
        if sc <= best_score:
            continue
        s = get_summary(h)
        if s and len(s.get("extract") or "") > 80:
            best_score = sc
            best_title = s.get("title") or h

    if best_title and best_score >= 1.0:
        print(f"[perceive] resolve « {title} » → « {best_title} » (score={best_score:.1f})", flush=True)
        return best_title

    FALLBACKS = [
        ("fly", "Fly"), ("mouche", "Fly"), ("ecology", "Ecology"),
        ("ecologie", "Ecology"), ("insect", "Insect"),
        ("ai", "Artificial intelligence"),
        ("cybersecurity", "Computer security"), ("cyber", "Computer security"),
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
            "action": "query", "titles": title, "prop": "links",
            "plnamespace": 0, "pllimit": min(limit, 50),
            "format": "json", "redirects": 1,
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
        r = requests.get(WIKI_RELATED.format(quote(title, safe="")), timeout=20, headers=HEADERS)
        if r.status_code != 200:
            return []
        return [p.get("title") for p in r.json().get("pages", []) if p.get("title")][:limit]
    except Exception as e:
        print(f"[perceive] related error for {title}: {e}", flush=True)
        return []


def get_categories(title: str, limit: int = 10):
    try:
        params = {
            "action": "query", "titles": title, "prop": "categories",
            "cllimit": limit, "clshow": "!hidden", "format": "json", "redirects": 1,
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
