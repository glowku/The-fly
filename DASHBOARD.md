# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-09 23:58:27 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **25.846** |
| Concepts traités | 200 | **133** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **133** |
| Arêtes du graphe | 55 |
| Frontière (à explorer) | 14 |
| Profondeur max | 10 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **25.846** |
| Actions dernières 24 h | 154 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 316 |
| Bon (6 – 8) | 8 |
| Moyen (4 – 6) | 4 |
| Faible (< 4) | 0 |

## Top articles par qualité

| Titre | Score | Mots | Liens |
|-------|-------|------|-------|
| [[Evolution]] | 10.00 | 298 | 6 |
| [[Halteres]] | 10.00 | 360 | 6 |
| [[Fly]] | 10.00 | 357 | 6 |
| [[Wing]] | 10.00 | 378 | 5 |
| [[Aerodynamics]] | 10.00 | 340 | 6 |
| [[Palaeoptera]] | 10.00 | 337 | 7 |
| [[Compound eye]] | 10.00 | 394 | 6 |
| [[Insect ecology]] | 10.00 | 383 | 9 |
| [[Insect behaviour]] | 10.00 | 381 | 6 |
| [[Hover]] | 10.00 | 306 | 6 |
| [[Neoptera]] | 10.00 | 397 | 7 |
| [[Exoskeleton]] | 10.00 | 360 | 12 |

## Derniers événements de l'agent

```
2026-11-09T21:01:22  triage_restore  
2026-11-09T21:01:22  triage          
2026-11-09T21:02:25  skill_reinforc  
2026-11-09T21:03:31  auto_learn_cyc  
2026-11-09T21:04:36  skill_reinforc  
2026-11-09T21:04:36  skill_learn_ar  Agent-Driven Automatic Software Improvement
2026-11-09T21:05:44  auto_learn_cyc  
2026-11-09T21:05:46  triage_restore  
2026-11-09T21:05:46  triage          
2026-11-09T21:06:50  skill_reinforc  
2026-11-09T21:06:50  skill_learn_ar  What Would a Graph Look Like in This Layout? A Machine Learning Approach to Large Graph Visualization
2026-11-09T21:08:01  auto_learn_cyc  
2026-11-09T21:33:57  plan            Thorax
2026-11-09T21:33:57  skill_reinforc  
2026-11-09T21:33:57  branch          Thorax
```

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
