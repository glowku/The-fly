"""Perception : Wikipedia REST API (gratuit, sans clé) + enrichissement."""
import requests
from urllib.parse import quote

HEADERS = {"User-Agent": "the-fly-agent/1.1 (knowledge-graph-builder; educational)"}
WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"
WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_RELATED = "https://en.wikipedia.org/api/rest_v1/page/related/{}"


def get_summary(title: str):
    """Résumé + métadonnées d'un article Wikipedia."""
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
        return {
            "title": data.get("title") or title,
            "extract": data.get("extract") or "",
            "description": data.get("description") or "",
            "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
            "thumbnail": (data.get("thumbnail") or {}).get("source"),
            "lang": data.get("lang", "en"),
        }
    except Exception as e:
        print(f"[perceive] summary error for {title}: {e}", flush=True)
        return None


def get_links(title: str, limit: int = 40):
    """Liens sortants d'un article Wikipedia (namespace 0)."""
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
    """Pages liées sémantiquement (REST related)."""
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
    """Catégories pour enrichir le contexte de planification."""
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
