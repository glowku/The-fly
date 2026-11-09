"""
Graph-RAG The-fly : nœuds wiki + skill_notes + option arXiv.
Les skills apprises sont injectées dans le chat.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

import requests

from .memory import load_coverage, load_quality
from .skills import score_relevance, is_hard_junk, is_domain_node, load_skills, get_skills_summary
from .arxiv_source import search_domain, format_arxiv_context
from .identity import SYSTEM_CORE, skill_boost_answer

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
WIKI_DIR = Path("wiki")
NOTES_DIR = Path("skill_notes")

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
    "code": ["software", "python", "api", "architecture", "git"],
    "sécurité": ["security", "secure", "validation", "owasp"],
    "securite": ["security", "secure", "validation", "owasp"],
}

GREETING = re.compile(
    r"^(salut|hello|hi|hey|bonjour|bonsoir|ça\s*va|ca\s*va|comment\s+tu\s+vas|"
    r"comment\s+allez|who\s+are\s+you|qui\s+es|présente|t'es\s+la|tes\s+la)\b",
    re.I,
)

SKILL_Q = re.compile(
    r"(booster?|améliorer|ameliorer|upgrade).*(skill|compétence|competence)|"
    r"(skill|compétence).*(booster?|améliorer)|fine[- ]?tun|ré[- ]?entraîner|re[- ]?entrain",
    re.I,
)

TECH_Q = re.compile(
    r"\b(code|coder|python|api|git|sécurit|securit|owasp|architecture|rag|"
    r"agent|validation|cors|docker|ci/cd|skill_notes?)\b",
    re.I,
)


def _tokenize(q: str) -> list[str]:
    words = [w for w in re.split(r"[^a-zA-Z0-9àâäéèêëïîôùûüç]+", (q or "").lower()) if len(w) > 2]
    out = list(words)
    for w in words:
        out.extend(FR_EXPAND.get(w, []))
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
    words = _tokenize(query)
    if not words:
        return rel
    blob = f"{title} {text[:2000]}".lower()
    hits = sum(1 for w in words if w in blob)
    title_hits = sum(1 for w in words if w in title.lower())
    return hits * 1.4 + title_hits * 3.0 + max(rel, 0) * 4.0


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


def retrieve_skill_notes(query: str, k: int = 4) -> list[dict]:
    """Récupère des notes skill_notes/ par résonance texte."""
    if not NOTES_DIR.exists():
        return []
    words = _tokenize(query)
    scored = []
    for p in NOTES_DIR.glob("*.md"):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        head = text[:2500]
        blob = (p.stem + " " + head).lower()
        sc = sum(1 for w in words if w in blob) * 2.0
        # frontmatter skill:
        m = re.search(r"skill:\s*(\S+)", text[:400])
        skill = m.group(1) if m else ""
        if skill and any(w in skill.lower() for w in words):
            sc += 3
        if TECH_Q.search(query) and skill in (
            "code_et_outils", "securite_defensive", "raisonnement",
            "recherche_web", "representation", "recherche_image",
        ):
            sc += 1.5
        if sc > 0:
            scored.append({
                "title": f"skill:{p.stem}",
                "score": sc,
                "text": head,
                "skill": skill,
                "path": str(p),
            })
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]


def retrieve(query: str, k: int = 6) -> list[dict]:
    cov = load_coverage()
    qual = load_quality()
    titles = list(dict.fromkeys(list(cov.get("nodes", {}).keys()) + list_wiki_titles()))
    scored = []
    for title in titles:
        if is_hard_junk(title):
            continue
        text = read_article(title) or ""
        # tech questions: allow non-insect wiki if title matches tech tokens
        if TECH_Q.search(query):
            sc = _score_doc(query, title, text)
        else:
            if not is_domain_node(title, text[:400]) and score_relevance(title) < 0.35:
                continue
            sc = _score_doc(query, title, text)
            if sc < 0.5:
                continue
        if sc < 0.4:
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
    temperature: float = 0.25,
) -> dict:
    q = (query or "").strip()

    if GREETING.search(q) or len(q) < 4:
        levels = get_skills_summary()
        top = sorted(levels.items(), key=lambda x: -x[1].get("level", 0))[:4]
        tops = ", ".join(f"{n}={v.get('level')}" for n, v in top)
        return {
            "answer": f"Là. The-fly — graphe + skills ({tops}). Question concrète.",
            "sources": [],
            "arxiv": [],
            "model": None,
            "mode": "greeting",
        }

    if SKILL_Q.search(q):
        return {
            "answer": skill_boost_answer(),
            "sources": [],
            "arxiv": [],
            "model": None,
            "mode": "skill_architecture",
        }

    docs = retrieve(q, k=k)
    notes = retrieve_skill_notes(q, k=4)
    papers = []
    if use_arxiv:
        try:
            papers = search_domain(q, max_results=4)
            papers = [
                p for p in papers
                if not is_hard_junk(p.get("title", ""), p.get("summary", ""))
            ][:3]
        except Exception:
            papers = []

    sources = [d["title"] for d in docs] + [n["title"] for n in notes]
    ctx_wiki = "\n\n".join(
        f"### {d['title']} (q={d.get('quality')}, depth={d.get('depth')})\n{d['text']}"
        for d in docs
    )
    ctx_notes = "\n\n".join(
        f"### NOTE {n['title']} (skill={n.get('skill')})\n{n['text'][:1200]}"
        for n in notes
    )
    ctx_arxiv = format_arxiv_context(papers) if papers else ""

    skills_summary = get_skills_summary()

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        bits = []
        for d in docs[:3]:
            lines = [ln for ln in d["text"].splitlines() if ln.strip() and not ln.startswith("#")]
            bits.append(f"• {d['title']}: {' '.join(lines[:2])[:280]}")
        for n in notes[:2]:
            bits.append(f"• {n['title']}: {n['text'][:200].replace(chr(10), ' ')}")
        if not bits:
            return {
                "answer": "Peu de contexte local. Lance skill_loop / cortex pour apprendre, ou fournis GROQ_API_KEY.",
                "sources": sources,
                "arxiv": papers,
                "model": None,
                "mode": "extractive_empty",
            }
        return {
            "answer": "Noyau local (wiki + skills) :\n" + "\n".join(bits),
            "sources": sources,
            "arxiv": papers,
            "model": None,
            "mode": "extractive",
        }

    prompt = f"""{SYSTEM_CORE}

Tu APPLIQUES les skills apprises (notes + niveaux) quand la question est tech/code/sécu.
Niveaux skills: {skills_summary}
Réponds en français, 70–180 mots hors code.
Housefly: labellum spongieux, pas stylet sanguin.

Question: {q}

=== NŒUDS WIKI ===
{ctx_wiki or '(vide)'}

=== SKILL NOTES (apprises) ===
{ctx_notes or '(vide)'}

=== ARXIV ===
{ctx_arxiv or '(vide)'}
"""

    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
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
                "answer": f"Moteur langage indispo ({r.status_code}).",
                "sources": sources,
                "arxiv": papers,
                "model": None,
                "mode": "error",
            }
        text = r.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r"\b(GPT-?4|ChatGPT|OpenAI|Groq|Claude)\b", "moteur de langage", text, flags=re.I)
        return {
            "answer": text,
            "sources": sources,
            "arxiv": papers,
            "model": "the-fly-cortex",
            "mode": "rag+skills",
            "skills": skills_summary,
        }
    except Exception as e:
        return {
            "answer": f"Erreur cortex: {e}",
            "sources": sources,
            "arxiv": papers,
            "model": None,
            "mode": "error",
        }
