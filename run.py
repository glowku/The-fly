#!/usr/bin/env python3
"""Cycle principal de l'agent : Perceive → Plan → Act → Evaluate → Reflect."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agent.memory import (
    load_coverage,
    save_coverage,
    load_quality,
    save_quality,
    log_event,
    compute_objective_score,
)
from agent.perception import get_summary, get_links, get_related
from agent.planning import pick_next_target, register_discovered, register_processed
from agent.synthesis import synthesize_article
from agent.evaluation import score_article, is_acceptable, explain_score
from agent.tools import write_article, git_commit_push


def run_cycle(dry_run: bool = False):
    """Exécute un cycle complet de l'agent."""
    print("=" * 60, flush=True)
    print("[agent] Démarrage du cycle autonome", flush=True)

    # 1. PLAN
    target = pick_next_target()
    title = target["title"]
    action = target["action"]
    print(f"[plan] {target['reason']} → « {title} » (action={action}, prio={target.get('priority')})", flush=True)

    # 2. PERCEIVE
    summary = get_summary(title)
    if not summary:
        print(f"[perceive] Aucun résumé utilisable pour « {title} » → skip", flush=True)
        cov = load_coverage()
        cov["frontier"] = [t for t in cov.get("frontier", []) if t != title]
        save_coverage(cov)
        log_event("skip", {"title": title, "reason": "no_summary"})
        return False

    extract_len = len(summary.get("extract") or "")
    print(f"[perceive] Résumé OK ({extract_len} chars) — {summary.get('description', '')[:80]}", flush=True)

    # Déterminer profondeur et parent
    cov = load_coverage()
    parent = None
    depth = 1
    if title in cov.get("nodes", {}):
        depth = cov["nodes"][title].get("depth", 1)
    else:
        for edge in cov.get("edges", []):
            if edge.get("to") == title and edge.get("from") in cov.get("nodes", {}):
                depth = cov["nodes"][edge["from"]].get("depth", 0) + 1
                parent = edge["from"]
                break
        if parent is None and cov.get("nodes"):
            parent = cov.get("root")
            depth = 1

    # 3. ACT — Synthèse
    content = synthesize_article(
        title=title,
        summary=summary.get("extract") or "",
        description=summary.get("description") or "",
        parent=parent,
        sources=[summary["url"]] if summary.get("url") else None,
    )
    print(f"[act] Article généré ({len(content)} chars)", flush=True)

    # 4. EVALUATE
    score = score_article(content)
    print(f"[evaluate] {explain_score(score)}", flush=True)

    if not is_acceptable(score):
        print(f"[reflect] Score trop bas ({score['score']}) → rejet, pas de commit", flush=True)
        log_event("reject", {
            "title": title,
            "score": score["score"],
            "metrics": score.get("metrics"),
        })
        # Même rejeté, on découvre des liens
        links = get_links(title, limit=20)
        related = get_related(title, limit=8)
        for child in list(set(links + related))[:12]:
            register_discovered(child, depth + 1, parent=title)
        return False

    # 5. WRITE + DISCOVER
    path = write_article(title, content)
    print(f"[act] Écrit → {path}", flush=True)

    links = get_links(title, limit=35)
    related = get_related(title, limit=12)
    discovered = list(set(links + related))[:22]
    for child in discovered:
        register_discovered(child, depth + 1, parent=title)

    register_processed(
        title,
        depth,
        sources=[summary["url"]] if summary.get("url") else [],
    )

    quality = load_quality()
    quality[title] = score
    save_quality(quality)

    # 6. REFLECT / COMMIT
    obj, n_nodes, avg_q = compute_objective_score()
    msg = f"wiki: {title} (score {score['score']}/10 | nodes={n_nodes} obj={obj})"
    print(f"[reflect] Objectif actuel = {obj} (nodes={n_nodes}, avg_q={avg_q})", flush=True)

    if dry_run:
        print(f"[dry-run] Commit simulé : {msg}", flush=True)
        log_event("expand_dry", {"title": title, "score": score["score"], "depth": depth})
        return True

    ok = git_commit_push(
        [f"wiki/{title}.md", "state/", "DASHBOARD.md"],
        msg,
    )
    print(f"[commit] {'✅' if ok else '❌ (rien ou erreur)'} {msg}", flush=True)

    log_event("expand", {
        "title": title,
        "score": score["score"],
        "depth": depth,
        "discovered": len(discovered),
        "objective": obj,
    })
    return ok


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="The Fly Autonomous Knowledge Agent")
    parser.add_argument("--dry-run", action="store_true", help="Ne pas committer")
    args = parser.parse_args()
    success = run_cycle(dry_run=args.dry_run)
    sys.exit(0 if success else 1)
