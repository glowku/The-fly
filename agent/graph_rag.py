"""
Graph-RAG The-fly : nœuds wiki + skill_notes + arXiv + recherche web live.
Questions d'actualité / cyber / sorties → web search obligatoire.
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
from .web_search import needs_live_web, search_web, format_web_context

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
WIKI_DIR = Path("wiki")
NOTES_DIR = Path("skill_notes")

FR_EXPAND = {
    "vol": ["flight", "insect flight", "wing", "haltere", "hover"],
    "mouche": ["fly", "housefly", "diptera", "musca", "drosophila"],
    "insecte": ["insect", "entomology", "arthropod"],
    "code": ["software", "python", "api", "architecture", "git"],
    "sécurité": ["security", "secure", "validation", "owasp"],
    "securite": ["security", "secure", "validation", "owasp"],
}

GREETING = re.compile(
    r"^(salut|hello|hi|hey|bonjour|bonsoir|ça\s*va|ca\s*va|comment\s+tu\s+vas|"
    r"qui\s+es|présente|t'es\s+la|tes\s+la)\b", re.I,
)
SKILL_Q = re.compile(
    r"(booster?|améliorer|ameliorer|upgrade).*(skill|compétence)|"
    r"(skill|compétence).*(booster?|améliorer)", re.I,
)
TECH_Q = re.compile(
    r"\b(code|coder|python|api|git|sécurit|securit|owasp|architecture|rag|"
    r"agent|validation|cors|docker|skill_notes?)\b", re.I,
)

NO_CUTOFF = (
    "Tu as accès à une recherche web LIVE. "
    "Ne dis JAMAIS que ta connaissance s'arrête en 2023/2024/2025, "
    "ni « je n'ai pas d'accès temps réel », ni « ma base s'arrête en… ». "
    "Si le contexte WEB LIVE est fourni, base-toi UNIQUEMENT dessus pour les faits récents. "
    "Cite les sources (titres / URLs) quand tu affirmes un incident ou une date de sortie."
)


def _tokenize(q: str) -> list[str]:
    words = [w for w in re.split(r"[^a-zA-Z0-9àâäéèêëïîôùûüç]+", (q or "").lower()) if len(w) > 2]
    out = list(words)
    for w in words:
        out.extend(FR_EXPAND.get(w, []))
    seen, uniq = set(), []
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
        m = re.search(r"skill:\s*(\S+)", text[:400])
        skill = m.group(1) if m else ""
        if skill and any(w in skill.lower() for w in words):
            sc += 3
        if sc > 0:
            scored.append({"title": f"skill:{p.stem}", "score": sc, "text": head, "skill": skill, "path": str(p)})
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
        scored.append({
            "title": title, "score": round(sc, 3),
            "quality": (qual.get(title) or {}).get("score"),
            "text": (text or "")[:1800],
            "depth": (cov.get("nodes", {}).get(title) or {}).get("depth"),
        })
    scored.sort(key=lambda x: (x["score"], x.get("quality") or 0), reverse=True)
    return scored[:k]


def answer(query: str, k: int = 6, use_arxiv: bool = True, temperature: float = 0.25) -> dict:
    q = (query or "").strip()

    if GREETING.search(q) or len(q) < 4:
        levels = get_skills_summary()
        top = sorted(levels.items(), key=lambda x: -x[1].get("level", 0))[:4]
        tops = ", ".join(f"{n}={v.get('level')}" for n, v in top)
        return {"answer": f"Là. The-fly — graphe + skills ({tops}). Question concrète.", "sources": [], "arxiv": [], "model": None, "mode": "greeting"}

    if SKILL_Q.search(q):
        return {"answer": skill_boost_answer(), "sources": [], "arxiv": [], "model": None, "mode": "skill_architecture"}

    # === WEB LIVE prioritaire pour actualité / cyber / sorties ===
    force_web = needs_live_web(q)
    web_hits: list[dict] = []
    if force_web:
        try:
            web_hits = search_web(q, max_results=8)
        except Exception as e:
            print(f"[graph_rag] web_search fail: {e}", flush=True)

    docs = [] if (force_web and web_hits) else retrieve(q, k=k)
    if not force_web and re.search(r"\b(ransomware|breach|zero[- ]?day|cve|cisa|cyber|vulnérabilit|incident|gta)\b", q, re.I):
        try:
            web_hits = search_web(q, max_results=5)
        except Exception:
            pass

    notes = retrieve_skill_notes(q, k=4)
    papers = []
    if use_arxiv and not force_web:
        try:
            papers = [p for p in search_domain(q, max_results=4) if not is_hard_junk(p.get("title", ""), p.get("summary", ""))][:3]
        except Exception:
            papers = []

    sources = [d["title"] for d in docs] + [n["title"] for n in notes]
    sources += [h.get("title") or h.get("url") or "web" for h in web_hits[:5]]

    ctx_wiki = "\n\n".join(f"### {d['title']}\n{d['text']}" for d in docs)
    ctx_notes = "\n\n".join(f"### NOTE {n['title']}\n{n['text'][:1200]}" for n in notes)
    ctx_arxiv = format_arxiv_context(papers) if papers else ""
    ctx_web = format_web_context(web_hits, limit=7)
    skills_summary = get_skills_summary()

    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        bits = []
        if ctx_web:
            bits.append("WEB LIVE:\n" + ctx_web[:1800])
        for d in docs[:3]:
            lines = [ln for ln in d["text"].splitlines() if ln.strip() and not ln.startswith("#")]
            bits.append(f"• {d['title']}: {' '.join(lines[:2])[:280]}")
        if not bits:
            return {"answer": "Peu de contexte. Lance run_chat_server.py avec GROQ_API_KEY pour la recherche live.", "sources": sources, "web": web_hits, "mode": "extractive_empty"}
        return {"answer": "\n".join(bits), "sources": sources, "web": web_hits, "mode": "extractive+web" if web_hits else "extractive"}

    web_block = f"\n=== WEB LIVE (prioritaire pour faits récents) ===\n{ctx_web}\n" if ctx_web else ""
    prompt = f"""{SYSTEM_CORE}

{NO_CUTOFF}

Niveaux skills: {skills_summary}
Réponds en français, précis, 80–220 mots.
Si WEB LIVE est présent, commence par les faits datés et cite les sources.

Question: {q}
{web_block}
=== NŒUDS WIKI ===
{ctx_wiki or '(vide)'}

=== SKILL NOTES ===
{ctx_notes or '(vide)'}

=== ARXIV ===
{ctx_arxiv or '(vide)'}
"""

    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": temperature, "max_tokens": 1100},
            timeout=90,
        )
        if r.status_code != 200:
            return {"answer": f"Moteur langage indispo ({r.status_code}).", "sources": sources, "web": web_hits, "mode": "error"}
        text = r.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r"\b(GPT-?4|ChatGPT|OpenAI|Groq|Claude)\b", "moteur de langage", text, flags=re.I)
        text = re.sub(
            r"(?i)(ma base de connaissances|knowledge cutoff|je n'ai pas d'accès (aux? données?|temps réel)|"
            r"mes connaissances s'arr[eê]tent|as of (my )?knowledge|trained until).{0,80}",
            "", text,
        )
        return {
            "answer": text.strip(),
            "sources": sources,
            "arxiv": papers,
            "web": web_hits,
            "model": "the-fly-cortex",
            "mode": "rag+web" if web_hits else "rag+skills",
            "skills": skills_summary,
        }
    except Exception as e:
        return {"answer": f"Erreur cortex: {e}", "sources": sources, "web": web_hits, "mode": "error"}
