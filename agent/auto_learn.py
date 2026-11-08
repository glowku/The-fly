"""
Auto-learning hybride :
- track A: wiki insecte (graphe connaissance)
- track B: skill_learn (code, sécu défensive, web, images, raisonnement)
Alterne pour ne pas stagner sur un graphe pollué.
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
    is_hard_junk,
)
from .perception import get_summary, search_titles, get_links, get_related
from .planning import register_discovered, register_processed
from .synthesis import synthesize_article
from .evaluation import score_article, is_acceptable, explain_score
from .tools import write_article, git_commit_push
from .arxiv_source import search_domain, concepts_from_papers
from .skill_learn import run_skill_learn, SKILL_TRACKS

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
        "Parasitoid", "Decomposer", "Biological pest control",
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
    r"angular velocity|angular momentum|"
    r"chewing gum|bubblegum|eccentricity\s*\(behavior\)|"
    r"punk rock|fly fishing|brewery|behavioral momentum|"
    r"cognitive behavioral|hovercraft|madama butterfly)",
    re.I,
)

# compteur simple en process pour alterner les tracks
_CYCLE = {"n": 0}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _is_junk(title: str) -> bool:
    if not title or len(title) < 2:
        return True
    if is_hard_junk(title):
        return True
    return bool(JUNK_RE.search(title))


def _is_insect_relevant(title: str) -> bool:
    if _is_junk(title):
        return False
    if score_relevance(title) < 0.35:
        return False
    t = (title or "").lower()
    # rejeter ambiguïtés fréquentes
    if any(x in t for x in ("fishing", "brew", "party", "therapy", "journal", "company")):
        if not any(x in t for x in ("insect", "diptera", "housefly", "mosquito", "haltere")):
            return False
    strong = (
        "insect", "fly", "flies", "diptera", "mosquito", "larva", "maggot",
        "wing", "halter", "flight", "hover", "swarm", "pollinat",
        "entomolog", "arthropod", "thorax", "antenna", "exoskeleton",
        "parasitoid", "mimicry", "neoptera", "paleoptera", "devonian",
        "compound eye", "spiracle", "mouthpart", "blowfly", "hoverfly",
        "tachinid", "apterygota", "alate", "wingbeat", "aerodynamic",
        "courtship", "foraging", "mating", "eusocial", "decomposer",
        "pest control", "pollination", "morphology",
    )
    if any(s in t for s in strong):
        return True
    return score_relevance(title) >= 0.45


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


def _recent_nodes(nodes: dict, limit: int = 12) -> list:
    items = []
    for title, info in nodes.items():
        ts = info.get("created_at") or info.get("updated_at") or ""
        items.append((ts, title))
    items.sort(reverse=True)
    return [t for _, t in items[:limit]]


def _graph_neighborhood(parent: str | None, recent: list, limit: int = 40) -> list:
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
    return neigh


def _groq_suggest(skill_name, skill_info, root, parent, recent, existing):
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return []
    kws = ", ".join(skill_info.get("keywords", [])[:8])
    existing_s = ", ".join(existing[:20]) if existing else "(none)"
    recent_s = ", ".join(recent[:10]) if recent else "(none)"
    parent_line = (
        f"Parent to expand under: « {parent} ». Suggest ONLY real sub-topics of this parent."
        if parent else ""
    )
    prompt = f"""You expand a knowledge graph about insects/flies: {root}
Skill: {skill_name} — {skill_info.get('description', '')}
Keywords: {kws}
Recent nodes: {recent_s}
{parent_line}
Already known — DO NOT suggest: {existing_s}

