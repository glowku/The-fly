"""Source arXiv : recherche papiers + extraction concepts."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET

import requests

from .skills import score_relevance, is_hard_junk

HEADERS = {
    "User-Agent": "the-fly-agent/1.5 (knowledge-graph; educational; +https://github.com/glowku/The-fly)"
}
ARXIV_API = "http://export.arxiv.org/api/query"

DOMAIN_CATS = (
    "q-bio.NC",
    "q-bio.PE",
    "q-bio.QM",
    "physics.bio-ph",
    "cs.RO",
)


def search_arxiv(
    query: str,
    max_results: int = 8,
    cats: tuple[str, ...] | None = None,
) -> list[dict]:
    q = (query or "").strip()
    if not q:
        return []

    search = q
    if cats:
        cat_clause = " OR ".join(f"cat:{c}" for c in cats)
        search = f"({q}) AND ({cat_clause})"

    # API arXiv: all: pour fulltext simple
    if "cat:" not in search and "AND" not in search:
        search_query = f"all:{q}"
    else:
        # mix: all:query AND (cat:...)
        if cats and "cat:" in search:
            search_query = f"all:{q} AND ({' OR '.join(f'cat:{c}' for c in cats)})"
        else:
            search_query = search

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max(1, min(max_results, 15)),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    try:
        r = requests.get(ARXIV_API, params=params, timeout=30, headers=HEADERS)
        if r.status_code != 200:
            print(f"[arxiv] HTTP {r.status_code}", flush=True)
            return []
        return _parse_atom(r.text)
    except Exception as e:
        print(f"[arxiv] error: {e}", flush=True)
        return []


def search_domain(topic: str, max_results: int = 6) -> list[dict]:
    topic = (topic or "insect flight").strip()
    hits = search_arxiv(topic, max_results=max_results)
    if len(hits) < 3:
        hits2 = search_arxiv(topic, max_results=max_results, cats=DOMAIN_CATS)
        seen = {h["id"] for h in hits}
        for h in hits2:
            if h["id"] not in seen:
                hits.append(h)
    return hits[:max_results]


def _parse_atom(xml_text: str) -> list[dict]:
    ns = {
        "a": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(xml_text)
    out = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
        title = re.sub(r"\s+", " ", title)
        summary = (entry.findtext("a:summary", default="", namespaces=ns) or "").strip()
        summary = re.sub(r"\s+", " ", summary)
        eid = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
        published = (entry.findtext("a:published", default="", namespaces=ns) or "")[:10]
        authors = [
            (a.findtext("a:name", default="", namespaces=ns) or "").strip()
            for a in entry.findall("a:author", ns)
        ]
        primary = entry.find("arxiv:primary_category", ns)
        cat = primary.get("term") if primary is not None else ""
        abs_url = eid
        for link in entry.findall("a:link", ns):
            if link.get("rel") == "alternate" or link.get("type") == "text/html":
                abs_url = link.get("href") or abs_url
                break
        if not title:
            continue
        out.append(
            {
                "id": eid,
                "title": title,
                "summary": summary,
                "authors": authors,
                "published": published,
                "url": abs_url,
                "primary_category": cat,
            }
        )
    return out


def format_arxiv_context(papers: list[dict]) -> str:
    if not papers:
        return ""
    blocks = []
    for p in papers:
        blocks.append(
            f"### {p.get('title')} ({p.get('primary_category', '')})\n"
            f"{p.get('summary', '')[:800]}\n"
            f"URL: {p.get('url', '')}"
        )
    return "\n\n".join(blocks)


def concepts_from_papers(papers: list[dict], min_relevance: float = 0.25) -> list[str]:
    """Extraire des titres / concepts filtrés depuis abstracts."""
    concepts = []
    for p in papers:
        title = p.get("title") or ""
        if is_hard_junk(title):
            continue
        if score_relevance(title, p.get("summary") or "") >= min_relevance or True:
            # pour bio on filtre plus ; pour tech on garde le titre papier
            concepts.append(title)
    return concepts[:12]
