"""
Skill learning hors-wiki : code, sécu défensive, recherche web, images.
Écrit des notes Markdown dans skill_notes/ et renforce skills.json.
Pas d'attaque offensive — uniquement défense / méthode / outils légitimes.
"""
from __future__ import annotations

import os
import re
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from .memory import log_event, STATE_DIR
from .skills import load_skills, save_skills, reinforce_skill
from .tools import git_commit_push

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
NOTES_DIR = Path("skill_notes")

# Tracks d'auto-apprentissage (rotation)
SKILL_TRACKS = {
    "code_et_outils": {
        "topics": [
            "clean architecture for autonomous agents",
            "HTML canvas particle systems for scientific viz",
            "Python asyncio patterns for scrapers",
            "GitHub Actions for continuous learning loops",
            "Graph RAG retrieval quality tricks",
        ],
        "keywords": ["code", "html", "python", "agent", "api"],
    },
    "securite_defensive": {
        "topics": [
            "secure coding basics input validation",
            "dependency pinning and supply chain hygiene",
            "secrets management GitHub Actions",
            "CORS and browser security model",
            "logging without leaking credentials",
        ],
        "keywords": ["security", "secure", "secrets", "validation", "cors"],
    },
    "recherche_web": {
        "topics": [
            "query formulation for scientific literature",
            "evaluating source reliability",
            "Wikipedia API vs primary papers",
            "arXiv search strategies for entomology",
            "cross-checking claims across sources",
        ],
        "keywords": ["search", "web", "arxiv", "source", "query"],
    },
    "recherche_image": {
        "topics": [
            "describing insect morphology for image search",
            "scientific figure interpretation",
            "alt text and accessibility for diagrams",
            "avoiding mislabeled insect photos",
            "canvas schematic drawing of fly anatomy",
        ],
        "keywords": ["image", "diagram", "figure", "visual", "canvas"],
    },
    "raisonnement": {
        "topics": [
            "intent routing for multi-mode agents",
            "anti-drift semantic filters",
            "when to refuse vs when to answer",
            "grounding LLM answers on retrieved notes",
            "self-evaluation loops for agent quality",
        ],
        "keywords": ["plan", "intent", "reasoning", "rag", "eval"],
    },
    "representation": {
        "topics": [
            "force-directed graph layouts",
            "skill cortex visualization design",
            "ASCII diagrams for anatomy",
            "dark terminal aesthetic UI",
            "interactive fly flight demos",
        ],
        "keywords": ["graph", "viz", "ascii", "ui", "demo"],
    },
}


def _ensure_skill_keys():
    skills = load_skills()
    changed = False
    for name, meta in SKILL_TRACKS.items():
        if name not in skills:
            skills[name] = {
                "level": 0.5,
                "description": f"Auto-track {name}",
                "keywords": meta["keywords"],
                "articles": [],
            }
            changed = True
    if changed:
        save_skills(skills)
    return skills


def _pick_track() -> str:
    skills = _ensure_skill_keys()
    # préférer le skill technique le plus faible
    tracks = list(SKILL_TRACKS.keys())
    ranked = sorted(tracks, key=lambda n: skills.get(n, {}).get("level", 0))
    return ranked[0]


def _groq_note(skill: str, topic: str) -> str | None:
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    prompt = f"""Tu es The-fly, agent d'apprentissage autonome.
Écris une NOTE DE COMPÉTENCE dense et opérationnelle (FR, 250–450 mots) sur:
Skill: {skill}
Topic: {topic}

Contraintes:
- Concret, actionnable, pas de blabla marketing
- Si sécu: UNIQUEMENT défensive (pas de guide d'attaque)
- Structure: ## Contexte / ## Méthode / ## Pièges / ## Checklist
- Lien possible avec agents autonomes / graphes de connaissance
Markdown pur, pas de fences externes.
"""
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.35,
                "max_tokens": 900,
            },
            timeout=90,
        )
        if r.status_code != 200:
            print(f"[skill_learn] Groq HTTP {r.status_code}", flush=True)
            return None
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[skill_learn] error: {e}", flush=True)
        return None


def run_skill_learn() -> bool:
    """Un cycle d'apprentissage skill (note + reinforce)."""
    print("[skill_learn] cycle compétences transverses", flush=True)
    skills = _ensure_skill_keys()
    skill = _pick_track()
    topics = SKILL_TRACKS[skill]["topics"]
    # topic non encore noté si possible
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    existing = {p.stem for p in NOTES_DIR.glob("*.md")}
    topic = topics[0]
    for t in topics:
        slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60]
        if slug not in existing:
            topic = t
            break
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:60]
    path = NOTES_DIR / f"{slug}.md"
    if path.exists():
        print(f"[skill_learn] déjà vu: {slug}", flush=True)
        # reinforce légèrement quand même pour rotation
        reinforce_skill(skill, slug, 40)
        return False

    body = _groq_note(skill, topic)
    if not body:
        # fallback minimal sans LLM
        body = (
            f"# {topic}\n\n## Contexte\nNote auto-générée (fallback) pour skill `{skill}`.\n\n"
            f"## Méthode\nDocumenter, tester, itérer.\n\n## Checklist\n- [ ] Lire\n- [ ] Appliquer\n- [ ] Mesurer\n"
        )

    header = (
        f"---\nskill: {skill}\ntopic: {topic}\n"
        f"created: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
    )
    path.write_text(header + body + "\n", encoding="utf-8")
    reinforce_skill(skill, slug, 75)
    log_event("skill_learn", {"skill": skill, "topic": topic, "file": str(path)})
    try:
        git_commit_push(
            [str(path), "state/skills.json", "state/"],
            f"skill_learn: {skill} — {slug}",
        )
    except Exception as e:
        print(f"[skill_learn] push skip: {e}", flush=True)
    print(f"[skill_learn] ✅ {skill} ← {topic}", flush=True)
    return True
