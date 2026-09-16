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
from agent.perception import get_summary, get_links, get_related, resolve_title, search_titles, multi_search
from agent.planning import pick_next_target, register_discovered, register_processed
from agent.synthesis import synthesize_article
from agent.evaluation import score_article, is_acceptable, explain_score
from agent.tools import write_article, git_commit_push
from agent.skills import reinforce_skill, load_skills


def _seed_skill_branches(root_title: str):
    """Sème la frontière avec des concepts multi-mots par skill."""
    skills = load_skills()
    seeded = 0
    for skill_name, info in skills.items():
        kws = info.get("keywords") or []
        queries = [root_title]
        if kws:
            queries.append(f"{root_title} {kws[0]}")
            if len(kws) > 1:
                queries.append(f"{kws[0]} {kws[1]}")
            queries.append(kws[0])
        for q in queries[:4]:
            hits = multi_search(q, limit_per=3)
            for h in hits[:3]:
                register_discovered(h, depth=2, parent=root_title)
                seeded += 1
                if seeded >= 24:
                    return seeded
    return seeded


def run_cycle(dry_run: bool = False):
    print("=" * 60, flush=True)
    print("[agent] Démarrage du cycle autonome", flush=True)

    target = pick_next_target()
    title = target["title"]
    action = target["action"]
    print(
        f"[plan] {target['reason']} → « {title} » "
        f"(action={action}, prio={target.get('priority')}, skill={target.get('skill')})",
        flush=True,
    )

    resolved = resolve_title(title)
    if resolved and resolved != title:
        print(f"[perceive] titre résolu: « {title} » → « {resolved} »", flush=True)
        cov = load_coverage()
        if not cov.get("nodes") and cov.get("root") == title:
            cov["root"] = resolved
            save_coverage(cov)
        title = resolved

    summary = get_summary(title)
    if not summary:
        print(f"[perceive] Aucun résumé utilisable pour « {title} » → skip", flush=True)
        cov = load_coverage()
        cov["frontier"] = [t for t in cov.get("frontier", []) if t != title and t != target["title"]]
        if not cov.get("nodes"):
            for w in (cov.get("root") or title).replace("-", " ").split():
                if len(w) < 3:
                    continue
                for h in search_titles(w, limit=5):
                    register_discovered(h, depth=1, parent=None)
            print("[perceive] frontière seedée depuis recherche", flush=True)
        save_coverage(load_coverage())
        log_event("skip", {"title": title, "reason": "no_summary"})
        return False

    extract_len = len(summary.get("extract") or "")
    print(f"[perceive] Résumé OK ({extract_len} chars) — {summary.get('description', '')[:80]}", flush=True)
    title = summary.get("title") or title

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

    content = synthesize_article(
        title=title,
        summary=summary.get("extract") or "",
        description=summary.get("description") or "",
        parent=parent,
        sources=[summary["url"]] if summary.get("url") else None,
    )
    print(f"[act] Article généré ({len(content)} chars)", flush=True)

    score = score_article(content)
    print(f"[evaluate] {explain_score(score)}", flush=True)

    if not is_acceptable(score):
        print(f"[reflect] Score trop bas ({score['score']}) → rejet", flush=True)
        log_event("reject", {"title": title, "score": score["score"], "metrics": score.get("metrics")})
        links = get_links(title, limit=20)
        related = get_related(title, limit=8)
        for child in list(set(links + related))[:12]:
            register_discovered(child, depth + 1, parent=title)
        return False

    path = write_article(title, content)
    print(f"[act] Écrit → {path}", flush=True)

    links = get_links(title, limit=35)
    related = get_related(title, limit=12)
    discovered = list(set(links + related))[:22]
    for child in discovered:
        register_discovered(child, depth + 1, parent=title)

    cov_now = load_coverage()
    if len(cov_now.get("nodes", {})) <= 1:
        nseed = _seed_skill_branches(title)
        print(f"[skill-seed] {nseed} concepts ajoutés à la frontière (branches)", flush=True)

    register_processed(
        title,
        depth,
        sources=[summary["url"]] if summary.get("url") else [],
    )

    quality = load_quality()
    quality[title] = score
    save_quality(quality)

    skill_name = target.get("skill")
    if skill_name:
        reinforce_skill(skill_name, title, score["score"])
        print(f"[skill] {skill_name} renforcée grâce à « {title} »", flush=True)

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
    print(f"[commit] {'✅' if ok else '❌'} {msg}", flush=True)

    log_event("expand", {
        "title": title,
        "score": score["score"],
        "depth": depth,
        "discovered": len(discovered),
        "objective": obj,
        "skill": skill_name,
    })
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="The Fly Autonomous Knowledge Agent")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_cycle(dry_run=args.dry_run)
    sys.exit(0)
