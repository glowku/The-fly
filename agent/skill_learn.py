"""
Skill learning ANCRÉ Wikipédia (comme auto_learn d'origine).

1. Choisit un skill sous-développé
2. Cherche des titres wiki par mots-clés / résonance
3. Filtre junk + score_relevance
4. Synthétise un article depuis le résumé Wikipedia
5. Attache au graphe + reinforce_skill

Plus de notes purement hallucinées par le LLM sur des topics inventés.
"""
from __future__ import annotations

import os
import re
from difflib import SequenceMatcher

from .memory import (
    load_coverage,
    load_quality,
    save_quality,
    log_event,
    compute_objective_score,
)
from .skills import (
    load_skills,
    save_skills,
    reinforce_skill,
    score_relevance,
    is_hard_junk,
    pick_skill_to_develop,
)
from .perception import get_summary, search_titles, get_links, get_related
from .planning import register_discovered, register_processed
from .synthesis import synthesize_article
from .evaluation import score_article, is_acceptable, explain_score
from .tools import write_article, git_commit_push

# Seeds Wikipedia par skill — vrais titres / requêtes de recherche
SKILL_WIKI_QUERIES = {
    "entomologie": [
        "Diptera", "Entomology", "Housefly", "Fruit fly", "Hoverfly",
        "Blowfly", "Tachinidae", "Mosquito", "Insect", "True flies",
    ],
    "anatomie_insecte": [
        "Insect morphology", "Haltere", "Compound eye", "Insect wing",
        "Exoskeleton", "Insect mouthparts", "Spiracle", "Arthropod leg",
        "Thorax", "Antenna (biology)", "Labellum",
    ],
    "vol_et_aerodynamique": [
        "Insect flight", "Haltere", "Aerodynamics", "Wing", "Hovering",
        "Flight", "Wing loading", "Clap and fling", "Reynolds number",
    ],
    "ecologie": [
        "Insect ecology", "Pollination", "Parasitoid", "Larva", "Maggot",
        "Decomposer", "Biological pest control", "Myiasis",
    ],
    "evolution": [
        "Evolution of insects", "Paleoptera", "Neoptera", "Devonian",
        "Adaptive radiation", "Coevolution", "Insect evolution",
    ],
    "comportement": [
        "Insect behavior", "Swarm behaviour", "Courtship", "Foraging",
        "Mimicry", "Mating", "Eusociality",
    ],
    "code_et_outils": [
        "Software architecture", "Application programming interface",
        "Version control", "Continuous integration", "Python (programming language)",
        "JSON", "Graph theory", "Retrieval-augmented generation",
    ],
    "securite_defensive": [
        "Input validation", "Secure coding", "Principle of least privilege",
        "Secret management", "Cross-origin resource sharing",
        "Supply chain security", "Dependency management",
    ],
    "recherche_web": [
        "Information retrieval", "Web search engine", "Citation",
        "Peer review", "Wikipedia", "arXiv",
    ],
    "recherche_image": [
        "Scientific visualization", "Diagram", "Morphology (biology)",
        "Micrograph", "Technical drawing",
    ],
    "raisonnement": [
        "Knowledge graph", "Semantic network", "Inference",
        "Ontology (information science)", "Reasoning",
    ],
    "representation": [
        "Graph drawing", "Data visualization", "Force-directed graph drawing",
        "Network theory", "Scientific visualization",
    ],
}

# skills techniques : on accepte wiki non-insecte si le skill le demande
TECH_SKILLS = {
    "code_et_outils", "securite_defensive", "recherche_web",
    "recherche_image", "raisonnement", "representation",
}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _ensure_skills():
    skills = load_skills()
    changed = False
    for name, queries in SKILL_WIKI_QUERIES.items():
        if name not in skills:
            skills[name] = {
                "level": 0.4,
                "description": f"Skill {name}",
                "keywords": [q.split()[0].lower() for q in queries[:6]],
                "articles": [],
            }
            changed = True
    if changed:
        save_skills(skills)
    return skills


