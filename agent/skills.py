"""Système de compétences (nœuds neuronaux) que l'agent développe.

Anti-dérive v3 : domaine insecte + compétences code/représentation.
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from .memory import STATE_DIR, log_event

SKILLS_FILE = STATE_DIR / "skills.json"

DEFAULT_SKILLS = {
    "entomologie": {
        "level": 1.0,
        "description": "Connaissance générale des insectes",
        "keywords": ["insect", "insecte", "diptera", "fly", "mouche", "entomology", "arthropod"],
        "articles": [],
    },
    "anatomie_insecte": {
        "level": 0.5,
        "description": "Morphologie et organes des insectes",
        "keywords": ["wing", "aile", "halter", "thorax", "antenne", "compound eye", "exoskeleton", "spiracle", "mouthpart"],
        "articles": [],
    },
    "vol_et_aerodynamique": {
        "level": 0.3,
        "description": "Mécanismes du vol des diptères",
        "keywords": ["flight", "vol", "aerodynamic", "wingbeat", "hover", "maneuver", "lift", "drag"],
        "articles": [],
    },
    "ecologie": {
        "level": 0.4,
        "description": "Rôle écologique, habitats, interactions",
        "keywords": ["ecology", "habitat", "pollinat", "predator", "parasite", "larva", "maggot", "decomposer"],
        "articles": [],
    },
    "evolution": {
        "level": 0.2,
        "description": "Histoire évolutive des diptères",
        "keywords": ["evolution", "fossil", "phylogen", "adaptation", "speciation", "radiation", "devonian", "paleoptera", "neoptera"],
        "articles": [],
    },
    "comportement": {
        "level": 0.3,
        "description": "Comportements (reproduction, alimentation, social)",
        "keywords": ["behavior", "behaviour", "mating", "feeding", "swarm", "courtship", "foraging", "mimicry"],
        "articles": [],
    },
    "code_et_outils": {
        "level": 0.5,
        "description": "Coder HTML/JS/Python, scripts agent, APIs",
        "keywords": ["code", "html", "python", "javascript", "api", "script", "github"],
        "articles": [],
    },
    "representation": {
        "level": 0.4,
        "description": "Viz graphes, ASCII, pages, cortex skills",
        "keywords": ["graph", "visual", "ascii", "canvas", "network", "cortex"],
        "articles": [],
    },
    "raisonnement": {
        "level": 0.5,
        "description": "Planifier, router intent, anti-dérive, Graph-RAG",
        "keywords": ["plan", "rag", "intent", "reasoning", "agent"],
        "articles": [],
    },
}

CORE_TERMS = {
    "fly", "flies", "mouche", "diptera", "insect", "insecte", "arthropod",
    "wing", "halter", "haltere", "larva", "maggot", "pupa",
    "entomolog", "thorax", "antenna", "exoskeleton", "compound eye",
    "hover", "swarm", "pollinat", "parasitoid", "mimicry",
    "neoptera", "paleoptera", "apterygota", "alate",
    "housefly", "blowfly", "hoverfly", "drosophila", "mosquito",
    "mouthpart", "proboscis", "spiracle",
}

STRONG_TERMS = CORE_TERMS | {
    "flight", "aerodynamic", "wingbeat", "ecology", "evolution",
    "speciation", "adaptation", "phylogen", "fossil", "devonian",
    "predator", "parasite", "decomposer", "courtship", "foraging",
    "tachinid", "fruit fly", "insect flight", "insect ecology",
    "insect behavior", "insect behaviour", "insect morphology",
}

HARD_JUNK = re.compile(
    r"("
    r"chewing gum|bubblegum|"
    r"eccentricity\s*\(behavior\)|eccentricity\s*\(behaviour\)|"
    r"tv series|television|album|film|song|band|episode|novel|game|"
    r"airline|aircraft manufacturer|institute|university|"
    r"password|malware|firewall|encryption|computer security|cybersecurity|"
    r"angular velocity|angular momentum|"
    r"wuornos|wing chun|"
    r"isbn|doi\s*:|academic press|publisher|"
    r"software|operating system|programming language|"
    r"human anatomy|mammal|penis|vagina|rectum|feces|anus|"
    r"fly\s*fishing|fishing|angler|trout|salmon|bamboo fly rod|"
    r"brewery|brewing|brewpub|beer|allagash|off color|two brothers|"
    r"bibliography|company|corporation|inc\.|ltd|"
    r"behavioral\s+momentum|association for the study|"
    r"animal behaviour\)|journal of|proceedings of|"
    r"critique of some current|george\s+c\.?\s*williams|"
    r"nasdaq|stock|football|basketball|baseball|soccer|"
    r"punk rock|blowfly's party|blowfly's punk|"
    r"cognitive behavioral|behavior therapy|behavior modification|"
    r"vineland adaptive|behaviour interactive|hovercraft|hovertrain|"
    r"madama butterfly|catskill fly|artificial fly|dry fly|wet fly|"
    r"flying boat|floatplane|list of flying"
    r")",
    re.I,
)

NOISE_TERMS = {
    "computer security", "cybersecurity", "encryption", "password",
    "malware", "firewall",
    "fishing", "brewery", "brewing", "bibliography",
    "behavioral momentum", "punk rock", "behavior therapy",
}

FALSE_FLY = re.compile(
    r"\b(fly\s*fishing|fishing\s*fly|butterfly|flying\s+fox|flywheel|flyby|"
    r"artificial fly|bamboo fly|dry fly|wet fly|fly rod|fly tying)\b",
    re.I,
)


def load_skills():
    if SKILLS_FILE.exists():
        skills = json.loads(SKILLS_FILE.read_text(encoding="utf-8"))
        # merge new default skills if missing
        for k, v in DEFAULT_SKILLS.items():
            if k not in skills:
                skills[k] = v.copy()
        return skills
    return {k: v.copy() for k, v in DEFAULT_SKILLS.items()}


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


def is_hard_junk(title: str, extract: str = "") -> bool:
    text = f"{title} {extract}".strip()
    if not text:
        return True
    if HARD_JUNK.search(text):
        return True
    if FALSE_FLY.search(title or ""):
        return True
    return False


def is_domain_node(title: str, extract: str = "") -> bool:
    if is_hard_junk(title, extract):
        return False
    return score_relevance(title, extract) >= 0.35


def score_relevance(title: str, extract: str = "") -> float:
    if not title or not title.strip():
        return 0.0
    if is_hard_junk(title, extract):
        return 0.0

    text = (title + " " + (extract or "")).lower()
    title_l = title.lower()

    if any(n in text for n in NOISE_TERMS) and not any(c in text for c in CORE_TERMS):
        return 0.0

    skills = load_skills()
    best_skill = 0.0
    for skill in skills.values():
        hits = sum(1 for kw in skill.get("keywords", []) if kw.lower() in text)
        if hits:
            rel = min(1.0, hits / 2.5) * (0.45 + skill.get("level", 0) / 25)
            best_skill = max(best_skill, rel)

    core_hits = sum(1 for t in CORE_TERMS if t in text)
    strong_hits = sum(1 for t in STRONG_TERMS if t in text)

    core_score = min(1.0, core_hits / 2.0) * 0.55
    strong_score = min(1.0, strong_hits / 3.0) * 0.35

    title_bonus = 0.0
    if any(s in title_l for s in CORE_TERMS):
        title_bonus = 0.35
    elif any(s in title_l for s in STRONG_TERMS):
        title_bonus = 0.18

    generic = {"behavior", "behaviour", "adaptation", "ecology", "evolution", "morphology"}
    if any(g in title_l for g in generic) and core_hits == 0 and strong_hits <= 1:
        title_bonus -= 0.35

    if re.search(r"\b(association|society|journal|review of|company|brewery)\b", title_l):
        if core_hits == 0:
            return 0.0

    score = best_skill + core_score + strong_score + title_bonus
    score = max(0.0, min(1.0, score))

    strong_anchor = (
        "diptera", "housefly", "hoverfly", "blowfly", "drosophila", "mosquito",
        "haltere", "halteres", "insect flight", "insect ecology", "insect morphology",
        "maggot", "larva", "compound eye", "musca",
    )
    if any(s in title_l for s in strong_anchor):
        score = max(score, 0.75)
    elif re.search(r"\b(insect|insects)\b", title_l):
        score = max(score, 0.65)
    elif re.search(r"\b(fly|flies)\b", title_l) and not FALSE_FLY.search(title_l):
        if core_hits >= 1 or strong_hits >= 2:
            score = max(score, 0.70)

    return round(score, 3)


def get_skills_summary():
    skills = load_skills()
    return {
        name: {
            "level": info["level"],
            "articles_count": len(info.get("articles", [])),
        }
        for name, info in skills.items()
    }
