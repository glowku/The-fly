"""Planification intelligente avec filtre de pertinence + compétences."""
from .memory import load_coverage, load_quality, log_event
from .skills import pick_skill_to_develop, score_relevance, load_skills


def _score_candidate(title: str, cov: dict, qual: dict, target_skill: str) -> float:
    score = 0.0

    if title in qual:
        q = qual[title].get("score", 10)
        if q < 4.0:
            return 120.0 + (4.0 - q) * 10
        if q < 6.5:
            score += (6.5 - q) * 6

    rel = score_relevance(title)
    score += rel * 35

    if title in cov.get("frontier", []) and title not in cov.get("nodes", {}):
        score += 30.0
        score += max(0, 12 - len(title) * 0.25)

    node = cov.get("nodes", {}).get(title)
    if node:
        depth = node.get("depth", 5)
        score += max(0, 12 - depth * 1.8)
    else:
        incoming = sum(1 for e in cov.get("edges", []) if e.get("to") == title)
        score += min(incoming * 2.5, 12)

    skills = load_skills()
    skill = skills.get(target_skill, {})
    for kw in skill.get("keywords", []):
        if kw.lower() in title.lower():
            score += 18
            break

    if len(title) > 55:
        score -= 12
    if title.count(" ") > 5:
        score -= 6
    banned = ["anus", "human", "mammal", "penis", "vagina", "rectum", "feces", "shit"]
    if any(b in title.lower() for b in banned):
        score -= 80

    return score


def pick_next_target(strategy: str = "value"):
    cov = load_coverage()
    qual = load_quality()
    target_skill = pick_skill_to_develop()

    candidates = []

    for title, info in qual.items():
        if info.get("score", 10) < 6.5:
            candidates.append((title, "repair", info.get("score", 0)))

    for t in cov.get("frontier", []):
        if t not in cov.get("nodes", {}):
            if score_relevance(t) >= 0.25:
                candidates.append((t, "expand", 0))

    for title, node in cov.get("nodes", {}).items():
        out_degree = sum(1 for e in cov.get("edges", []) if e.get("from") == title)
        if out_degree < 3:
            candidates.append((title, "re-expand", out_degree))

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
        prio = _score_candidate(title, cov, qual, target_skill)
        if action == "repair":
            prio += 40
        scored.append((prio, title, action, extra))

    scored.sort(reverse=True)
    best = scored[0]
    prio, title, action, extra = best

    reason_map = {
        "repair": f"low_quality={extra:.1f}",
        "expand": "frontier_gap",
        "re-expand": f"low_outdegree={extra}",
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
    if score_relevance(title) < 0.2:
        return

    cov = load_coverage()
    if title in cov["nodes"] or title in cov.get("frontier", []):
        if parent:
            edge = {"from": parent, "to": title}
            if edge not in cov["edges"]:
                cov["edges"].append(edge)
                from .memory import save_coverage
                save_coverage(cov)
        return

    if title not in cov["frontier"]:
        cov["frontier"].append(title)
    if parent:
        edge = {"from": parent, "to": title}
        if edge not in cov["edges"]:
            cov["edges"].append(edge)
    from .memory import save_coverage
    save_coverage(cov)


def register_processed(title: str, depth: int, sources: list):
    from datetime import datetime, timezone
    cov = load_coverage()
    cov["nodes"][title] = {
        "depth": depth,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": sources,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    cov["frontier"] = [t for t in cov.get("frontier", []) if t != title]
    cov["max_depth"] = max(cov.get("max_depth", 0), depth)
    from .memory import save_coverage
    save_coverage(cov)