def _already(title: str, nodes: dict, quality: dict) -> bool:
    n = _norm(title)
    for t in list(nodes.keys()) + list(quality.keys()):
        if _norm(t) == n or _similar(title, t) >= 0.90:
            return True
    return False


def _resonance(title: str, skill_name: str, skill_info: dict) -> float:
    """Score de résonance titre ↔ skill (mots-clés + queries)."""
    if is_hard_junk(title):
        return 0.0
    t = title.lower()
    score = 0.0
    for kw in skill_info.get("keywords") or []:
        if kw.lower() in t:
            score += 0.35
    for q in SKILL_WIKI_QUERIES.get(skill_name, []):
        ql = q.lower()
        if _norm(q) == _norm(title):
            score += 1.0
        elif ql in t or t in ql:
            score += 0.5
        else:
            score += 0.15 * _similar(q, title)
    # boost domaine insecte pour skills biologiques
    if skill_name not in TECH_SKILLS:
        score += score_relevance(title) * 0.8
    else:
        # tech: éviter pure insecte hors sujet sauf si mot-clé match
        if score_relevance(title) > 0.5 and score < 0.3:
            score *= 0.5
    return round(score, 3)


def _search_pool(skill_name: str, skill_info: dict) -> list[str]:
    pool = []
    queries = list(SKILL_WIKI_QUERIES.get(skill_name, []))
    # requêtes dérivées des keywords
    for kw in (skill_info.get("keywords") or [])[:5]:
        queries.append(kw)
    seen = set()
    for q in queries:
        # titre exact seed
        if _norm(q) not in seen:
            pool.append(q)
            seen.add(_norm(q))
        try:
            hits = search_titles(q, limit=6)
        except Exception:
            hits = []
        for h in hits:
            k = _norm(h)
            if k in seen or is_hard_junk(h):
                continue
            seen.add(k)
            pool.append(h)
    # voisinage graphe si parent skill
    cov = load_coverage()
    nodes = cov.get("nodes") or {}
    for art in (skill_info.get("articles") or [])[-5:]:
        if art not in nodes:
            continue
        try:
            for h in get_links(art, 12) + get_related(art, 6):
                k = _norm(h)
                if k in seen or is_hard_junk(h):
                    continue
                seen.add(k)
                pool.append(h)
        except Exception:
            pass
    return pool


def _resolve(title: str):
    if is_hard_junk(title):
        return None, None
    s = get_summary(title)
    if s and len(s.get("extract") or "") > 50:
        return s.get("title") or title, s
    for h in search_titles(title, limit=4):
        if is_hard_junk(h):
            continue
        s = get_summary(h)
        if s and len(s.get("extract") or "") > 50:
            return s.get("title") or h, s
    return None, None


def _pick_parent(title: str, skill_name: str, nodes: dict, cov: dict):
    skills = load_skills()
    arts = skills.get(skill_name, {}).get("articles") or []
    for a in reversed(arts):
        if a in nodes:
            try:
                links = set(get_links(a, 20))
                if any(_norm(x) == _norm(title) or _similar(x, title) >= 0.9 for x in links):
                    return a
            except Exception:
                pass
            return a
    root = cov.get("root") or "Fly"
    return root if root in nodes else (next(iter(nodes), None))


