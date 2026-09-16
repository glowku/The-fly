"""Génère le DASHBOARD.md public à partir de l'état de l'agent."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
from .memory import (
    load_coverage,
    load_quality,
    read_history,
    compute_objective_score,
    load_goal,
)


def render_dashboard():
    cov = load_coverage()
    qual = load_quality()
    hist = read_history()
    goal = load_goal()

    n_nodes = len(cov.get("nodes", {}))
    n_edges = len(cov.get("edges", []))
    n_frontier = len(cov.get("frontier", []))
    obj_score, _, avg_quality = compute_objective_score()

    # Actions 24h
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(hours=24)).isoformat()
    last_24h = [h for h in hist if h.get("ts", "") >= cutoff]

    max_depth = cov.get("max_depth", 0) or max(
        (n.get("depth", 0) for n in cov.get("nodes", {}).values()), default=0
    )

    # Top articles
    top = sorted(qual.items(), key=lambda kv: -kv[1].get("score", 0))[:12]

    # Répartition des scores
    buckets = {"excellent (≥8)": 0, "bon (6-8)": 0, "moyen (4-6)": 0, "faible (<4)": 0}
    for info in qual.values():
        s = info.get("score", 0)
        if s >= 8:
            buckets["excellent (≥8)"] += 1
        elif s >= 6:
            buckets["bon (6-8)"] += 1
        elif s >= 4:
            buckets["moyen (4-6)"] += 1
        else:
            buckets["faible (<4)"] += 1

    content = f"""# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : {now.strftime("%Y-%m-%d %H:%M:%S")} UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« {cov.get('root', 'Fly')} »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **{obj_score}** |
| Concepts traités | {goal.get('target_nodes', 200)} | **{n_nodes}** |
| Qualité moyenne | ≥ {goal.get('target_avg_quality', 7.5)} | **{avg_quality}/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **{n_nodes}** |
| Arêtes du graphe | {n_edges} |
| Frontière (à explorer) | {n_frontier} |
| Profondeur max | {max_depth} |
| Score qualité moyen | **{avg_quality}/10** |
| Score objectif (coverage × quality) | **{obj_score}** |
| Actions dernières 24 h | {len(last_24h)} |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | {buckets['excellent (≥8)']} |
| Bon (6 – 8) | {buckets['bon (6-8)']} |
| Moyen (4 – 6) | {buckets['moyen (4-6)']} |
| Faible (< 4) | {buckets['faible (<4)']} |

## Top articles par qualité

| Titre | Score | Mots | Liens |
|-------|-------|------|-------|
"""
    for title, info in top:
        m = info.get("metrics", {})
        content += (
            f"| [[{title}]] | {info.get('score', 0):.2f} | "
            f"{m.get('words', '?')} | {m.get('links', '?')} |\n"
        )

    content += "\n## Derniers événements de l'agent\n\n```\n"
    for h in hist[-15:]:
        ts = h.get("ts", "")[:19]
        typ = h.get("type", "")[:14]
        title = h.get("title", h.get("count", ""))
        extra = ""
        if "score" in h:
            extra = f" score={h['score']}"
        elif "new_score" in h:
            extra = f" {h.get('old_score')}→{h['new_score']}"
        content += f"{ts}  {typ:<14}  {title}{extra}\n"
    content += "```\n"

    content += f"""
## Architecture de l'agent

```
PERCEIVE (Wikipedia) → PLAN (value-based) → ACT (Groq + git)
         ↑                                           ↓
      REFLECT ←────────── EVALUATE (multi-criteria score)
```

- **Perception** : Wikipedia REST (summary + links + related)
- **Mémoire** : `state/coverage.json` + `quality.json` + `history.jsonl`
- **Planification** : priorité = qualité faible + trou de frontière + centralité
- **Action** : synthèse LLM (Groq llama-3.3-70b) + commit
- **Évaluation** : score 0-10 (longueur, structure, liens, diversité, propreté)
- **Réflexion** : repair des articles faibles + promotion des liens cassés + nettoyage orphelins

---
*Agent autonome — mis à jour automatiquement à chaque cycle.*
"""

    Path("DASHBOARD.md").write_text(content, encoding="utf-8")
    print("[dashboard] mis à jour", flush=True)
    return content


if __name__ == "__main__":
    render_dashboard()
