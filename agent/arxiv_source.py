"""Source arXiv : recherche papiers + extraction concepts (sans dépendance extra)."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

import requests

from .skills import score_relevance, is_hard_junk

HEADERS = {
    "User-Agent": "the-fly-agent/1.4 (knowledge-graph; educational; +https://github.com/glowku/The-fly)"
}
ARXIV_API = "http://export.arxiv.org/api/query"

# Domaine scientifique utile pour The-fly
DOMAIN_CATS = (
    "q-bio.NC",  # neurons / cognition (flight control)
    "q-bio.PE",  # populations / evolution
    "q-bio.QM",
    "physics.bio-ph",
    "cs.RO",  # bio-inspired flight / robotics
)


def search_arxiv(
    query: str,
    max_results: int = 8,
    cats: tuple[str, ...] | None = None,
) -> list[dict]:
    """
    Recherche arXiv. Retourne [{id, title, summary, authors, published, url, primary_category}].
    """
    q = (query or "").strip()
    if not q:
        return []

    # Ancrer un peu le domaine si la query est trop large
    search = q
    if cats:
        cat_clause = " OR ".join(f"cat:{c}" for c in cats)
        search = f"({q}) AND ({cat_clause})"

    params = {
        "search_query": search if ":" in search or "AND" in search else f"all:{q}",
        "start": 0,
        "max_results": max(1, min(max_results, 15)),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    try:
        r = requests.get(ARXIV_API, params=params, timeout=25, headers=HEADERS)
        if r.status_code != 200:
            print(f"[arxiv] HTTP {r.status_code}", flush=True)
            return []
        return _parse_atom(r.text)
    except Exception as e:
        print(f"[arxiv] error: {e}", flush=True)
        return []


def search_domain(topic: str, max_results: int = 6) -> list[dict]:
    """Recherche orientée insectes / vol / evolution."""
    topic = (topic or "insect flight").strip()
    # Deux passes : full-text puis catégories bio
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
        eid = (entry.findtext("a:id", default="", namespaces=ns) or "").strip()
        title = re.sub(r"\s+", " ", (entry.findtext("a:title", default="", namespaces=ns) or "").strip())
        summary = re.sub(r"\s+", " ", (entry.findtext("a:summary", default="", namespaces=ns) or "").strip())
        published = (entry.findtext("a:published", default="", namespaces=ns) or "")[:10]
        authors = [
            (a.findtext("a:name", default="", namespaces=ns) or "").strip()
            for a in entry.findall("a:author", ns)
        ]
        primary = entry.find("arxiv:primary_category", ns)
        cat = primary.get("term") if primary is not None else ""
        abs_url = eid
        for link in entry.findall("a:link", ns):
            if link.get("type") == "text/html" or link.get("rel") == "alternate":
                abs_url = link.get("href") or abs_url
                break
        if not title:
            continue
        out.append(
            {
                "id": eid.split("/abs/")[-1] if "/abs/" in eid else eid,
                "title": title,
                "summary": summary[:1200],
                "authors": [a for a in authors if a][:8],
                "published": published,
                "url": abs_url,
                "primary_category": cat,
            }
        )
    return out


def concepts_from_papers(papers: list[dict], min_relevance: float = 0.32) -> list[str]:
    """
    Extrait des titres-concepts candidats (pour frontier) filtrés anti-dérive.
    On garde des phrases courtes issues des titres de papiers.
    """
    candidates = []
    for p in papers:
        title = p.get("title") or ""
        # Nettoyer titres académiques trop longs → garder noyau
        clean = re.sub(r"[:：].*$", "", title).strip()
        clean = re.sub(r"\s+", " ", clean)
        if len(clean) < 4 or len(clean) > 80:
            continue
        if is_hard_junk(clean, p.get("summary") or ""):
            continue
        rel = score_relevance(clean, p.get("summary") or "")
        if rel < min_relevance:
            # second chance: tokens insecte dans abstract
            abs_l = (p.get("summary") or "").lower()
            if not any(
                t in abs_l
                for t in (
                    "insect",
                    "fly",
                    "diptera",
                    "drosophila",
                    "mosquito",
                    "wing",
                    "flight",
                    "haltere",
                    "larva",
                )
            ):
                continue
        candidates.append(clean)
    # dédoublonnage
    seen = set()
    uniq = []
    for c in candidates:
        k = re.sub(r"[^a-z0-9]+", "", c.lower())
        if k in seen:
            continue
        seen.add(k)
        uniq.append(c)
    return uniq


def format_arxiv_context(papers: list[dict], limit: int = 4) -> str:
    """Bloc texte pour injection synthèse / Graph-RAG."""
    blocks = []
    for p in papers[:limit]:
        authors = ", ".join(p.get("authors") or [])[:80]
        blocks.append(
            f"- {p.get('title')} ({p.get('published')}, {p.get('primary_category')})\n"
            f"  {authors}\n"
            f"  {(p.get('summary') or '')[:400]}\n"
            f"  {p.get('url')}"
        )
    return "\n".join(blocks)
