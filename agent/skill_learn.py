"""
Skill learning hors-wiki : code, sécu défensive, recherche web, images, raisonnement.
Notes Markdown dans skill_notes/ + reinforce skills.json.
Pas d'attaque offensive.
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

import requests

from .memory import log_event
from .skills import load_skills, save_skills, reinforce_skill
from .tools import git_commit_push

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"
NOTES_DIR = Path("skill_notes")

SKILL_TRACKS = {
    "code_et_outils": {
        "topics": [
            "clean architecture for autonomous agents",
            "HTML canvas particle systems for scientific viz",
            "Python asyncio patterns for scrapers",
            "GitHub Actions for continuous learning loops",
            "Graph RAG retrieval quality tricks",
            "streaming JSONL agent logs",
            "idempotent git commit push from workers",
            "typing and contracts between agent modules",
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
            "path traversal guards on wiki paths",
            "rate limiting public chat endpoints",
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
            "deduplicating search results by title norm",
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
            "chat-triggered learning without fake APIs",
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
    tracks = list(SKILL_TRACKS.keys())
    return sorted(tracks, key=lambda n: skills.get(n, {}).get("level", 0))[0]


def _groq_note(skill: str, topic: str) -> str | None:
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return None
    prompt = f"""Tu es The-fly, agent d'apprentissage autonome.
NOTE DE COMPÉTENCE opérationnelle (FR, 280–500 mots) :
Skill: {skill}
Topic: {topic}

Contraintes:
- Concret, actionnable, zéro marketing
- Sécu: UNIQUEMENT défensive
- Structure: ## Contexte / ## Méthode / ## Pièges / ## Checklist
- Lien agents autonomes / graphes si pertinent
Markdown pur.
"""
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
                "max_tokens": 1000,
            },
            timeout=90,
        )
        if r.status_code != 200:
            return None
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[skill_learn] error: {e}", flush=True)
        return None


def run_skill_learn(force_skill: str | None = None, force_topic: str | None = None) -> dict:
    print("[skill_learn] cycle compétences", flush=True)
    skills = _ensure_skill_keys()
    skill = force_skill if force_skill in SKILL_TRACKS else _pick_track()
    topics = SKILL_TRACKS[skill]["topics"]
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    existing = {p.stem for p in NOTES_DIR.glob("*.md")}

    if force_topic:
        topic = force_topic
    else:
        topic = topics[0]
        for t in topics:
            slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")[:60]
            if slug not in existing:
                topic = t
                break

    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:60]
    path = NOTES_DIR / f"{slug}.md"
    if path.exists() and not force_topic:
        reinforce_skill(skill, slug, 25)
        return {"ok": True, "skill": skill, "topic": topic, "file": str(path), "new": False}

    body = _groq_note(skill, topic)
    if not body:
        body = (
            f"# {topic}\n\n## Contexte\nNote fallback skill `{skill}`.\n\n"
            f"## Méthode\nDocumenter → tester → mesurer.\n\n## Checklist\n- [ ] Lire\n- [ ] Appliquer\n"
        )

    header = (
        f"---\nskill: {skill}\ntopic: {topic}\n"
        f"created: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
    )
    path.write_text(header + body + "\n", encoding="utf-8")
    reinforce_skill(skill, slug, 80)
    log_event("skill_learn", {"skill": skill, "topic": topic, "file": str(path)})
    try:
        git_commit_push([str(path), "state/skills.json", "state/"], f"skill_learn: {skill} — {slug}")
    except Exception as e:
        print(f"[skill_learn] push skip: {e}", flush=True)
    print(f"[skill_learn] ✅ {skill} ← {topic}", flush=True)
    return {"ok": True, "skill": skill, "topic": topic, "file": str(path), "new": True}
