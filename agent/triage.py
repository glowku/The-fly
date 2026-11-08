"""
Triage du graphe — TRIER, pas effacer.

Règles:
- Junk hard → quarantine
- Nœuds cœur insecte PROTÉGÉS (jamais sortis pour low_rel)
- low_rel seulement si score très bas ET aucun ancrage insecte
- Dédup titres
- wiki/*.md jamais supprimés
- restore_protected() ramène les faux positifs déjà quarantinés
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .memory import STATE_DIR, load_coverage, log_event
from .skills import load_skills, save_skills, is_hard_junk, score_relevance

COV_PATH = STATE_DIR / "coverage.json"
QUAL_PATH = STATE_DIR / "quality.json"
QUAR_PATH = STATE_DIR / "quarantine.json"

# Jamais triage out pour low_rel seul
PROTECTED = {
    "fly", "insect", "diptera", "housefly", "hoverfly", "blowfly", "mosquito",
    "drosophila", "fruit fly", "tachinidae", "haltere", "halteres",
    "compound eye", "insect flight", "insect wing", "insect morphology",
    "insect ecology", "insect behaviour", "insect behavior", "maggot", "larva",
    "exoskeleton", "thorax", "spiracle", "insect mouthparts", "antenna (biology)",
    "arthropod", "arthropod leg", "pollination", "parasitoid", "mimicry",
    "evolution of insects", "paleoptera", "palaeoptera", "neoptera",
    "devonian", "apterygota", "alate", "swarm behaviour", "wing",
    "aerodynamics", "hovering", "flight", "musca", "entomology",
}

INSECT_HINT = re.compile(
    r"\b(insect|insects|diptera|fly|flies|mosquito|maggot|larva|haltere|"
    r"entomolog|arthropod|drosophila|tachinid|hoverfly|blowfly|housefly|"
    r"compound eye|mouthpart|spiracle|parasitoid|pollinat|neoptera|paleoptera|"
    r"palaeoptera|apterygota|wingbeat|exoskeleton)\b",
    re.I,
)


def _load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def _save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def load_quarantine() -> dict:
    return _load_json(QUAR_PATH, {"nodes": {}, "edges": [], "dedup_map": {}, "updated_at": None})


def save_quarantine(q: dict):
    q["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_json(QUAR_PATH, q)


def _is_protected(title: str) -> bool:
    t = (title or "").lower().strip()
    if t in PROTECTED:
        return True
    if any(p in t for p in PROTECTED if len(p) > 4):
        return True
    if INSECT_HINT.search(title or ""):
        return True
    return False


def should_quarantine(title: str) -> tuple[bool, str]:
    """Retourne (move?, reason)."""
    if not title or not title.strip():
        return True, "empty"
    if is_hard_junk(title):
        return True, "junk"
    if _is_protected(title):
        return False, "protected"
    rel = score_relevance(title)
    # hors domaine clair seulement si très bas ET pas d'indice insecte
    if rel < 0.12 and not INSECT_HINT.search(title):
        return True, f"low_rel={rel}"
    if rel < 0.20 and not INSECT_HINT.search(title) and not any(
        w in title.lower() for w in ("wing", "flight", "ecology", "evolution", "mating")
    ):
        return True, f"low_rel={rel}"
    return False, "keep"


def restore_protected() -> dict:
    """Ramène depuis quarantine les nœuds protégés / insecte (faux positifs)."""
    cov = load_coverage()
    nodes = dict(cov.get("nodes") or {})
    quar = load_quarantine()
    restored = []
    still = {}
    for title, info in list((quar.get("nodes") or {}).items()):
        if is_hard_junk(title):
            still[title] = info
            continue
        if _is_protected(title) or (score_relevance(title) >= 0.25 and INSECT_HINT.search(title)):
            # restore
            clean = {k: v for k, v in info.items() if k not in ("quarantined_at", "reason", "prev_quality")}
            nodes[title] = clean or {"depth": 2}
            restored.append(title)
        else:
            still[title] = info
    quar["nodes"] = still
    cov["nodes"] = nodes
    _save_json(COV_PATH, cov)
    save_quarantine(quar)
    rep = {"restored": len(restored), "sample": restored[:20]}
    log_event("triage_restore", rep)
    print(f"[triage] restore_protected: {rep}", flush=True)
    return rep


def run_triage(max_move: int = 80, restore_first: bool = True) -> dict:
    """Trie le graphe actif. Ne supprime aucun fichier wiki."""
    if restore_first:
        restore_protected()

    cov = load_coverage()
    nodes = dict(cov.get("nodes") or {})
    edges = list(cov.get("edges") or [])
    frontier = list(cov.get("frontier") or [])
    quality = _load_json(QUAL_PATH, {})
    quar = load_quarantine()

    candidates_out = []
    kept = {}
    for title, info in nodes.items():
        move, reason = should_quarantine(title)
        if move:
            candidates_out.append((title, info, reason))
        else:
            kept[title] = info

    moved = []
    for title, info, reason in candidates_out[:max_move]:
        quar["nodes"][title] = {
            **(info if isinstance(info, dict) else {}),
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "prev_quality": quality.get(title),
        }
        moved.append({"title": title, "reason": reason})

    still_out = candidates_out[max_move:]
    for title, info, _ in still_out:
        kept[title] = info

    # dédup dans kept
    by_norm = {}
    deduped = 0
    final_kept = {}
    for title, info in sorted(
        kept.items(),
        key=lambda kv: -((quality.get(kv[0]) or {}).get("score") or 0),
    ):
        n = _norm(title)
        if not n:
            continue
        if n in by_norm:
            primary = by_norm[n]
            quar["nodes"][title] = {
                **(info if isinstance(info, dict) else {}),
                "quarantined_at": datetime.now(timezone.utc).isoformat(),
                "reason": f"dedup_of:{primary}",
            }
            quar.setdefault("dedup_map", {})[title] = primary
            deduped += 1
            moved.append({"title": title, "reason": f"dedup_of:{primary}"})
        else:
            by_norm[n] = title
            final_kept[title] = info

    active_edges = []
    archived_edges = []
    for e in edges:
        fr, to = e.get("from"), e.get("to")
        if fr in final_kept and to in final_kept:
            active_edges.append(e)
        else:
            archived_edges.append(e)
    quar.setdefault("edges", [])
    # ne pas exploser le fichier : garder les 2000 dernières arêtes archivées
    quar["edges"] = (quar["edges"] + archived_edges)[-2000:]

    new_frontier = []
    for t in frontier:
        move, _ = should_quarantine(t)
        if move:
            continue
        if _norm(t) in {_norm(x) for x in final_kept}:
            continue
        new_frontier.append(t)

    skills = load_skills()
    skill_cleaned = 0
    for name, sk in skills.items():
        arts = list(sk.get("articles") or [])
        clean, seen = [], set()
        for a in arts:
            if a in quar["nodes"] and not _is_protected(a):
                skill_cleaned += 1
                continue
            if is_hard_junk(a):
                skill_cleaned += 1
                continue
            n = _norm(a)
            if n in seen:
                skill_cleaned += 1
                continue
            seen.add(n)
            clean.append(a)
        sk["articles"] = clean
    save_skills(skills)

    cov["nodes"] = final_kept
    cov["edges"] = active_edges
    cov["frontier"] = new_frontier[:200]
    _save_json(COV_PATH, cov)
    save_quarantine(quar)

    report = {
        "moved_to_quarantine": len(moved),
        "deduped": deduped,
        "active_nodes": len(final_kept),
        "active_edges": len(active_edges),
        "archived_edges": len(archived_edges),
        "frontier": len(new_frontier),
        "skill_articles_removed": skill_cleaned,
        "pending_out_of_domain": len(still_out),
        "sample_moved": moved[:15],
        "note": "Aucun fichier wiki supprimé — triage seulement; protected nodes kept",
    }
    log_event("triage", report)
    print(f"[triage] {report}", flush=True)
    return report
