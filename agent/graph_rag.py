"""
Graph-RAG : interroge le noyau wiki The-fly (+ option arXiv) via Groq.
Persona : raisonner comme une mouche savante — domaine insecte/diptère only.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import requests

from .memory import load_coverage, load_quality
from .skills import score_relevance, is_hard_junk, is_domain_node
from .arxiv_source import search_domain, format_arxiv_context

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
WIKI_DIR = Path("wiki")

FR_EXPAND = {
    "vol": ["flight", "insect flight", "wing", "haltere", "hover"],
    "vole": ["flight", "fly", "wing", "hover"],
    "voler": ["flight", "fly", "wing"],
    "mouche": ["fly", "housefly", "diptera", "musca", "drosophila"],
    "mouches": ["fly", "flies", "diptera"],
    "mange": ["feeding", "mouthpart", "proboscis", "foraging", "maggot", "diet"],
    "manger": ["feeding", "mouthpart", "foraging"],
    "alimentation": ["feeding", "foraging", "mouthpart", "proboscis"],
    "aile": ["wing", "haltere", "insect wing"],
    "ailes": ["wing", "haltere"],
    "yeux": ["compound eye", "arthropod eye"],
    "oeil": ["compound eye"],
    "œil": ["compound eye"],
    "larve": ["larva", "maggot"],
    "insecte": ["insect", "entomology", "arthropod"],
}

GREETING = re.compile(
    r"^(salut|hello|hi|hey|bonjour|bonsoir|ça\s*va|ca\s*va|comment\s+tu\s+vas|"
    r"comment\s+allez|who\s+are\s+you|qui\s+es[- ]tu|présente)\b",
    re.I,
)


def _tokenize(q: str) -> list[str]:
    words = [w for w in re.split(r"[^a-zA-Z0-9àâäéèêëïîôùûüç]+", (q or "").lower()) if len(w) > 2]
    out = list(words)
    for w in words:
        out.extend(FR_EXPAND.get(w, []))
    # dédoublonne en gardant l'ordre
    seen = set()
    uniq = []
    for w in out:
        wl = w.lower()
        if wl not in seen:
            seen.add(wl)
            uniq.append(wl)
    return uniq


def _score_doc(query: str, title: str, text: str) -> float:
    if is_hard_junk(title, text[:300]):
        return -1.0
    rel = score_relevance(title, text[:400])
    if rel < 0.30:
        return -1.0
    words = _tokenize(query)
    if not words:
        return rel
    blob = f"{title} {text[:2000]}".lower()
    hits = sum(1 for w in words if w in blob)
    title_hits = sum(1 for w in words if w in title.lower())
    return hits * 1.4 + title_hits * 3.0 + rel * 4.0


def list_wiki_titles() -> list[str]:
    if not WIKI_DIR.exists():
        return list(load_coverage().get("nodes", {}).keys())
    return sorted(p.stem for p in WIKI_DIR.glob("*.md"))


def read_article(title: str) -> str | None:
    path = WIKI_DIR / f"{title}.md"
    if path.exists():
        return path.read_text(encoding="utf-8", errors="ignore")
    for p in WIKI_DIR.glob("*.md"):
        if p.stem.lower() == title.lower():
            return p.read_text(encoding="utf-8", errors="ignore")
    return None


def retrieve(query: str, k: int = 6) -> list[dict]:
    """Top-k articles wiki — domaine insecte uniquement."""
    cov = load_coverage()
    qual = load_quality()
    titles = list(dict.fromkeys(list(cov.get("nodes", {}).keys()) + list_wiki_titles()))
    scored = []
    for title in titles:
        if is_hard_junk(title):
            continue
        text = read_article(title) or ""
        if not is_domain_node(title, text[:400]):
            continue
        sc = _score_doc(query, title, text)
        if sc < 0.5:
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
    return scored[:k]


def answer(
    query: str,
    k: int = 6,
    use_arxiv: bool = True,
    temperature: float = 0.2,
) -> dict:
    q = (query or "").strip()

    # Salutations : ne pas balancer 3 articles hors-sujet
    if GREETING.search(q) or len(q) < 4:
        return {
            "answer": (
                "Salut — je suis The-fly, un graphe vivant sur les mouches et les insectes. "
                "Pose-moi une vraie question de mouche : vol, haltères, yeux composés, "
                "alimentation, larves, écologie…"
            ),
            "sources": [],
            "arxiv": [],
            "model": None,
            "mode": "greeting",
        }

    docs = retrieve(q, k=k)
    papers = search_domain(q, max_results=4) if use_arxiv else []
    papers = [
        p
        for p in papers
        if not is_hard_junk(p.get("title", ""), p.get("summary", ""))
        and (
            score_relevance(p.get("title", ""), p.get("summary", "")) >= 0.28
            or any(
                t in (p.get("summary") or "").lower()
                for t in ("insect", "drosophila", "diptera", "housefly", "mosquito", "haltere")
            )
        )
    ][:3]

    sources = [d["title"] for d in docs]
    ctx_wiki = "\n\n".join(
        f"### {d['title']} (q={d.get('quality')}, depth={d.get('depth')})\n{d['text']}"
        for d in docs
    )
    ctx_arxiv = format_arxiv_context(papers) if papers else ""

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        if not docs:
            return {
                "answer": (
                    "Je n’ai rien de solide dans le noyau insecte pour ça. "
                    "Essaie : « comment vole la mouche », « rôle des haltères », "
                    "« alimentation de la mouche domestique »."
                ),
                "sources": [],
                "arxiv": papers,
                "model": None,
                "mode": "extractive_empty",
            }
        bits = []
        for d in docs[:4]:
            lines = [ln for ln in d["text"].splitlines() if ln.strip() and not ln.startswith("#")]
            bits.append(f"• {d['title']}: {' '.join(lines[:3])[:350]}")
        return {
            "answer": "D’après le noyau wiki (domaine insecte) :\n" + "\n".join(bits),
            "sources": sources,
            "arxiv": papers,
            "model": None,
            "mode": "extractive",
        }

    prompt = f"""Tu es The-fly : une intelligence qui raisonne COMME une mouche savante.
Domaine UNIQUE : insectes, diptères, mouches, vol, morphologie, écologie, évolution des insectes.

Réponds en français, précis, 80–180 mots.
Règles STRICTES :
1. Utilise UNIQUEMENT le contexte wiki/arXiv ci-dessous.
2. Ignore tout hors-sujet (brasseries, pêche à la mouche, associations, livres génériques).
3. Si le contexte est vide ou hors-sujet, dis que tu ne sais pas encore et propose une question insecte.
4. Ne cite JAMAIS une source hors domaine insecte.
5. Ton : clair, un peu « cerveau de mouche » (concret, sensoriel), sans blabla corporate.

Question: {q}

=== CONTEXTE WIKI (noyau appris) ===
{ctx_wiki[:7000] if ctx_wiki else "(vide)"}

=== CONTEXTE ARXIV ===
{ctx_arxiv[:2000] if ctx_arxiv else "(aucun)"}
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
                "max_tokens": 700,
            },
            timeout=90,
        )
        if r.status_code != 200:
            return {
                "answer": f"[Groq HTTP {r.status_code}] " + (ctx_wiki[:1200] or "pas de contexte"),
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
    q = f"Vérification factuelle (domaine insecte uniquement): {claim}"
    res = answer(
        q + "\nRéponds par SOUTENU / PARTIEL / NON_SOUTENU puis justification courte.",
        k=k,
        use_arxiv=True,
        temperature=0.1,
    )
    res["claim"] = claim
    return res
