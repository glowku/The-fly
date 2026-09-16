#!/usr/bin/env python3
"""
Worker parallèle : 1 nœud (définition Wikipedia) par cœur CPU.
- modèle Groq le moins cher : openai/gpt-oss-20b
- lit les derniers nœuds + voisinage
- choisit un sous-parent
- expand N titres en parallèle (N = cpu_count, max 4)
- 1 seul git commit/push à la fin
"""
from __future__ import annotations

import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agent.auto_learn import (
    MODEL,
    SKILL_SEEDS,
    _already_known,
    _best_parent_for_skill,
    _candidates_from_frontier,
    _graph_neighborhood,
    _groq_suggest,
    _is_insect_relevant,
    _norm,
    _pick_parent_for_title,
    _recent_nodes,
    _resolve_page,
)
from agent.evaluation import explain_score, is_acceptable, score_article
from agent.memory import (
    compute_objective_score,
    load_coverage,
    load_quality,
    log_event,
    save_quality,
)
from agent.perception import get_links, get_related
from agent.planning import register_discovered, register_processed
from agent.skills import load_skills, pick_skill_to_develop, reinforce_skill
from agent.synthesis import synthesize_article
from agent.tools import git_commit_push, write_article

MAX_WORKERS_CAP = 4


def max_workers() -> int:
    n = os.cpu_count() or 2
    return max(1, min(n, MAX_WORKERS_CAP))


def expand_one_no_git(title: str, parent: str | None, skill_name: str) -> dict:
    result = {
        "title": title,
        "parent": parent,
        "ok": False,
        "score": None,
        "path": None,
        "error": None,
    }
    try:
        canon, summary = _resolve_page(title)
        if not summary:
            result["error"] = "cannot_resolve"
            print(f"[parallel] cannot resolve: {title}", flush=True)
            return result
        title = canon
        result["title"] = title

        content = synthesize_article(
            title=title,
            summary=summary.get("extract") or "",
            description=summary.get("description") or "",
            parent=parent,
            sources=[summary["url"]] if summary.get("url") else None,
        )
        score = score_article(content)
        print(f"[parallel] {explain_score(score)} — {title}", flush=True)
        if not is_acceptable(score):
            result["error"] = f"reject_score={score['score']}"
            print(f"[parallel] reject score={score['score']}", flush=True)
            return result

        path = write_article(title, content)
        result["path"] = path
        result["score"] = score

        parent_depth = 1
        if parent:
            cov = load_coverage()
            info = (cov.get("nodes") or {}).get(parent)
            parent_depth = (info.get("depth", 1) + 1) if info else 2

        register_processed(
            title,
            depth=parent_depth,
            sources=[summary["url"]] if summary.get("url") else [],
        )
        if parent:
            register_discovered(title, depth=parent_depth, parent=parent)

        quality = load_quality()
        quality[title] = score
        save_quality(quality)

        for child in list(set(get_links(title, 12) + get_related(title, 5)))[:8]:
            if _is_insect_relevant(child):
                register_discovered(
                    child, depth=parent_depth + 1, parent=title
                )

        reinforce_skill(skill_name, title, score["score"])
        result["ok"] = True
        print(
            f"[parallel] ✅ {title} ← parent={parent} score={score['score']}",
            flush=True,
        )
        return result
    except Exception as e:
        result["error"] = str(e)
        print(f"[parallel] ERROR {title}: {e}", flush=True)
        traceback.print_exc()
        return result


def build_fresh_candidates(
    skill_name: str,
    skill_info: dict,
    root: str,
    parent: str | None,
    nodes: dict,
    frontier: list,
    quality: dict,
    recent: list[str],
    existing: list,
) -> list[str]:
    neighborhood = _graph_neighborhood(parent, recent, limit=40)
    pool: list[str] = []
    pool += neighborhood
    pool += _candidates_from_frontier(skill_name, frontier)
    pool += _groq_suggest(
        skill_name, skill_info, root, parent, recent, existing
    )
    pool += SKILL_SEEDS.get(skill_name, SKILL_SEEDS["entomologie"])

    seen: set[str] = set()
    ordered: list[str] = []
    for t in pool:
        k = _norm(t)
        if k in seen:
            continue
        seen.add(k)
        ordered.append(t)

    fresh: list[str] = []
    for title in ordered:
        if _already_known(title, nodes, frontier, quality):
            continue
        if not _is_insect_relevant(title):
            continue
        canon, s = _resolve_page(title)
        if not s:
            continue
        if _already_known(canon, nodes, frontier, quality):
            continue
        if not _is_insect_relevant(canon):
            continue
        fresh.append(canon)

    if not fresh and frontier:
        for t in frontier:
            if not _is_insect_relevant(t) or t in nodes:
                continue
            canon, s = _resolve_page(t)
            if (
                s
                and not _already_known(canon, nodes, [], quality)
                and _is_insect_relevant(canon)
            ):
                fresh.append(canon)
                break

    return fresh


