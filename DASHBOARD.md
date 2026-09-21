# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-21 21:45:10 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.747** |
| Concepts traités | 200 | **218** |
| Qualité moyenne | ≥ 7.5 | **9.69/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **218** |
| Arêtes du graphe | 292 |
| Frontière (à explorer) | 34 |
| Profondeur max | 9 |
| Score qualité moyen | **9.69/10** |
| Score objectif (coverage × quality) | **38.747** |
| Actions dernières 24 h | 166 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 211 |
| Bon (6 – 8) | 4 |
| Moyen (4 – 6) | 3 |
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
2026-09-21T16:43:01  skill_reinforc  
2026-09-21T16:43:03  auto_learn_exp  Behavioral cusp score=10.0
2026-09-21T16:43:03  auto_learn      
2026-09-21T16:44:41  auto_learn      
2026-09-21T16:46:19  auto_learn      
2026-09-21T16:47:56  auto_learn      
2026-09-21T16:49:34  auto_learn      
2026-09-21T16:51:11  auto_learn      
2026-09-21T16:52:49  auto_learn      
2026-09-21T16:54:26  auto_learn      
2026-09-21T19:07:05  plan            Evolutionary anachronism
2026-09-21T19:07:06  skill_reinforc  
2026-09-21T19:07:06  branch          Evolutionary anachronism
2026-09-21T19:58:43  auto_learn      
2026-09-21T21:26:52  parallel_learn  
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
