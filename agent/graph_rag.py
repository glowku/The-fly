"""
Graph-RAG : interroge le noyau wiki The-fly (+ option arXiv) via Groq.
Réponses grounded uniquement sur le contexte récupéré.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import requests

from .memory import load_coverage, load_quality
from .skills import score_relevance
from .arxiv_source import search_domain, format_arxiv_context

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
WIKI_DIR = Path("wiki")


def _tokenize(q: str) -> list[str]:
    return [w for w in re.split(r"[^a-zA-Z0-9àâäéèêëïîôùûüç]+", (q or "").lower()) if len(w) > 2]


def _score_doc(query: str, title: str, text: str) -> float:
    words = _tokenize(query)
    if not words:
        return 0.0
    blob = f"{title} {text[:2000]}".lower()
    hits = sum(1 for w in words if w in blob)
    title_hits = sum(1 for w in words if w in title.lower())
    rel = score_relevance(title, text[:400])
    return hits * 1.2 + title_hits * 2.5 + rel * 3.0


def list_wiki_titles() -> list[str]:
    if not WIKI_DIR.exists():
        return list(load_coverage().get("nodes", {}).keys())
    return sorted(p.stem for p in WIKI_DIR.glob("*.md"))


def read_article(title: str) -> str | None:
    path = WIKI_DIR / f"{title}.md"
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    # fuzzy
    for p in WIKI_DIR.glob("*.md"):
        if p.stem.lower() == title.lower():
            return p.read_text(encoding="utf-8", errors="ignore")
    return None


def retrieve(query: str, k: int = 6) -> list[dict]:
    """Top-k articles wiki pertinents."""
    cov = load_coverage()
    qual = load_quality()
    titles = list(dict.fromkeys(list(cov.get("nodes", {}).keys()) + list_wiki_titles()))
    scored = []
    for title in titles:
        text = read_article(title) or ""
        if not text and title not in qual:
            continue
        sc = _score_doc(query, title, text)
        if sc <= 0 and score_relevance(title) < 0.25:
            continue
        scored.append(
            {
                "title": title,
                "score": round(sc, 3),
                "quality": (qual.get(title) or {}).get("score"),
                "text": (text or "")[:1800],
                "depth": (cov.get("nodes", {}).get(title) or {}).get("depth"),
            }
        )
    scored.sort(key=lambda x: (x["score"], x.get("quality") or 0), reverse=True)
    return [x for x in scored if x["score"] > 0 or x.get("text")][:k]


def answer(
    query: str,
    k: int = 6,
    use_arxiv: bool = True,
    temperature: float = 0.2,
) -> dict:
    """
    Réponse Graph-RAG.
    return {answer, sources, arxiv, model, mode}
    """
    docs = retrieve(query, k=k)
    papers = search_domain(query, max_results=4) if use_arxiv else []
    # filtre papers hors sujet grossier
    papers = [
        p
        for p in papers
        if score_relevance(p.get("title", ""), p.get("summary", "")) >= 0.15
        or any(
            t in (p.get("summary") or "").lower()
            for t in ("insect", "drosophila", "diptera", "fly ", "flight", "wing")
        )
    ][:4]

    sources = [d["title"] for d in docs]
    ctx_wiki = "\n\n".join(
        f"### {d['title']} (q={d.get('quality')}, depth={d.get('depth')})\n{d['text']}"
        for d in docs
    )
    ctx_arxiv = format_arxiv_context(papers) if papers else ""

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        # mode extractif
        bits = []
        for d in docs[:4]:
            lines = [ln for ln in d["text"].splitlines() if ln.strip() and not ln.startswith("#")]
            bits.append(f"• {d['title']}: {' '.join(lines[:3])[:350]}")
        extract = "\n".join(bits) if bits else "Aucun article wiki pertinent."
        if papers:
            extract += "\n\narXiv:\n" + "\n".join(f"- {p['title']}" for p in papers[:3])
        return {
            "answer": extract,
            "sources": sources,
            "arxiv": papers,
            "model": None,
            "mode": "extractive",
        }

    prompt = f"""Tu es le moteur de langage de The-fly (graphe de connaissance vivant sur insectes / diptères / vol / évolution).
Réponds en français, de façon précise et concise (120–250 mots).
Règles STRICTES :
1. Utilise UNIQUEMENT le contexte wiki (et arXiv si fourni).
2. N'invente aucun fait.
3. Si le contexte est insuffisant, dis-le clairement.
4. Cite les titres sources en fin de réponse.

Question: {query}

=== CONTEXTE WIKI (noyau appris) ===
{ctx_wiki[:7000] if ctx_wiki else "(vide)"}

=== CONTEXTE ARXIV (recherche) ===
{ctx_arxiv[:2500] if ctx_arxiv else "(aucun)"}
"""

    try:
        r = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": 900,
            },
            timeout=90,
        )
        if r.status_code != 200:
            return {
                "answer": f"[Groq HTTP {r.status_code}] fallback extractif\n"
                + (ctx_wiki[:1500] or "pas de contexte"),
                "sources": sources,
                "arxiv": papers,
                "model": MODEL,
                "mode": "error_fallback",
            }
        text = r.json()["choices"][0]["message"]["content"].strip()
        return {
            "answer": text,
            "sources": sources,
            "arxiv": papers,
            "model": MODEL,
            "mode": "llm",
        }
    except Exception as e:
        return {
            "answer": f"[erreur LLM: {e}]",
            "sources": sources,
            "arxiv": papers,
            "model": MODEL,
            "mode": "error",
        }


def verify_claim(claim: str, k: int = 5) -> dict:
    """Vérifie une affirmation contre le noyau wiki (+ arXiv)."""
    q = f"Vérification factuelle: {claim}"
    res = answer(
        q
        + "\nRéponds par SOUTENU / PARTIEL / NON_SOUTENU puis justification courte.",
        k=k,
        use_arxiv=True,
        temperature=0.1,
    )
    res["claim"] = claim
    return res
