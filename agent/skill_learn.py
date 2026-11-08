"""
Skill learning hybride, toujours ancré sur des sources réelles.

- Skills biologie → Wikipédia insecte (résonance mots-clés)
- Skills tech (code, sécu, web, images, raisonnement, représentation)
  → Wikipédia CS/SE + arXiv (cs.SE, cs.CR, cs.AI, …)
  → note skill_notes/ + reinforce, éventuellement page wiki/

Jamais de pavé LLM sans source.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from datetime import datetime, timezone
from pathlib import Path

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
from .arxiv_source import search_arxiv

NOTES_DIR = Path("skill_notes")

TECH_SKILLS = {
    "code_et_outils",
    "securite_defensive",
    "recherche_web",
    "recherche_image",
    "raisonnement",
    "representation",
}

# Requêtes wiki + arXiv par skill tech
SKILL_SOURCES = {
    "entomologie": {
        "wiki": [
            "Diptera", "Entomology", "Housefly", "Fruit fly", "Hoverfly",
            "Blowfly", "Tachinidae", "Mosquito", "Insect", "True flies",
        ],
        "arxiv": [],
    },
    "anatomie_insecte": {
        "wiki": [
            "Insect morphology", "Haltere", "Compound eye", "Insect wing",
            "Exoskeleton", "Insect mouthparts", "Spiracle", "Arthropod leg",
            "Thorax", "Antenna (biology)",
        ],
        "arxiv": ["insect morphology haltere"],
    },
    "vol_et_aerodynamique": {
        "wiki": [
            "Insect flight", "Haltere", "Aerodynamics", "Wing", "Hovering",
            "Clap and fling", "Reynolds number",
        ],
        "arxiv": ["insect flight aerodynamics"],
    },
    "ecologie": {
        "wiki": [
            "Insect ecology", "Pollination", "Parasitoid", "Larva", "Maggot",
            "Biological pest control",
        ],
        "arxiv": ["insect ecology parasitoid"],
    },
    "evolution": {
        "wiki": [
            "Evolution of insects", "Paleoptera", "Neoptera", "Devonian",
            "Adaptive radiation", "Coevolution",
        ],
        "arxiv": ["insect evolution phylogeny"],
    },
    "comportement": {
        "wiki": [
            "Insect behavior", "Swarm behaviour", "Courtship", "Foraging",
            "Mimicry", "Eusociality",
        ],
        "arxiv": ["insect behavior swarm"],
    },
    "code_et_outils": {
        "wiki": [
            "Software architecture", "Application programming interface",
            "Version control", "Git", "Continuous integration",
            "Python (programming language)", "JSON", "Graph theory",
            "Retrieval-augmented generation", "Microservices",
            "Autonomous agent", "Software design pattern",
            "Asynchronous I/O", "REST",
        ],
        "arxiv": [
            "retrieval augmented generation",
            "autonomous software agents",
            "continuous integration software",
            "large language model agent tool use",
        ],
        "cats": ("cs.SE", "cs.AI", "cs.IR", "cs.MA"),
    },
    "securite_defensive": {
        "wiki": [
            "Input validation", "Secure coding", "Principle of least privilege",
            "Computer security", "Authentication", "Authorization",
            "Cross-origin resource sharing", "OWASP",
            "Supply chain security", "Secret management",
            "Privilege separation", "Web application security",
            "Dependency management", "Software supply chain",
        ],
        "arxiv": [
            "secure coding practices",
            "software supply chain security",
            "web application security",
            "secrets management",
        ],
        "cats": ("cs.CR", "cs.SE"),
    },
    "recherche_web": {
        "wiki": [
            "Information retrieval", "Web search engine", "Citation",
            "Peer review", "arXiv", "Search engine indexing",
            "Query expansion", "Relevance (information retrieval)",
        ],
        "arxiv": [
            "information retrieval ranking",
            "scientific literature search",
        ],
        "cats": ("cs.IR", "cs.DL"),
    },
    "recherche_image": {
        "wiki": [
            "Scientific visualization", "Diagram", "Technical drawing",
            "Computer vision", "Image retrieval",
        ],
        "arxiv": ["scientific visualization", "image retrieval"],
        "cats": ("cs.CV", "cs.GR"),
    },
    "raisonnement": {
        "wiki": [
            "Knowledge graph", "Semantic network", "Inference",
            "Ontology (information science)", "Automated reasoning",
            "Graph database", "Semantic reasoner",
        ],
        "arxiv": [
            "knowledge graph reasoning",
            "retrieval augmented generation reasoning",
        ],
        "cats": ("cs.AI", "cs.CL", "cs.DB"),
    },
    "representation": {
        "wiki": [
            "Graph drawing", "Data visualization", "Force-directed graph drawing",
            "Network theory", "Scientific visualization",
        ],
        "arxiv": ["graph visualization layout", "force directed graph"],
        "cats": ("cs.GR", "cs.SI"),
    },
}


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _ensure_skills():
    skills = load_skills()
    changed = False
    for name, src in SKILL_SOURCES.items():
        if name not in skills:
            kws = []
            for q in src.get("wiki", [])[:6]:
                kws.append(q.split()[0].lower())
            skills[name] = {
                "level": 0.4,
                "description": f"Skill {name}",
                "keywords": kws,
                "articles": [],
            }
            changed = True
    if changed:
        save_skills(skills)
    return skills


def _already(title: str, nodes: dict, quality: dict, notes_stems: set) -> bool:
    n = _norm(title)
    if n in notes_stems:
        return True
    for t in list(nodes.keys()) + list(quality.keys()):
        if _norm(t) == n or _similar(title, t) >= 0.90:
            return True
    return False


def _resonance(title: str, skill_name: str, skill_info: dict) -> float:
    if is_hard_junk(title):
        return 0.0
    t = title.lower()
    score = 0.0
    for kw in skill_info.get("keywords") or []:
        if kw.lower() in t:
            score += 0.3
    for q in SKILL_SOURCES.get(skill_name, {}).get("wiki", []):
        if _norm(q) == _norm(title):
            score += 1.2
        elif q.lower() in t or t in q.lower():
            score += 0.55
        else:
            score += 0.12 * _similar(q, title)
    if skill_name not in TECH_SKILLS:
        score += score_relevance(title) * 0.7
    return round(score, 3)


def _wiki_pool(skill_name: str, skill_info: dict) -> list[str]:
    src = SKILL_SOURCES.get(skill_name, {})
    pool, seen = [], set()
    for q in src.get("wiki", []) + list(skill_info.get("keywords") or [])[:5]:
        k = _norm(q)
        if k and k not in seen:
            pool.append(q)
            seen.add(k)
        try:
            for h in search_titles(str(q), limit=5):
                hk = _norm(h)
                if hk in seen or is_hard_junk(h):
                    continue
                seen.add(hk)
                pool.append(h)
        except Exception:
            pass
    return pool


def _resolve_wiki(title: str):
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


def _arxiv_candidates(skill_name: str) -> list[dict]:
    src = SKILL_SOURCES.get(skill_name, {})
    cats = src.get("cats")
    out, seen = [], set()
    for q in src.get("arxiv") or []:
        try:
            hits = search_arxiv(q, max_results=5, cats=cats)
        except Exception as e:
            print(f"[skill_learn] arxiv err: {e}", flush=True)
            hits = []
        for h in hits:
            tid = h.get("id") or h.get("title")
            if not tid or tid in seen:
                continue
            seen.add(tid)
            out.append(h)
    return out


def _write_tech_note(skill_name: str, title: str, body: str, source_url: str, kind: str) -> Path:
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:70]
    path = NOTES_DIR / f"{slug}.md"
    header = (
        f"---\nskill: {skill_name}\ntitle: {title}\n"
        f"source: {kind}\nurl: {source_url}\n"
        f"created: {datetime.now(timezone.utc).isoformat()}\n---\n\n"
    )
    path.write_text(header + body.strip() + "\n", encoding="utf-8")
    return path


def _learn_from_wiki(skill_name: str, skill_info: dict, nodes: dict, quality: dict, notes_stems: set):
    pool = _wiki_pool(skill_name, skill_info)
    ranked = []
    for t in pool:
        r = _resonance(t, skill_name, skill_info)
        if r >= 0.25:
            ranked.append((r, t))
    ranked.sort(reverse=True)
    print(f"[skill_learn] wiki ranked: {ranked[:8]}", flush=True)

    cov = load_coverage()
    for res, title in ranked[:14]:
        if _already(title, nodes, quality, notes_stems):
            continue
        if skill_name not in TECH_SKILLS and score_relevance(title) < 0.28 and res < 0.6:
            continue
        canon, summary = _resolve_wiki(title)
        if not summary or _already(canon, nodes, quality, notes_stems):
            continue
        if is_hard_junk(canon):
            continue

        parent = None
        arts = skill_info.get("articles") or []
        for a in reversed(arts):
            if a in nodes:
                parent = a
                break
        if not parent:
            parent = cov.get("root") if cov.get("root") in nodes else None

        content = synthesize_article(
            title=canon,
            summary=summary.get("extract") or "",
            description=summary.get("description") or "",
            parent=parent,
            sources=[summary["url"]] if summary.get("url") else None,
        )
        score = score_article(content)
        print(f"[skill_learn] wiki {explain_score(score)} — {canon}", flush=True)
        if not is_acceptable(score):
            continue

        write_article(canon, content)
        depth = 1
        if parent and parent in nodes:
            depth = nodes[parent].get("depth", 1) + 1
        register_processed(canon, depth=depth, sources=[summary["url"]] if summary.get("url") else [])
        if parent:
            register_discovered(canon, depth=depth, parent=parent)
        quality[canon] = score
        save_quality(quality)
        reinforce_skill(skill_name, canon, score["score"])

        # note tech aussi pour skills techniques
        if skill_name in TECH_SKILLS:
            note_body = (
                f"# {canon}\n\n"
                f"## Source\nWikipedia — {summary.get('url', '')}\n\n"
                f"## Extrait\n{summary.get('extract', '')[:1200]}\n\n"
                f"## Points utiles pour The-fly\n"
                f"- Intégrer ce concept dans les boucles agent / graphe / CI.\n"
            )
            _write_tech_note(skill_name, canon, note_body, summary.get("url") or "", "wikipedia")

        try:
            git_commit_push(
                [f"wiki/{canon}.md", "state/", "skill_notes/", "DASHBOARD.md"],
                f"skill_learn(wiki): {canon} [{skill_name}]",
            )
        except Exception as e:
            print(f"[skill_learn] push skip: {e}", flush=True)

        return {
            "ok": True,
            "skill": skill_name,
            "title": canon,
            "resonance": res,
            "score": score["score"],
            "source": "wikipedia",
            "new": True,
        }
    return None


def _learn_from_arxiv(skill_name: str, nodes: dict, quality: dict, notes_stems: set):
    if skill_name not in TECH_SKILLS and skill_name not in (
        "vol_et_aerodynamique", "evolution", "ecologie", "anatomie_insecte"
    ):
        # bio peut aussi profiter d'arxiv mais wiki d'abord
        pass

    papers = _arxiv_candidates(skill_name)
    print(f"[skill_learn] arxiv hits: {len(papers)}", flush=True)
    for p in papers:
        title = (p.get("title") or "").strip()
        if not title:
            continue
        if _already(title, nodes, quality, notes_stems):
            continue
        summary = (p.get("summary") or "").strip()
        if len(summary) < 80:
            continue
        url = p.get("url") or p.get("id") or ""

        # Note ancrée (pas d'invention)
        body = (
            f"# {title}\n\n"
            f"## Source\narXiv — {url}\n\n"
            f"## Abstract\n{summary[:2000]}\n\n"
            f"## Extraction pour skill `{skill_name}`\n"
            f"- Concepts à retenir pour l'agent The-fly (architecture, sécu, retrieval, graphe).\n"
            f"- Ne pas traiter l'abstract comme un tutoriel offensif.\n"
        )
        path = _write_tech_note(skill_name, title, body, url, "arxiv")
        slug = path.stem
        reinforce_skill(skill_name, slug, 70)
        log_event("skill_learn_arxiv", {"skill": skill_name, "title": title, "url": url})

        # Option: aussi une fiche wiki courte synthétisée depuis abstract
        try:
            content = synthesize_article(
                title=title[:120],
                summary=summary[:1500],
                description=f"arXiv paper for skill {skill_name}",
                parent=None,
                sources=[url] if url else None,
            )
            score = score_article(content)
            if is_acceptable(score):
                safe_title = re.sub(r"[^\w\s\-]", "", title)[:80].strip() or slug
                write_article(safe_title, content)
                register_processed(safe_title, depth=2, sources=[url] if url else [])
                quality[safe_title] = score
                save_quality(quality)
        except Exception as e:
            print(f"[skill_learn] arxiv wiki skip: {e}", flush=True)

        try:
            git_commit_push(
                ["skill_notes/", "state/", "wiki/", "DASHBOARD.md"],
                f"skill_learn(arxiv): {title[:60]} [{skill_name}]",
            )
        except Exception as e:
            print(f"[skill_learn] push skip: {e}", flush=True)

        return {
            "ok": True,
            "skill": skill_name,
            "title": title,
            "source": "arxiv",
            "new": True,
            "file": str(path),
        }
    return None


def run_skill_learn(force_skill: str | None = None, force_topic: str | None = None) -> dict:
    print("[skill_learn] hybrid wiki+arxiv cycle", flush=True)
    skills = _ensure_skills()

    if force_skill and force_skill in skills:
        skill_name = force_skill
    else:
        # alterner: favoriser skills tech si sous-niveau
        tech_levels = [(k, skills.get(k, {}).get("level", 0)) for k in TECH_SKILLS if k in skills]
        bio_levels = [(k, skills.get(k, {}).get("level", 0)) for k in skills if k not in TECH_SKILLS]
        tech_levels.sort(key=lambda x: x[1])
        bio_levels.sort(key=lambda x: x[1])
        # 50/50 biais tech si un tech < 3
        if tech_levels and tech_levels[0][1] < 3.5:
            skill_name = tech_levels[0][0]
        else:
            skill_name = pick_skill_to_develop()
            if skill_name not in SKILL_SOURCES and tech_levels:
                skill_name = tech_levels[0][0]

    skill_info = skills.get(skill_name, {})
    print(f"[skill_learn] skill={skill_name} level={skill_info.get('level')} tech={skill_name in TECH_SKILLS}", flush=True)

    nodes = load_coverage().get("nodes") or {}
    quality = load_quality()
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    notes_stems = {_norm(p.stem) for p in NOTES_DIR.glob("*.md")}

    if force_topic:
        # forcer une recherche wiki sur le topic
        skill_info = dict(skill_info)
        skill_info["keywords"] = list(skill_info.get("keywords") or []) + [force_topic]

    # Ordre: tech → wiki CS puis arxiv ; bio → wiki insecte puis arxiv léger
    if skill_name in TECH_SKILLS:
        hit = _learn_from_wiki(skill_name, skill_info, nodes, quality, notes_stems)
        if hit:
            return hit
        hit = _learn_from_arxiv(skill_name, nodes, quality, notes_stems)
        if hit:
            return hit
    else:
        hit = _learn_from_wiki(skill_name, skill_info, nodes, quality, notes_stems)
        if hit:
            return hit
        hit = _learn_from_arxiv(skill_name, nodes, quality, notes_stems)
        if hit:
            return hit

    print("[skill_learn] aucun candidat frais", flush=True)
    return {"ok": False, "skill": skill_name, "new": False, "source": "none"}


# compat
SKILL_TRACKS = {
    k: {"topics": v.get("wiki", []), "keywords": []}
    for k, v in SKILL_SOURCES.items()
}
