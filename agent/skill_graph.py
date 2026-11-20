"""Injecte les skills comme nœuds du graphe + arêtes skill→articles.

Les skills appris (state/skills.json) deviennent des nœuds `skill:<name>`
reliés aux articles qu'ils ont réellement appris. Appelé par densify / évolution.
"""
from __future__ import annotations

from .memory import load_coverage, save_coverage, log_event
from .skills import load_skills


def inject_skill_nodes(max_edges_per_skill: int = 40) -> dict:
    """Ajoute nœuds skill + arêtes vers articles connus. Idempotent."""
    cov = load_coverage()
    nodes = cov.setdefault("nodes", {})
    edges = list(cov.get("edges") or [])
    edge_set = {(e.get("from"), e.get("to")) for e in edges if e.get("from") and e.get("to")}
    skills = load_skills()
    added_nodes = 0
    added_edges = 0

    for name, info in skills.items():
        sid = f"skill:{name}"
        if sid not in nodes:
            nodes[sid] = {
                "depth": 0,
                "kind": "skill",
                "skill": name,
                "level": info.get("level", 1),
            }
            added_nodes += 1
        else:
            nodes[sid]["level"] = info.get("level", nodes[sid].get("level", 1))
            nodes[sid]["kind"] = "skill"

        arts = list(info.get("articles") or [])[:max_edges_per_skill]
        for art in arts:
            if art not in nodes:
                continue
            if (sid, art) not in edge_set:
                edges.append({"from": sid, "to": art, "kind": "skill_link", "skill": name})
                edge_set.add((sid, art))
                added_edges += 1

    cov["nodes"] = nodes
    cov["edges"] = edges
    save_coverage(cov)
    log_event("inject_skill_nodes", {"nodes": added_nodes, "edges": added_edges})
    return {"added_nodes": added_nodes, "added_edges": added_edges, "skills": len(skills)}
