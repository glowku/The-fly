"""
Auto-learning intelligent :
1. Choisit la skill la plus faible
2. Groq propose des concepts
3. Déduplique (nodes + frontier + similarité)
4. ÉCRIT un vrai article (wiki + quality + coverage) pour 1 concept
5. Ajoute les autres à la frontier
"""
import os
import re
import json
import requests
from difflib import SequenceMatcher

from .memory import (
    load_coverage, load_quality, save_quality, log_event, compute_objective_score,
)
from .skills import load_skills, pick_skill_to_develop, reinforce_skill
from .perception import multi_search, get_summary, search_titles, get_links, get_related
from .planning import register_discovered, register_processed
from .synthesis import synthesize_article
from .evaluation import score_article, is_acceptable, explain_score
from .tools import write_article, git_commit_push

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _already_known(title: str, nodes: dict, frontier: list, quality: dict) -> bool:
    """True si le concept existe déjà ou est trop proche d'un existant."""
    n = _norm(title)
    if not n:
        return True
    for t in list(nodes.keys()) + list(quality.keys()) + list(frontier):
        if _norm(t) == n:
            return True
        if _similar(title, t) >= 0.88:
            return True
    return False


def _groq_suggest(skill_name: str, skill_info: dict, root: str, existing: list) -> list:
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return []

    kws = ", ".join(skill_info.get("keywords", [])[:8])
    existing_s = ", ".join(existing[:25]) if existing else "(aucun)"
    prompt = f"""Tu construis un graphe encyclopédique sur: {root}
Compétence: {skill_name} — {skill_info.get('description','')}
Keywords: {kws}
Déjà dans le wiki (NE PAS resuggestionner): {existing_s}

Propose 8 titres Wikipedia EN ANGLAIS, précis, NON présents dans la liste,
pertinents pour cette compétence ET le sujet racine.
Réponds UNIQUEMENT un JSON array de strings.
Exemple: ["Haltere", "Insect wing", "Compound eye"]"""

    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.35,
                "max_tokens": 400,
            },
            timeout=60,
        )
        if r.status_code != 200:
            print(f"[auto_learn] Groq HTTP {r.status_code}: {r.text[:200]}", flush=True)
            return []
        text = r.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            return []
        return [str(x).strip() for x in json.loads(m.group(0)) if str(x).strip()][:10]
    except Exception as e:
        print(f"[auto_learn] groq error: {e}", flush=True)
        return []


def _fallback(skill_info: dict, root: str) -> list:
    out = []
    for kw in (skill_info.get("keywords") or [])[:4]:
        out += multi_search(f"{root} {kw}", limit_per=3)[:3]
        out += search_titles(kw, limit=3)
    seen = set()
    res = []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res[:12]


def _expand_one(title: str, parent: str | None, skill_name: str) -> bool:
    """Écrit un vrai article wiki pour title. Retourne True si OK."""
    summary = get_summary(title)
    if not summary:
        return False
    title = summary.get("title") or title
    content = synthesize_article(
        title=title,
        summary=summary.get("extract") or "",
        description=summary.get("description") or "",
        parent=parent,
        sources=[summary["url"]] if summary.get("url") else None,
    )
    score = score_article(content)
    print(f"[auto_learn] evaluate {title}: {explain_score(score)}", flush=True)
    if not is_acceptable(score):
        print(f"[auto_learn] reject {title} score={score['score']}", flush=True)
        return False

    write_article(title, content)
    register_processed(title, depth=2, sources=[summary["url"]] if summary.get("url") else [])
    if parent:
        register_discovered(title, depth=2, parent=parent)

    quality = load_quality()
    quality[title] = score
    save_quality(quality)

    # discover children links
    for child in list(set(get_links(title, 20) + get_related(title, 8)))[:10]:
        register_discovered(child, depth=3, parent=title)

    reinforce_skill(skill_name, title, score["score"])
    obj, n_nodes, avg_q = compute_objective_score()
    msg = f"auto_learn: {title} (skill={skill_name} score={score['score']} nodes={n_nodes})"
    git_commit_push([f"wiki/{title}.md", "state/", "DASHBOARD.md"], msg)
    log_event("auto_learn_expand", {
        "title": title, "skill": skill_name,
        "score": score["score"], "objective": obj,
    })
    print(f"[auto_learn] ✅ article créé: {title}", flush=True)
    return True


def run_auto_learn():
    print("=" * 60, flush=True)
    print("[auto_learn] cycle intelligent", flush=True)

    cov = load_coverage()
    quality = load_quality()
    root = cov.get("root") or "Fly"
    nodes = cov.get("nodes") or {}
    frontier = list(cov.get("frontier") or [])

    skills = load_skills()
    skill_name = pick_skill_to_develop()
    skill_info = skills.get(skill_name, {})
    print(f"[auto_learn] skill={skill_name} level={skill_info.get('level', 0)}", flush=True)

    existing = list(nodes.keys()) + list(quality.keys())
    suggestions = _groq_suggest(skill_name, skill_info, root, existing)
    if not suggestions:
        suggestions = _fallback(skill_info, root)
        print(f"[auto_learn] fallback → {suggestions[:5]}", flush=True)
    else:
        print(f"[auto_learn] Groq → {suggestions}", flush=True)

    parent = root if root in nodes else (existing[0] if existing else None)

    # validate + dedupe
    fresh = []
    for title in suggestions:
        s = get_summary(title)
        if not s:
            for h in multi_search(title, limit_per=3)[:2]:
                s = get_summary(h)
                if s:
                    title = s.get("title") or h
                    break
        if not s:
            print(f"[auto_learn] no wiki page: {title}", flush=True)
            continue
        title = s.get("title") or title
        if _already_known(title, nodes, frontier, quality):
            print(f"[auto_learn] skip duplicate/similar: {title}", flush=True)
            continue
        fresh.append(title)

    print(f"[auto_learn] {len(fresh)} concepts nouveaux après dédup", flush=True)

    # 1) expand the first fresh concept into a REAL node
    learned = False
    for title in fresh[:3]:
        if _expand_one(title, parent, skill_name):
            learned = True
            # refresh state after write
            cov = load_coverage()
            nodes = cov.get("nodes") or {}
            quality = load_quality()
            frontier = list(cov.get("frontier") or [])
            break

    # 2) rest → frontier only (not already known)
    added_f = 0
    for title in fresh:
        if _already_known(title, nodes, frontier, quality):
            continue
        register_discovered(title, depth=2, parent=parent)
        frontier.append(title)
        added_f += 1

    log_event("auto_learn", {
        "skill": skill_name,
        "learned": learned,
        "frontier_added": added_f,
        "fresh": fresh[:10],
    })
    print(
        f"[auto_learn] done — article_écrit={learned} frontier+={added_f}",
        flush=True,
    )
    return learned or added_f > 0
