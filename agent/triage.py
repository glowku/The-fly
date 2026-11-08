"""
Triage du graphe — TRIER, pas effacer.

- Déplace les nœuds junk / hors-domaine vers state/quarantine.json
- Retire les arêtes actives liées (archivées dans quarantine)
- Déduplique titres quasi-identiques (garde le meilleur score qualité)
- Nettoie skills.json articles (liste active vs quarantaine)
- Les fichiers wiki/*.md restent sur disque (rien n'est supprimé)
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .memory import STATE_DIR, load_coverage, log_event
from .skills import load_skills, save_skills, is_hard_junk, score_relevance, is_domain_node

COV_PATH = STATE_DIR / "coverage.json"
QUAL_PATH = STATE_DIR / "quality.json"
QUAR_PATH = STATE_DIR / "quarantine.json"


def _load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def _save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _norm(s: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def load_quarantine() -> dict:
    return _load_json(QUAR_PATH, {"nodes": {}, "edges": [], "dedup_map": {}, "updated_at": None})


def save_quarantine(q: dict):
    q["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_json(QUAR_PATH, q)


def run_triage(max_move: int = 80) -> dict:
    """Trie le graphe actif. Ne supprime aucun fichier wiki."""
    cov = load_coverage()
    nodes = dict(cov.get("nodes") or {})
    edges = list(cov.get("edges") or [])
    frontier = list(cov.get("frontier") or [])
    quality = _load_json(QUAL_PATH, {})
    quar = load_quarantine()

    moved = []
    kept = {}
    # 1) score chaque nœud
    for title, info in nodes.items():
        extract = ""
        # quality extract not always present
        junk = is_hard_junk(title)
        rel = score_relevance(title)
        domain = is_domain_node(title) and rel >= 0.35 and not junk
        if not domain:
            reason = "junk" if junk else f"low_rel={rel}"
            quar["nodes"][title] = {
                **(info if isinstance(info, dict) else {}),
                "quarantined_at": datetime.now(timezone.utc).isoformat(),
                "reason": reason,
                "prev_quality": quality.get(title),
            }
            moved.append({"title": title, "reason": reason})
            if len(moved) >= max_move:
                # still must keep remaining as-is for this pass
                kept[title] = info
                # actually if we hit max, keep rest active without re-check... better continue classifying but only move max
        else:
            kept[title] = info

    # fix: above logic is wrong when max_move hits. Rewrite cleaner.
    moved = []
    kept = {}
    candidates_out = []
    for title, info in nodes.items():
        junk = is_hard_junk(title)
        rel = score_relevance(title)
        domain = (not junk) and is_domain_node(title) and rel >= 0.35
        if not domain:
            candidates_out.append((title, info, "junk" if junk else f"low_rel={rel}"))
        else:
            kept[title] = info

    for title, info, reason in candidates_out[:max_move]:
        quar["nodes"][title] = {
            **(info if isinstance(info, dict) else {}),
            "quarantined_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "prev_quality": quality.get(title),
        }
        moved.append({"title": title, "reason": reason})

    still_out = {t for t, _, _ in candidates_out[max_move:]}
    for title, info, _ in candidates_out[max_move:]:
        kept[title] = info  # report later as pending

    # 2) dédup dans kept
    by_norm = {}
    deduped = 0
    final_kept = {}
    for title, info in sorted(kept.items(), key=lambda kv: -((quality.get(kv[0]) or {}).get("score") or 0)):
        n = _norm(title)
        if not n:
            continue
        if n in by_norm:
            # archive le doublon, garde le premier (meilleure qualité)
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

    # 3) edges : actives seulement si both ends in final_kept
    active_edges = []
    archived_edges = []
    for e in edges:
        fr, to = e.get("from"), e.get("to")
        if fr in final_kept and to in final_kept:
            active_edges.append(e)
        else:
            archived_edges.append(e)
    quar.setdefault("edges", [])
    quar["edges"].extend(archived_edges)

    # 4) frontier nettoyée
    new_frontier = []
    for t in frontier:
        if is_hard_junk(t):
            continue
        if score_relevance(t) < 0.32:
            continue
        if _norm(t) in {_norm(x) for x in final_kept}:
            continue
        new_frontier.append(t)

    # 5) skills.articles — retirer titres quarantaine, garder trace
    skills = load_skills()
    skill_cleaned = 0
    for name, sk in skills.items():
        arts = list(sk.get("articles") or [])
        clean = []
        for a in arts:
            if a in quar["nodes"] or is_hard_junk(a) or score_relevance(a) < 0.30:
                skill_cleaned += 1
                continue
            clean.append(a)
        # dédup articles skill
        seen = set()
        uniq = []
        for a in clean:
            n = _norm(a)
            if n in seen:
                skill_cleaned += 1
                continue
            seen.add(n)
            uniq.append(a)
        sk["articles"] = uniq
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
        "note": "Aucun fichier wiki supprimé — triage seulement",
    }
    log_event("triage", report)
    print(f"[triage] {report}", flush=True)
    return report
