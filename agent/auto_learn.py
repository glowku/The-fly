"""
Auto-learning :
- priorise les liens / related du sous-parent choisi (vrai branchement)
- Groq guidé par le parent + skill
- seeds curés en fallback
- dédup + filtre anti-bruit + filtre insecte
- depth correct (parent.depth + 1)
- si fresh vide → force un item de frontier sous le parent
- 1 vrai article par cycle, rattaché au sous-parent
"""
import os
import re
import json
import requests
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
    r"arxiv|academic press|publisher|isbn|doi|journal|"
    r"computer security|cybersecurity|encryption|"
    r"angular velocity|angular momentum|"
    r"adrian thomas|zoologist\)?$)",
    re.I,
)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _is_junk(title: str) -> bool:
    if not title or len(title) < 2:
        return True
    if JUNK_RE.search(title):
        return True
    return False


def _is_insect_relevant(title: str) -> bool:
    """Refuse tout ce qui n'a rien à voir avec insectes / vol / diptera."""
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
    )
    if any(s in t for s in strong):
        return True
    if score_relevance(title) >= 0.35:
        return True
    return False


def _already_known(title: str, nodes: dict, frontier: list, quality: dict) -> bool:
    n = _norm(title)
    if not n:
        return True
    for t in list(nodes.keys()) + list(quality.keys()) + list(frontier):
        if _norm(t) == n or _similar(title, t) >= 0.88:
            return True
    return False


def _resolve_page(title: str):
    """Retourne (canonical_title, summary) ou (None, None)."""
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