Return ONLY a JSON array of 8 real English Wikipedia titles.
STRICT domain: insects, flies, diptera, morphology, flight, ecology, evolution of insects.
Reject media, fishing, brewing, psychology, software, gum, parties.
"""
    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.25, "max_tokens": 400},
            timeout=60,
        )
        if r.status_code != 200:
            return []
        text = r.json()["choices"][0]["message"]["content"].strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        m = re.search(r"\[[\s\S]*?\]", text)
        if not m:
            return []
        raw = re.sub(r",\s*]", "]", m.group(0))
        return [str(x).strip() for x in json.loads(raw) if str(x).strip()][:10]
    except Exception:
        return []


def _candidates_from_frontier(skill_name, frontier):
    scored = []
    skills = load_skills()
    kws = skills.get(skill_name, {}).get("keywords") or []
    for t in frontier:
        if not _is_insect_relevant(t):
            continue
        rel = score_relevance(t)
        if rel < 0.38:
            continue
        bonus = sum(1 for k in kws if k.lower() in t.lower()) * 0.25
        scored.append((rel + bonus, t))
    scored.sort(reverse=True)
    return [t for s, t in scored if s >= 0.35][:8]


def _best_parent_for_skill(skill_name, nodes, cov):
    skills = load_skills()
    skill = skills.get(skill_name, {})
    skill_articles = set(skill.get("articles", []))
    keywords = [k.lower() for k in skill.get("keywords", [])]
    children_count = {}
    for e in cov.get("edges", []):
        fr = e.get("from")
        if fr:
            children_count[fr] = children_count.get(fr, 0) + 1
    candidates = []
    for title, info in nodes.items():
        if not _is_insect_relevant(title):
            continue
        n_kids = children_count.get(title, 0)
        is_skill = title in skill_articles or any(kw in title.lower() for kw in keywords)
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
        candidates.append((score, title))
    if not candidates:
        return cov.get("root") or "Fly"
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


def _pick_parent_for_title(title, preferred, nodes, cov):
    if preferred:
        try:
            links = set(get_links(preferred, 30) + get_related(preferred, 10))
            if any(_norm(x) == _norm(title) or _similar(x, title) >= 0.9 for x in links):
                return preferred
        except Exception:
            pass
    for e in cov.get("edges", []):
        if _norm(e.get("to", "")) == _norm(title) and e.get("from") in nodes:
            return e["from"]
    return preferred


def _expand_one(title, parent, skill_name):
    canon, summary = _resolve_page(title)
    if not summary:
        return False
    title = canon
    if not _is_insect_relevant(title):
        return False
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
        return False
    write_article(title, content)
    parent_depth = 1
    if parent:
        cov = load_coverage()
        parent_info = (cov.get("nodes") or {}).get(parent)
        parent_depth = parent_info.get("depth", 1) + 1 if parent_info else 2
    register_processed(title, depth=parent_depth, sources=[summary["url"]] if summary.get("url") else [])
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
    msg = f"auto_learn: {title} (skill={skill_name} score={score['score']} nodes={n_nodes})"
    git_commit_push([f"wiki/{title}.md", "state/", "DASHBOARD.md"], msg)
    log_event("auto_learn_expand", {"title": title, "skill": skill_name, "score": score["score"], "objective": obj})
    print(f"[auto_learn] ✅ {title} ← {parent}", flush=True)
    return True


def run_wiki_learn() -> bool:
    print("[auto_learn] track WIKI insecte", flush=True)
    cov = load_coverage()
    quality = load_quality()
    root = cov.get("root") or "Fly"
    nodes = cov.get("nodes") or {}
    frontier = list(cov.get("frontier") or [])
    # ne pick que skills entomologie pour le wiki track
    insect_skills = [k for k in load_skills() if k not in SKILL_TRACKS]
    if not insect_skills:
        insect_skills = list(SKILL_SEEDS.keys())
    skills = load_skills()
    skill_name = min(insect_skills, key=lambda k: skills.get(k, {}).get("level", 0))
    skill_info = skills.get(skill_name, {})
    existing = list(nodes.keys()) + list(quality.keys())
    recent = _recent_nodes(nodes, limit=12)
    parent = _best_parent_for_skill(skill_name, nodes, cov)
    neighborhood = _graph_neighborhood(parent, recent, limit=40)
    pool = []
    pool += neighborhood
    pool += _candidates_from_frontier(skill_name, frontier)
    pool += _groq_suggest(skill_name, skill_info, root, parent, recent, existing)
    try:
        papers = search_domain(f"{skill_name} {root} insect", max_results=5)
        pool += concepts_from_papers(papers, min_relevance=0.30)
    except Exception:
        pass
    pool += SKILL_SEEDS.get(skill_name, SKILL_SEEDS["entomologie"])
    seen = set()
    ordered = []
    for t in pool:
        k = _norm(t)
        if k in seen:
            continue
        seen.add(k)
        ordered.append(t)
    fresh = []
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
    print(f"[auto_learn] candidats: {fresh[:8]}", flush=True)
    learned = False
    for title in fresh[:4]:
        real_parent = _pick_parent_for_title(title, parent, nodes, cov)
        if _expand_one(title, real_parent, skill_name):
            learned = True
            break
    log_event("auto_learn", {"skill": skill_name, "learned": learned, "fresh": fresh[:8]})
    return learned


def run_auto_learn():
    """Point d'entrée: alterne wiki / skill tracks."""
    print("=" * 60, flush=True)
    _CYCLE["n"] += 1
    n = _CYCLE["n"]
    # 1 sur 3 cycles → skill transverse (code/sécu/web/image)
    if n % 3 == 0:
        ok = run_skill_learn()
        print(f"[auto_learn] skill_learn done={ok}", flush=True)
        return ok
    ok = run_wiki_learn()
    print(f"[auto_learn] wiki done={ok}", flush=True)
    return ok