def run_parallel_cycle() -> bool:
    print("=" * 60, flush=True)
    workers = max_workers()
    print(
        f"[parallel] cpu={os.cpu_count()} → workers={workers} model={MODEL}",
        flush=True,
    )

    cov = load_coverage()
    quality = load_quality()
    root = cov.get("root") or "Fly"
    nodes = cov.get("nodes") or {}
    frontier = list(cov.get("frontier") or [])

    skill_name = pick_skill_to_develop()
    skills = load_skills()
    skill_info = skills.get(skill_name, {})
    print(
        f"[parallel] skill={skill_name} level={skill_info.get('level', 0)}",
        flush=True,
    )

    existing = list(nodes.keys()) + list(quality.keys())
    recent = _recent_nodes(nodes, limit=12)

    parent = _best_parent_for_skill(skill_name, nodes, cov)
    if not parent:
        parent = root if root in nodes else (
            existing[0] if existing else None
        )

    fresh = build_fresh_candidates(
        skill_name,
        skill_info,
        root,
        parent,
        nodes,
        frontier,
        quality,
        recent,
        existing,
    )
    print(f"[parallel] {len(fresh)} candidats: {fresh[:workers + 2]}", flush=True)

    batch = fresh[:workers]
    if not batch:
        print("[parallel] aucun candidat → stop", flush=True)
        log_event(
            "parallel_learn",
            {"skill": skill_name, "learned": 0, "workers": workers, "parent": parent},
        )
        return False

    jobs = [
        (t, _pick_parent_for_title(t, parent, nodes, cov)) for t in batch
    ]
    print(
        f"[parallel] expand {len(jobs)} nœuds: {[j[0] for j in jobs]}",
        flush=True,
    )

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {
            pool.submit(expand_one_no_git, title, par, skill_name): title
            for title, par in jobs
        }
        for fut in as_completed(futs):
            results.append(fut.result())

    ok_results = [r for r in results if r.get("ok")]
    learned_titles = [r["title"] for r in ok_results]

    cov = load_coverage()
    nodes = cov.get("nodes") or {}
    quality = load_quality()
    frontier = list(cov.get("frontier") or [])

    parent_depth = 1
    if parent and parent in nodes:
        parent_depth = nodes[parent].get("depth", 1) + 1

    already = {_norm(t) for t in learned_titles}
    added_f = 0
    for title in fresh:
        if _norm(title) in already:
            continue
        if _already_known(title, nodes, frontier, quality):
            continue
        if not _is_insect_relevant(title):
            continue
        real_parent = _pick_parent_for_title(title, parent, nodes, cov)
        register_discovered(title, depth=parent_depth, parent=real_parent)
        frontier.append(title)
        added_f += 1
        if added_f >= 6:
            break

    if ok_results:
        paths = [f"wiki/{r['title']}.md" for r in ok_results]
        paths += ["state/", "DASHBOARD.md"]
        obj, n_nodes, _ = compute_objective_score()
        msg = (
            f"parallel_learn: {', '.join(learned_titles)} "
            f"(skill={skill_name} x{len(learned_titles)} "
            f"nodes={n_nodes} obj={obj})"
        )
        git_commit_push(paths, msg)

    log_event(
        "parallel_learn",
        {
            "skill": skill_name,
            "learned": len(learned_titles),
            "titles": learned_titles,
            "workers": workers,
            "cpu": os.cpu_count(),
            "frontier_added": added_f,
            "parent": parent,
            "recent": recent[:8],
        },
    )
    print(
        f"[parallel] done — articles={len(learned_titles)} {learned_titles} "
        f"frontier+={added_f} workers={workers} parent={parent}",
        flush=True,
    )
    return len(learned_titles) > 0 or added_f > 0


def main():
    start = time.time()
    try:
        ok = run_parallel_cycle()
        print(
            f"[parallel] cycle {'OK' if ok else 'empty'} "
            f"en {time.time() - start:.1f}s",
            flush=True,
        )
        sys.exit(0)
    except Exception as e:
        print(f"[parallel] FATAL: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