def run_skill_learn(force_skill: str | None = None, force_topic: str | None = None) -> dict:
    """Un cycle : Wikipedia → article → skill reinforce."""
    print("[skill_learn] Wikipedia resonance cycle", flush=True)
    skills = _ensure_skills()
    skill_name = force_skill if force_skill in skills else pick_skill_to_develop()
    # préférer un skill avec queries wiki
    if skill_name not in SKILL_WIKI_QUERIES:
        skill_name = min(
            SKILL_WIKI_QUERIES.keys(),
            key=lambda k: skills.get(k, {}).get("level", 0),
        )
    skill_info = skills.get(skill_name, {})
    print(f"[skill_learn] skill={skill_name} level={skill_info.get('level')}", flush=True)

    cov = load_coverage()
    nodes = cov.get("nodes") or {}
    quality = load_quality()

    pool = _search_pool(skill_name, skill_info)
    if force_topic:
        pool = [force_topic] + pool

    ranked = []
    for t in pool:
        res = _resonance(t, skill_name, skill_info)
        if res < 0.25:
            continue
        ranked.append((res, t))
    ranked.sort(reverse=True)

    print(f"[skill_learn] pool ranked: {[(r, t) for r, t in ranked[:10]]}", flush=True)

    learned = None
    for res, title in ranked[:12]:
        if _already(title, nodes, quality):
            continue
        # insect skills: exiger un minimum domaine
        if skill_name not in TECH_SKILLS and score_relevance(title) < 0.28 and res < 0.6:
            continue
        canon, summary = _resolve(title)
        if not summary:
            continue
        if _already(canon, nodes, quality):
            continue
        if is_hard_junk(canon):
            continue
        if skill_name not in TECH_SKILLS and score_relevance(canon, summary.get("extract") or "") < 0.25:
            if _resonance(canon, skill_name, skill_info) < 0.55:
                print(f"[skill_learn] skip low domain: {canon}", flush=True)
                continue

        parent = _pick_parent(canon, skill_name, nodes, cov)
        content = synthesize_article(
            title=canon,
            summary=summary.get("extract") or "",
            description=summary.get("description") or "",
            parent=parent,
            sources=[summary["url"]] if summary.get("url") else None,
        )
        score = score_article(content)
        print(f"[skill_learn] {explain_score(score)} — {canon} (res={res})", flush=True)
        if not is_acceptable(score):
            continue

        write_article(canon, content)
        parent_depth = 1
        if parent and parent in nodes:
            parent_depth = nodes[parent].get("depth", 1) + 1
        register_processed(
            canon,
            depth=parent_depth,
            sources=[summary["url"]] if summary.get("url") else [],
        )
        if parent:
            register_discovered(canon, depth=parent_depth, parent=parent)

        quality[canon] = score
        save_quality(quality)

        # frontier enfants wiki
        try:
            for child in list(set(get_links(canon, 10) + get_related(canon, 5)))[:8]:
                if is_hard_junk(child):
                    continue
                if skill_name not in TECH_SKILLS and score_relevance(child) < 0.3:
                    continue
                register_discovered(child, depth=parent_depth + 1, parent=canon)
        except Exception:
            pass

        reinforce_skill(skill_name, canon, score["score"])
        obj, n_nodes, _ = compute_objective_score()
        msg = f"skill_learn: {canon} (skill={skill_name} res={res} score={score['score']})"
        try:
            git_commit_push([f"wiki/{canon}.md", "state/", "DASHBOARD.md"], msg)
        except Exception as e:
            print(f"[skill_learn] push skip: {e}", flush=True)

        learned = {
            "ok": True,
            "skill": skill_name,
            "title": canon,
            "resonance": res,
            "score": score["score"],
            "parent": parent,
            "nodes": n_nodes,
            "source": "wikipedia",
            "new": True,
        }
        log_event("skill_learn_wiki", learned)
        print(f"[skill_learn] ✅ wiki {canon} ← skill={skill_name}", flush=True)
        return learned

    # rien de nouveau : au moins renforcer via un seed déjà connu
    for res, title in ranked[:5]:
        canon, summary = _resolve(title)
        if canon:
            reinforce_skill(skill_name, canon, 30)
            return {
                "ok": True,
                "skill": skill_name,
                "title": canon,
                "resonance": res,
                "new": False,
                "source": "wikipedia_reinforce_only",
            }

    print("[skill_learn] aucun candidat wiki frais", flush=True)
    return {"ok": False, "skill": skill_name, "new": False, "source": "wikipedia"}


# compat anciens imports
SKILL_TRACKS = {k: {"topics": v, "keywords": []} for k, v in SKILL_WIKI_QUERIES.items()}
