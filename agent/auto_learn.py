"""
Auto-learning :
- lit les DERNIERS nœuds + leurs liens Wikipedia (voisinage du graphe)
- choisit un sous-parent (feuille / peu d'enfants)
- priorise les liens du parent et du voisinage récent
- Groq guidé par parent + contexte graphe
- seeds en dernier recours
- filtre insecte + anti-junk
- depth = parent.depth + 1
- 1 article par cycle rattaché au bon parent
"""
import os
import re
import json
import requests
from difflib import SequenceMatcher
from datetime import datetime

from .memory import (
    load_coverage,
    load_quality,
    save_quality,
    log_event,
    compute_objective_score,
)
from .skills import (
    load_skills,
    pick_skill_to_develop,
    reinforce_skill,
    score_relevance,
)
from .perception import get_summary, search_titles, get_links, get_related
from .planning import register_discovered, register_processed
from .synthesis import synthesize_article
from .evaluation import score_article, is_acceptable, explain_score
from .tools import write_article, git_commit_push

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"

SKILL_SEEDS = {
    "entomologie": [
        "Diptera", "Insect", "Fly", "Housefly", "Fruit fly", "Mosquito",
        "Hoverfly", "Blowfly", "Tachinidae", "Entomology",
    ],
    "anatomie_insecte": [
        "Insect morphology", "Insect wing", "Haltere", "Compound eye",
        "Exoskeleton", "Antenna (biology)", "Thorax", "Arthropod leg",
        "Spiracle", "Insect mouthparts",
    ],
    "vol_et_aerodynamique": [
        "Insect flight", "Haltere", "Insect wing", "Aerodynamics",
        "Hovering", "Wing", "Flight", "Diptera",
    ],
    "ecologie": [
        "Insect ecology", "Pollination", "Larva", "Maggot",
        "Parasitoid", "Decomposer", "Insecticide", "Biological pest control",
    ],
    "evolution": [
        "Evolution of insects", "Insect evolution", "Devonian",
        "Paleoptera", "Neoptera", "Adaptive radiation", "Coevolution",
    ],
    "comportement": [
        "Insect behavior", "Swarm behaviour", "Mating", "Courtship",
        "Foraging", "Eusociality", "Mimicry",
    ],
}

JUNK_RE = re.compile(
    r"(tv series|album|film|song|band|airline|aircraft|institute|"
    r"wuornos|chun|password|malware|software|episode|novel|game|"
    r"arxiv|academic press|publisher|isbn|doi|"
    r"computer security|cybersecurity|encryption|"
    r"angular velocity|angular momentum)",
    re.I,
)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _is_junk(title: str) -> bool:
    if not title or len(title) < 2:
        return True
    return bool(JUNK_RE.search(title))


def _is_insect_relevant(title: str) -> bool:
    if _is_junk(title):
        return False
    t = (title or "").lower()
    strong = (
        "insect", "fly", "flies", "diptera", "mosquito", "larva", "maggot",
        "wing", "halter", "flight", "hover", "swarm", "pollinat",
        "entomolog", "arthropod", "thorax", "antenna", "exoskeleton",
        "parasitoid", "mimicry", "neoptera", "paleoptera", "devonian",
        "compound eye", "spiracle", "mouthpart", "blowfly", "hoverfly",
        "tachinid", "apterygota", "alate", "wingbeat", "aerodynamic",
        "courtship", "foraging", "mating", "eusocial", "decomposer",
        "pest control", "insecticide", "pollination", "morphology",
        "ecology", "evolution", "behaviour", "behavior",
    )
    if any(s in t for s in strong):
        return True
    for seeds in SKILL_SEEDS.values():
        for seed in seeds:
            if _norm(seed) == _norm(title) or _similar(seed, title) >= 0.9:
                return True
    skills = load_skills()
    for sk in skills.values():
        for kw in sk.get("keywords", []):
            if kw.lower() in t:
                return True
    return score_relevance(title) >= 0.18


