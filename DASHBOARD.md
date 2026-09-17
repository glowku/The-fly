# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-17 03:45:15 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **14.627** |
| Concepts traités | 200 | **75** |
| Qualité moyenne | ≥ 7.5 | **9.75/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **75** |
| Arêtes du graphe | 74 |
| Frontière (à explorer) | 22 |
| Profondeur max | 6 |
| Score qualité moyen | **9.75/10** |
| Score objectif (coverage × quality) | **14.627** |
| Actions dernières 24 h | 276 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 74 |
| Bon (6 – 8) | 1 |
| Moyen (4 – 6) | 0 |
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
2026-09-17T00:29:57  auto_learn      
2026-09-17T00:31:30  auto_learn      
2026-09-17T00:33:03  auto_learn      
2026-09-17T00:34:36  auto_learn      
2026-09-17T00:36:11  auto_learn      
2026-09-17T00:37:43  auto_learn      
2026-09-17T00:39:16  auto_learn      
2026-09-17T00:40:49  auto_learn      
2026-09-17T00:42:22  auto_learn      
2026-09-17T00:43:55  auto_learn      
2026-09-17T00:45:27  auto_learn      
2026-09-17T00:47:01  skill_reinforc  
2026-09-17T00:47:02  auto_learn_exp  Basal (phylogenetics) score=8.7
2026-09-17T00:47:02  auto_learn      
2026-09-17T02:32:56  parallel_learn  
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
