"""Système de compétences (nœuds neuronaux) que l'agent développe."""
import json
from datetime import datetime, timezone
from pathlib import Path
from .memory import STATE_DIR, log_event

SKILLS_FILE = STATE_DIR / "skills.json"

DEFAULT_SKILLS = {
    "entomologie": {
        "level": 1.0,
        "description": "Connaissance générale des insectes",
        "keywords": ["insect", "insecte", "diptera", "fly", "mouche", "entomology"],
        "articles": [],
    },
    "anatomie_insecte": {
        "level": 0.5,
        "description": "Morphologie et organes des insectes",
        "keywords": ["wing", "aile", "halter", "thorax", "antenne", "compound eye", "exoskeleton"],
        "articles": [],
    },
    "vol_et_aerodynamique": {
        "level": 0.3,
        "description": "Mécanismes du vol des diptères",
        "keywords": ["flight", "vol", "aerodynamic", "wingbeat", "hover", "maneuver"],
        "articles": [],
    },
    "ecologie": {
        "level": 0.4,
        "description": "Rôle écologique, habitats, interactions",
        "keywords": ["ecology", "habitat", "pollinat", "predator", "parasite", "larva"],
        "articles": [],
    },
    "evolution": {
        "level": 0.2,
        "description": "Histoire évolutive des diptères",
        "keywords": ["evolution", "fossil", "phylogen", "adaptation", "speciation"],
        "articles": [],
    },
    "comportement": {
        "level": 0.3,
        "description": "Comportements (reproduction, alimentation, social)",
        "keywords": ["behavior", "mating", "feeding", "swarm", "courtship"],
        "articles": [],
    },
}


def load_skills():
    if SKILLS_FILE.exists():
        return json.loads(SKILLS_FILE.read_text(encoding="utf-8"))
    return DEFAULT_SKILLS.copy()


def save_skills(skills):
    SKILLS_FILE.write_text(json.dumps(skills, indent=2, ensure_ascii=False), encoding="utf-8")


def pick_skill_to_develop():
    skills = load_skills()
    sorted_skills = sorted(skills.items(), key=lambda kv: kv[1]["level"])
    return sorted_skills[0][0] if sorted_skills else "entomologie"


def reinforce_skill(skill_name: str, article_title: str, score: float):
    skills = load_skills()
    if skill_name not in skills:
        return
    gain = min(0.15, score / 100.0)
    skills[skill_name]["level"] = round(min(10.0, skills[skill_name]["level"] + gain), 2)
    if article_title not in skills[skill_name]["articles"]:
        skills[skill_name]["articles"].append(article_title)
    skills[skill_name]["last_reinforced"] = datetime.now(timezone.utc).isoformat()
    save_skills(skills)
    log_event("skill_reinforce", {
        "skill": skill_name,
        "new_level": skills[skill_name]["level"],
        "article": article_title,
    })


def score_relevance(title: str, extract: str = "") -> float:
    skills = load_skills()
    text = (title + " " + extract).lower()
    best = 0.0
    for skill in skills.values():
        hits = sum(1 for kw in skill["keywords"] if kw.lower() in text)
        if hits:
            rel = min(1.0, hits / 3.0) * (0.5 + skill["level"] / 20)
            best = max(best, rel)
    strong = ["fly", "mouche", "diptera", "insect", "insecte", "wing", "aile", "larva", "maggot"]
    if any(s in title.lower() for s in strong):
        best = max(best, 0.7)
    return round(best, 3)


def get_skills_summary():
    skills = load_skills()
    return {
        name: {
            "level": info["level"],
            "articles_count": len(info.get("articles", [])),
        }
        for name, info in skills.items()
    }