def _already_known(title: str, nodes: dict, frontier: list, quality: dict) -> bool:
    n = _norm(title)
    if not n:
        return True
    for t in list(nodes.keys()) + list(quality.keys()) + list(frontier):
        if _norm(t) == n or _similar(title, t) >= 0.88:
            return True
    return False


def _resolve_page(title: str):
    if _is_junk(title):
        return None, None
    s = get_summary(title)
    if s and len(s.get("extract") or "") > 60:
        return s.get("title") or title, s
    for h in search_titles(title, limit=5):
        if _is_junk(h):
            continue
        s = get_summary(h)
        if s and len(s.get("extract") or "") > 60:
            return s.get("title") or h, s
    return None, None


def _recent_nodes(nodes: dict, limit: int = 12) -> list[str]:
    """Derniers nœuds créés (par created_at), pour comprendre le graphe."""
    items = []
    for title, info in nodes.items():
        ts = info.get("created_at") or info.get("updated_at") or ""
        items.append((ts, title))
    items.sort(reverse=True)
    recent = [t for _, t in items[:limit]]
    print(f"[auto_learn] derniers nœuds: {recent[:8]}", flush=True)
    return recent


def _graph_neighborhood(parent: str | None, recent: list[str], limit: int = 40) -> list[str]:
    """
    Récupère les liens Wikipedia des derniers nœuds + du parent
    → le 'complément' pour comprendre les mots et leurs relations.
    """
    sources = []
    if parent:
        sources.append(parent)
    sources.extend(recent[:8])

    seen = set()
    neigh = []
    for src in sources:
        try:
            links = get_links(src, 20) + get_related(src, 8)
        except Exception:
            links = []
        for t in links:
            k = _norm(t)
            if not k or k in seen:
                continue
            if not _is_insect_relevant(t):
                continue
            seen.add(k)
            neigh.append(t)
            if len(neigh) >= limit:
                break
        if len(neigh) >= limit:
            break

    print(
        f"[auto_learn] voisinage graphe ({len(sources)} sources) "
        f"→ {len(neigh)} titres pertinents",
        flush=True,
    )
    return neigh


def _groq_suggest(
    skill_name: str,
    skill_info: dict,
    root: str,
    parent: str | None,
    recent: list[str],
    existing: list,
) -> list:
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        print("[auto_learn] GROQ_API_KEY missing", flush=True)
        return []

    kws = ", ".join(skill_info.get("keywords", [])[:8])
    existing_s = ", ".join(existing[:20]) if existing else "(none)"
    recent_s = ", ".join(recent[:10]) if recent else "(none)"
    parent_line = (
        f"Parent to expand under: « {parent} ». "
        "Suggest ONLY real sub-topics of this parent."
        if parent
        else ""
    )
    prompt = f"""You expand a knowledge graph about insects/flies: {root}
Skill: {skill_name} — {skill_info.get('description', '')}
Keywords: {kws}
Recent nodes in the graph: {recent_s}
{parent_line}
Already in wiki — DO NOT suggest these: {existing_s}

Return ONLY a valid JSON array of 8 real English Wikipedia article titles.
Focus on insects, flies, diptera, and direct children of the parent.
No markdown, no text outside the JSON array.
Example: ["Haltere", "Insect wing", "Compound eye"]"""

    try:
        r = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.35,
                "max_tokens": 400,
            },
            timeout=60,
        )
        if r.status_code != 200:
            print(
                f"[auto_learn] Groq HTTP {r.status_code}: {r.text[:250]}",
                flush=True,
            )
            return []
        text = r.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        m = re.search(r"\[[\s\S]*?\]", text)
        if not m:
            print(f"[auto_learn] Groq bad JSON: {text[:200]}", flush=True)
            return []
        raw = re.sub(r",\s*]", "]", m.group(0))
        items = [
            str(x).strip()
            for x in json.loads(raw)
            if str(x).strip()
        ]
        print(f"[auto_learn] Groq OK → {items}", flush=True)
        return items[:10]
    except Exception as e:
        print(f"[auto_learn] Groq error: {e}", flush=True)
        return []


