"""
Auto-learning : utilise Groq pour proposer des concepts à explorer
dans une branche skill, puis les ajoute à la frontière / en expand un.
"""
import os
import re
import json
import requests
from .memory import load_coverage, load_quality, log_event, save_coverage
from .skills import load_skills, pick_skill_to_develop, reinforce_skill
from .perception import multi_search, get_summary, search_titles
from .planning import register_discovered

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-20b"


def _groq_suggest(skill_name: str, skill_info: dict, root: str, existing: list) -> list:
    """Demande à Groq une liste de concepts Wikipedia à apprendre."""
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        print("[auto_learn] pas de GROQ_API_KEY → fallback keywords", flush=True)
        return []

    kws = ", ".join(skill_info.get("keywords", [])[:8])
    existing_s = ", ".join(existing[:20]) if existing else "(aucun)"
    prompt = f"""Tu es un tuteur qui construit un graphe de connaissance encyclopédique.

Sujet racine du wiki: {root}
Compétence à développer: {skill_name}
Description: {skill_info.get('description', '')}
Mots-clés: {kws}
Articles déjà présents: {existing_s}

Propose exactement 8 titres d'articles Wikipedia EN ANGLAIS, réels et précis,
utiles pour approfondir cette compétence liés au sujet racine.
Réponds UNIQUEMENT avec une liste JSON de strings, sans markdown.
Exemple: ["Diptera", "Insect wing", "Haltere"]"""

    try:
        r = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.4,
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
        # extract JSON array
        m = re.search(r"\[.*\]", text, re.S)
        if not m:
            return []
        items = json.loads(m.group(0))
        return [str(x).strip() for x in items if str(x).strip()][:10]
    except Exception as e:
        print(f"[auto_learn] error: {e}", flush=True)
        return []


def _fallback_from_keywords(skill_info: dict, root: str) -> list:
    kws = skill_info.get("keywords") or []
    out = []
    for kw in kws[:4]:
        for h in multi_search(f"{root} {kw}", limit_per=3)[:3]:
            out.append(h)
        for h in search_titles(kw, limit=3):
            out.append(h)
    # dedupe
    seen = set()
    res = []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res[:12]


def run_auto_learn():
    """
    1. Choisit la skill la plus faible
    2. Demande à Groq des concepts à explorer
    3. Valide via Wikipedia (summary existe)
    4. Ajoute à la frontière sous le root / articles liés
    """
    print("=" * 60, flush=True)
    print("[auto_learn] cycle d'auto-apprentissage", flush=True)

    cov = load_coverage()
    root = cov.get("root") or "Fly"
    skills = load_skills()
    skill_name = pick_skill_to_develop()
    skill_info = skills.get(skill_name, {})
    print(f"[auto_learn] skill cible: {skill_name} (level={skill_info.get('level', 0)})", flush=True)

    existing = list(cov.get("nodes", {}).keys())
    suggestions = _groq_suggest(skill_name, skill_info, root, existing)
    if not suggestions:
        suggestions = _fallback_from_keywords(skill_info, root)
        print(f"[auto_learn] fallback keywords → {len(suggestions)} suggestions", flush=True)
    else:
        print(f"[auto_learn] Groq → {len(suggestions)} suggestions: {suggestions[:5]}…", flush=True)

    parent = root if root in cov.get("nodes", {}) else (existing[0] if existing else None)
    added = 0
    validated = []
    for title in suggestions:
        # validate page exists
        s = get_summary(title)
        if not s:
            # try multi_search resolve
            hits = multi_search(title, limit_per=3)
            for h in hits[:2]:
                s = get_summary(h)
                if s:
                    title = s.get("title") or h
                    break
        if not s:
            print(f"[auto_learn] skip (no wiki): {title}", flush=True)
            continue
        title = s.get("title") or title
        if title in cov.get("nodes", {}):
            continue
        register_discovered(title, depth=2, parent=parent)
        validated.append(title)
        added += 1

    log_event("auto_learn", {
        "skill": skill_name,
        "suggested": len(suggestions),
        "added": added,
        "titles": validated[:12],
    })
    print(f"[auto_learn] {added} concepts ajoutés à la frontière pour skill={skill_name}", flush=True)
    return added