def _groq_suggest(
    skill_name: str,
    skill_info: dict,
    root: str,
    parent: str | None,
    existing: list,
) -> list:
    """Suggestions guidées par le sous-parent choisi → vrais enfants."""
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        print("[auto_learn] GROQ_API_KEY missing", flush=True)
        return []
    kws = ", ".join(skill_info.get("keywords", [])[:8])
    existing_s = ", ".join(existing[:25]) if existing else "(none)"
    parent_line = (
        f"Parent node to expand under: « {parent} ». "
        "Suggest real sub-topics of this parent."
        if parent
        else ""
    )
    prompt = f"""You expand a knowledge graph about: {root}
Skill to grow: {skill_name} ({skill_info.get('description', '')})
Keywords: {kws}
{parent_line}
Already in wiki — DO NOT suggest these: {existing_s}
Return ONLY a JSON array of 8 real English Wikipedia article titles
that are direct sub-concepts of the parent (or of the skill if no parent).
Focus on insects / flies / diptera. No markdown, no comments.
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
                "temperature": 0.4,
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
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            print(f"[auto_learn] Groq bad JSON: {text[:200]}", flush=True)
            return []
        items = [
            str(x).strip()
            for x in json.loads(m.group(0))
            if str(x).strip()
        ]
        print(f"[auto_learn] Groq OK → {items}", flush=True)
        return items[:10]
    except Exception as e:
        print(f"[auto_learn] Groq error: {e}", flush=True)
        return []


def _candidates_from_parent(parent: str | None) -> list:
    """Vrais enfants potentiels = liens + related du parent, filtrés insecte."""
    if not parent:
        return []
    kids = list(set(get_links(parent, 25) + get_related(parent, 12)))
    good = [t for t in kids if _is_insect_relevant(t)]
    print(
        f"[auto_learn] liens parent « {parent} » → {len(good)} pertinents",
        flush=True,
    )
    return good[:12]


def _candidates_from_frontier(skill_name: str, frontier: list) -> list:
    """Frontier items matching skill keywords / relevance."""
    scored = []
    skills = load_skills()
    kws = skills.get(skill_name, {}).get("keywords") or []
    for t in frontier:
        if _is_junk(t) or not _is_insect_relevant(t):
            continue
        rel = score_relevance(t)
        bonus = sum(1 for k in kws if k.lower() in t.lower()) * 0.25
        scored.append((rel + bonus, t))
    scored.sort(reverse=True)
    return [t for s, t in scored if s >= 0.12][:8]


def _best_parent_for_skill(
    skill_name: str, nodes: dict, cov: dict
) -> str | None:
    """
    Choisit le meilleur sous-parent pour ramifier :
    1. Feuille (0 enfant) déjà liée à la skill
    2. Nœud de la skill avec < 3 enfants
    3. N'importe quelle feuille du graphe
    4. Fallback → root
    """
    skills = load_skills()
    skill = skills.get(skill_name, {})
    skill_articles = set(skill.get("articles", []))
    keywords = [k.lower() for k in skill.get("keywords", [])]

    edges = cov.get("edges", [])
    children_count: dict[str, int] = {}
    for e in edges:
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

    # profondeur réelle = parent.depth + 1
    parent_depth = 1
    if parent:
        cov = load_coverage()
        parent_info = (cov.get("nodes") or {}).get(parent)
        if parent_info:
            parent_depth = parent_info.get("depth", 1) + 1
        else:
            parent_depth = 2

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

    # enfants du nouvel article (filtrés insecte)
    for child in list(set(get_links(title, 15) + get_related(title, 6)))[:10]:
        if _is_insect_relevant(child):
            register_discovered(
                child, depth=parent_depth + 1, parent=title
            )

    reinforce_skill(skill_name, title, score["score"])
    obj, n_nodes, _ = compute_objective_score()
    msg = (
        f"auto_learn: {title} "
        f"(skill={skill_name} score={score['score']} "
        f"nodes={n_nodes} parent={parent})"
    )
    git_commit_push(
        [f"wiki/{title}.md", "state/", "DASHBOARD.md"], msg
    )
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
    print("[auto_learn] cycle intelligent (sous-parent)", flush=True)

    cov = load_coverage()
    quality = load_quality()
    root = cov.get("root") or "Fly"
    nodes = cov.get("nodes") or {}
    frontier = list(cov.get("frontier") or [])

    skill_name = pick_skill_to_develop()
    skills = load_skills()
    skill_info = skills.get(skill_name, {})
    print(
        f"[auto_learn] skill={skill_name} "
        f"level={skill_info.get('level', 0)}",
        flush=True,
    )

    existing = list(nodes.keys()) + list(quality.keys())

    # ★★★ CHOIX DU SOUS-PARENT ★★★
    parent = _best_parent_for_skill(skill_name, nodes, cov)
    if not parent:
        parent = root if root in nodes else (
            existing[0] if existing else None
        )

    # 1) liens du parent  2) frontier  3) Groq  4) seeds
    pool: list[str] = []
    pool += _candidates_from_parent(parent)
    pool += _candidates_from_frontier(skill_name, frontier)
    pool += _groq_suggest(
        skill_name, skill_info, root, parent, existing
    )
    pool += SKILL_SEEDS.get(skill_name, SKILL_SEEDS["entomologie"])

    # unique, ordre préservé
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

    # Fallback : forcer un item de frontier sous le parent
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
        if _expand_one(title, parent, skill_name):
            learned = True
            cov = load_coverage()
            nodes = cov.get("nodes") or {}
            quality = load_quality()
            frontier = list(cov.get("frontier") or [])
            break

    # reste en frontier avec la bonne profondeur
    parent_depth = 1
    if parent and parent in nodes:
        parent_depth = nodes[parent].get("depth", 1) + 1

    added_f = 0
    for title in fresh[(1 if learned else 0) :]:
        if _already_known(title, nodes, frontier, quality):
            continue
        if not _is_insect_relevant(title):
            continue
        register_discovered(title, depth=parent_depth, parent=parent)
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
        },
    )
    print(
        f"[auto_learn] done — article_écrit={learned} "
        f"frontier+={added_f} parent={parent}",
        flush=True,
    )
    return learned or added_f > 0