def _candidates_from_frontier(skill_name: str, frontier: list) -> list:
    scored = []
    skills = load_skills()
    kws = skills.get(skill_name, {}).get("keywords") or []
    for t in frontier:
        if not _is_insect_relevant(t):
            continue
        rel = score_relevance(t)
        bonus = sum(1 for k in kws if k.lower() in t.lower()) * 0.25
        scored.append((rel + bonus, t))
    scored.sort(reverse=True)
    return [t for s, t in scored if s >= 0.12][:8]


def _best_parent_for_skill(
    skill_name: str, nodes: dict, cov: dict
) -> str | None:
    skills = load_skills()
    skill = skills.get(skill_name, {})
    skill_articles = set(skill.get("articles", []))
    keywords = [k.lower() for k in skill.get("keywords", [])]

    children_count: dict[str, int] = {}
    for e in cov.get("edges", []):
        fr = e.get("from")
        if fr:
            children_count[fr] = children_count.get(fr, 0) + 1

    candidates = []
    for title, info in nodes.items():
        n_kids = children_count.get(title, 0)
        is_skill = title in skill_articles or any(
            kw in title.lower() for kw in keywords
        )
        score = 0.0
        if n_kids == 0:
            score += 100
        elif n_kids < 3:
            score += 50 - n_kids * 12
        else:
            score -= 25
        if is_skill:
            score += 70
        depth = info.get("depth", 1)
        score += max(0, 10 - abs(depth - 2) * 2)
        candidates.append((score, title, n_kids, is_skill))

    if not candidates:
        return cov.get("root") or "Fly"

    candidates.sort(key=lambda x: x[0], reverse=True)
    best_score, best_title, n_kids, is_skill = candidates[0]
    print(
        f"[auto_learn] parent choisi: {best_title} "
        f"(score={best_score:.0f} kids={n_kids} skill={is_skill})",
        flush=True,
    )
    return best_title


def _pick_parent_for_title(
    title: str, preferred: str | None, nodes: dict, cov: dict
) -> str | None:
    """
    Si le titre est un lien du preferred → garder preferred.
    Sinon essayer de trouver un nœud existant qui linke vers ce titre.
    Sinon preferred / root.
    """
    if preferred:
        try:
            links = set(get_links(preferred, 30) + get_related(preferred, 10))
            if any(_norm(x) == _norm(title) or _similar(x, title) >= 0.9 for x in links):
                return preferred
        except Exception:
            pass

    # chercher un parent déjà dans le graphe via edges
    for e in cov.get("edges", []):
        if _norm(e.get("to", "")) == _norm(title) and e.get("from") in nodes:
            return e["from"]

    return preferred


def _expand_one(title: str, parent: str | None, skill_name: str) -> bool:
    canon, summary = _resolve_page(title)
    if not summary:
        print(f"[auto_learn] cannot resolve: {title}", flush=True)
        return False
    title = canon

    content = synthesize_article(
        title=title,
        summary=summary.get("extract") or "",
        description=summary.get("description") or "",
        parent=parent,
        sources=[summary["url"]] if summary.get("url") else None,
    )
    score = score_article(content)
    print(f"[auto_learn] {explain_score(score)} — {title}", flush=True)
    if not is_acceptable(score):
        print(f"[auto_learn] reject score={score['score']}", flush=True)
        return False

    write_article(title, content)

    parent_depth = 1
    if parent:
        cov = load_coverage()
        parent_info = (cov.get("nodes") or {}).get(parent)
        parent_depth = (
            parent_info.get("depth", 1) + 1 if parent_info else 2
        )

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

    for child in list(set(get_links(title, 15) + get_related(title, 6)))[:10]:
        if _is_insect_relevant(child):
            register_discovered(child, depth=parent_depth + 1, parent=title)

    reinforce_skill(skill_name, title, score["score"])
    obj, n_nodes, _ = compute_objective_score()
    msg = (
        f"auto_learn: {title} "
        f"(skill={skill_name} score={score['score']} "
        f"nodes={n_nodes} parent={parent})"
    )
    git_commit_push([f"wiki/{title}.md", "state/", "DASHBOARD.md"], msg)
    log_event(
        "auto_learn_expand",
        {
            "title": title,
            "skill": skill_name,
            "score": score["score"],
            "objective": obj,
            "parent": parent,
        },
    )
    print(
        f"[auto_learn] ✅ article créé: {title} ← parent={parent}",
        flush=True,
    )
    return True


