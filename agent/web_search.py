"""Recherche web live pour questions d'actualité / temporelles.
Priorité : DuckDuckGo Instant + HTML lite, sans clé API.
"""
from __future__ import annotations

import re
import time
from typing import Any
from urllib.parse import quote_plus

import requests

HEADERS = {
    "User-Agent": "the-fly-agent/1.4 (knowledge-agent; educational research)",
    "Accept": "text/html,application/json",
    "Accept-Language": "fr,en;q=0.8",
}

# Signaux "besoin de live web"
TEMPORAL = re.compile(
    r"\b(aujourd.?hui|cette\s+semaine|cette\s+nuit|hier|maintenant|"
    r"actu(alité)?s?|news|breaking|en\s+ce\s+moment|"
    r"novembre\s+202[56]|2026|2025|"
    r"derniers?\s+(jours?|incidents?|breaches?|attaques?)|"
    r"récent|recent|latest|this\s+week|today)\b",
    re.I,
)
CYBER_NEWS = re.compile(
    r"\b(ransomware|data\s*breach|zero[- ]?day|cve-?20|"
    r"cyber\s*(attaque|attack|incident|security)|"
    r"exfiltration|leak\s*site|cisa\s*kev|"
    r"vulnérabilité|vulnerability)\b",
    re.I,
)


def needs_live_web(query: str) -> bool:
    q = (query or "").strip()
    if not q:
        return False
    if TEMPORAL.search(q):
        return True
    if CYBER_NEWS.search(q) and any(
        x in q.lower()
        for x in ("16", "17", "18", "19", "20", "novembre", "november", "semaine", "week", "aujourd", "today", "2026")
    ):
        return True
    # questions purement d'actualité
    if re.search(r"\b(quels?|quelles?|what|which).{0,40}(incidents?|attaques?|breaches?)\b", q, re.I):
        return True
    # sorties jeux / produits récents
    if re.search(r"\b(gta\s*6|gta\s*vi|grand theft auto\s*v?i?|sorti|sortie|release\s*date|est[- ]?il\s+sorti|when\s+did|when\s+does|out\s+now)\b", q, re.I):
        return True
    return False


def _ddg_instant(query: str, max_results: int = 8) -> list[dict[str, Any]]:
    """DuckDuckGo Instant Answer API (gratuit, sans clé)."""
    try:
        r = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            headers=HEADERS,
            timeout=12,
        )
        if r.status_code != 200:
            return []
        data = r.json()
        out: list[dict[str, Any]] = []
        if data.get("AbstractText"):
            out.append({
                "title": data.get("Heading") or query,
                "snippet": data.get("AbstractText", "")[:500],
                "url": data.get("AbstractURL") or "",
                "source": "ddg-abstract",
            })
        for t in (data.get("RelatedTopics") or [])[:max_results]:
            if isinstance(t, dict) and t.get("Text"):
                out.append({
                    "title": (t.get("Text") or "")[:120],
                    "snippet": t.get("Text", "")[:400],
                    "url": t.get("FirstURL") or "",
                    "source": "ddg-related",
                })
            elif isinstance(t, dict) and "Topics" in t:
                for st in t["Topics"][:3]:
                    if st.get("Text"):
                        out.append({
                            "title": (st.get("Text") or "")[:120],
                            "snippet": st.get("Text", "")[:400],
                            "url": st.get("FirstURL") or "",
                            "source": "ddg-related",
                        })
        return out[:max_results]
    except Exception as e:
        print(f"[web_search] ddg instant: {e}", flush=True)
        return []


def _ddg_html(query: str, max_results: int = 8) -> list[dict[str, Any]]:
    """Scraping léger de la page HTML DuckDuckGo (html.duckduckgo.com)."""
    try:
        r = requests.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers=HEADERS,
            timeout=15,
        )
        if r.status_code != 200:
            return []
        html = r.text
        results = []
        blocks = re.findall(
            r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?'
            r'class="result__snippet"[^>]*>(.*?)</(?:a|td|div)',
            html,
            re.S | re.I,
        )
        for url, title, snip in blocks[:max_results]:
            title = re.sub(r"<[^>]+>", "", title).strip()
            snip = re.sub(r"<[^>]+>", "", snip).strip()
            if title and len(title) > 5:
                results.append({
                    "title": title[:200],
                    "snippet": snip[:400],
                    "url": url,
                    "source": "ddg-html",
                })
        if results:
            return results
        links = re.findall(r'uddg=([^&"]+).*?class="result__a"[^>]*>(.*?)</a>', html, re.S)
        for url_enc, title in links[:max_results]:
            from urllib.parse import unquote
            title = re.sub(r"<[^>]+>", "", title).strip()
            results.append({
                "title": title[:200],
                "snippet": "",
                "url": unquote(url_enc),
                "source": "ddg-html",
            })
        return results[:max_results]
    except Exception as e:
        print(f"[web_search] ddg html: {e}", flush=True)
        return []


def search_web(query: str, max_results: int = 8) -> list[dict[str, Any]]:
    """Recherche web multi-source, dédupliquée."""
    q = (query or "").strip()
    if not q:
        return []
    if CYBER_NEWS.search(q) and "2026" not in q:
        q = q + " 2026"
    seen_urls: set[str] = set()
    out: list[dict[str, Any]] = []
    for fn in (_ddg_instant, _ddg_html):
        try:
            hits = fn(q, max_results=max_results)
        except Exception:
            hits = []
        for h in hits:
            u = (h.get("url") or "").split("?")[0]
            if u and u in seen_urls:
                continue
            if u:
                seen_urls.add(u)
            if h.get("title") or h.get("snippet"):
                out.append(h)
            if len(out) >= max_results:
                return out
        time.sleep(0.15)
    return out


def format_web_context(hits: list[dict[str, Any]], limit: int = 6) -> str:
    if not hits:
        return ""
    lines = []
    for i, h in enumerate(hits[:limit], 1):
        title = h.get("title") or "sans titre"
        snip = (h.get("snippet") or "").replace("\n", " ").strip()
        url = h.get("url") or ""
        lines.append(f"[{i}] {title}\n    {snip}\n    {url}")
    return "\n".join(lines)
