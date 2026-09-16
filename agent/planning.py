"""Planification : priorise nœuds sans enfants, frontier, qualité faible, anti-doublon."""
from .memory import load_coverage, load_quality, log_event
from .skills import pick_skill_to_develop, score_relevance, load_skills


def _children_of(title: str, cov: dict) -> list:
    return [e["to"] for e in cov.get("edges", []) if e.get("from") == title]


def _score_candidate(title: str, cov: dict, qual: dict, target_skill: str, action: str) -> float:
    score = 0.0
    nodes = cov.get("nodes", {})
    frontier = cov.get("frontier", [])

    # --- qualité faible → repair ---
    if title in qual:
        q = qual[title].get("score", 10)
        if q < 4.0:
            return 200.0 + (4.0 - q) * 10
        if q < 6.5:
            score += (6.5 - q) * 8

    # --- nœud existant SANS enfants (feuille) = priorité haute pour ramifier ---
    if title in nodes:
        kids = _children_of(title, cov)
        if len(kids) == 0:
            score += 55.0  # gros bonus : créer des sous-branches
        elif len(kids) < 3:
            score += 25.0 + (3 - len(kids)) * 5
        else:
            score -= 5.0  # déjà bien branché

    # --- frontier jamais écrite ---
    if title in frontier and title not in nodes:
        score += 40.0
        score += max(0, 10 - len(title) * 0.2)

    # --- pertinence skill ---
    rel = score_relevance(title)
    score += rel * 30

    skills = load_skills()
    skill = skills.get(target_skill, {})
    for kw in skill.get("keywords", []):
        if kw.lower() in title.lower():
            score += 16
            break

    # --- profondeur ---
    node = nodes.get(title)
    if node:
        depth = node.get("depth", 5)
        score += max(0, 10 - depth * 1.5)

    # --- action bonuses ---
    if action == "repair":
        score += 35
    elif action == "branch":  # feuille sans enfants
        score += 45
    elif action == "expand":
        score += 10

    # --- pénalités ---
    if len(title) > 55:
        score -= 12
    if title.count(" ") > 5:
        score -= 6
    banned = ["anus", "human", "mammal", "penis", "vagina", "rectum", "feces",
              "computer security", "password", "malware"]
    if any(b in title.lower() for b in banned):
        score -= 100

    return score


def pick_next_target(strategy: str = "value"):
    """
    Priorités :
    1. repair articles faibles
    2. branch : nœuds SANS sous-enfants (étendre le graphe)
    3. expand : frontier non encore écrite
    4. re-expand : nœuds avec peu d'enfants
    """
    cov = load_coverage()
    qual = load_quality()
    target_skill = pick_skill_to_develop()
    nodes = cov.get("nodes", {})
    candidates = []

    # 1. repair
    for title, info in qual.items():
        if info.get("score", 10) < 6.5:
            candidates.append((title, "repair", info.get("score", 0)))

    # 2. feuilles sans enfants (nœuds existants à ramifier)
    for title in nodes:
        kids = _children_of(title, cov)
        if len(kids) == 0:
            candidates.append((title, "branch", 0))
        elif len(kids) < 2:
            candidates.append((title, "re-expand", len(kids)))

    # 3. frontier jamais écrite
    for t in cov.get("frontier", []):
        if t not in nodes and score_relevance(t) >= 0.2:
            candidates.append((t, "expand", 0))

    if not candidates:
        root = cov.get("root", "Fly")
        return {
            "title": root,
            "reason": "bootstrap",
            "action": "expand",
            "priority": 999,
            "skill": target_skill,
        }

    scored = []
    for title, action, extra in candidates:
        prio = _score_candidate(title, cov, qual, target_skill, action)
        scored.append((prio, title, action, extra))

    scored.sort(reverse=True)
    prio, title, action, extra = scored[0]

    reason_map = {
        "repair": f"low_quality={extra:.1f}",
        "expand": "frontier_new",
        "branch": "leaf_no_children",
        "re-expand": f"few_children={extra}",
    }
    reason = reason_map.get(action, action)

    log_event("plan", {
        "title": title,
        "action": action,
        "priority": round(prio, 1),
        "reason": reason,
        "skill": target_skill,
    })

    return {
        "title": title,
        "reason": reason,
        "action": action,
        "priority": round(prio, 1),
        "skill": target_skill,
    }


def register_discovered(title: str, depth: int, parent: str | None = None):
    """Ajoute à la frontier seulement si pertinent et pas déjà connu."""
    if score_relevance(title) < 0.2:
        return

    from .memory import save_coverage
    cov = load_coverage()
    nodes = cov.get("nodes", {})
    frontier = cov.get("frontier", [])

    # déjà un nœud écrit → juste l'edge parent
    if title in nodes:
        if parent:
            edge = {"from": parent, "to": title}
            if edge not in cov["edges"]:
                cov["edges"].append(edge)
                save_coverage(cov)
        return

    if title not in frontier:
        frontier.append(title)
        cov["frontier"] = frontier

    if parent:
        edge = {"from": parent, "to": title}
        if edge not in cov.get("edges", []):
            cov.setdefault("edges", []).append(edge)

    save_coverage(cov)


def register_processed(title: str, depth: int, sources: list):
    """Marque comme traité + retire de frontier."""
    from datetime import datetime, timezone
    from .memory import save_coverage
    cov = load_coverage()
    cov.setdefault("nodes", {})[title] = {
        "depth": depth,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    cov["frontier"] = [t for t in cov.get("frontier", []) if t != title]
    cov["max_depth"] = max(cov.get("max_depth", 0), depth)
    save_coverage(cov)