def run_auto_learn():
    print("=" * 60, flush=True)
    print("[auto_learn] cycle intelligent (voisinage + sous-parent)", flush=True)

    cov = load_coverage()
    quality = load_quality()
    root = cov.get("root") or "Fly"
    nodes = cov.get("nodes") or {}
    frontier = list(cov.get("frontier") or [])

    skill_name = pick_skill_to_develop()
    skills = load_skills()
    skill_info = skills.get(skill_name, {})
    print(
        f"[auto_learn] skill={skill_name} level={skill_info.get('level', 0)}",
        flush=True,
    )

    existing = list(nodes.keys()) + list(quality.keys())

    # 1) derniers nœuds pour comprendre le graphe
    recent = _recent_nodes(nodes, limit=12)

    # 2) sous-parent
    parent = _best_parent_for_skill(skill_name, nodes, cov)
    if not parent:
        parent = root if root in nodes else (
            existing[0] if existing else None
        )

    # 3) voisinage = liens des derniers nœuds + parent
    neighborhood = _graph_neighborhood(parent, recent, limit=40)

    # 4) pool de candidats (ordre de priorité)
    pool: list[str] = []
    pool += neighborhood                          # liens réels du graphe
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
            print(f"[auto_learn] skip hors-sujet: {title}", flush=True)
            continue
        canon, s = _resolve_page(title)
        if not s:
            continue
        if _already_known(canon, nodes, frontier, quality):
            continue
        if not _is_insect_relevant(canon):
            continue
        fresh.append(canon)

    print(
        f"[auto_learn] {len(fresh)} candidats valides: {fresh[:8]}",
        flush=True,
    )

    # fallback : frontier pertinente (pas un seed random sous le mauvais parent)
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
                print(
                    f"[auto_learn] fallback frontier → {canon}",
                    flush=True,
                )
                break

    learned = False
    for title in fresh[:4]:
        # rattacher au bon parent (lien réel si possible)
        real_parent = _pick_parent_for_title(title, parent, nodes, cov)
        if _expand_one(title, real_parent, skill_name):
            learned = True
            cov = load_coverage()
            nodes = cov.get("nodes") or {}
            quality = load_quality()
            frontier = list(cov.get("frontier") or [])
            break

    parent_depth = 1
    if parent and parent in nodes:
        parent_depth = nodes[parent].get("depth", 1) + 1

    added_f = 0
    for title in fresh[(1 if learned else 0) :]:
        if _already_known(title, nodes, frontier, quality):
            continue
        if not _is_insect_relevant(title):
            continue
        real_parent = _pick_parent_for_title(title, parent, nodes, cov)
        register_discovered(
            title, depth=parent_depth, parent=real_parent
        )
        frontier.append(title)
        added_f += 1
        if added_f >= 6:
            break

    log_event(
        "auto_learn",
        {
            "skill": skill_name,
            "learned": learned,
            "frontier_added": added_f,
            "fresh": fresh[:10],
            "parent": parent,
            "recent": recent[:8],
        },
    )
    print(
        f"[auto_learn] done — article_écrit={learned} "
        f"frontier+={added_f} parent={parent}",
        flush=True,
    )
    return learned or added_f > 0
