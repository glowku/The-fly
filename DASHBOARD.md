# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-20 23:52:54 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.882** |
| Concepts traités | 200 | **204** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **204** |
| Arêtes du graphe | 258 |
| Frontière (à explorer) | 27 |
| Profondeur max | 9 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **38.882** |
| Actions dernières 24 h | 223 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 199 |
| Bon (6 – 8) | 2 |
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
2026-09-20T20:53:27  auto_learn      
2026-09-20T20:55:02  skill_reinforc  
2026-09-20T20:55:04  auto_learn_exp  Antecedent (behavioral psychology) score=8.7
2026-09-20T20:55:04  auto_learn      
2026-09-20T20:56:37  auto_learn      
2026-09-20T20:58:10  auto_learn      
2026-09-20T21:25:32  plan            Evolutionary anachronism
2026-09-20T21:25:32  skill_reinforc  
2026-09-20T21:25:32  branch          Evolutionary anachronism
2026-09-20T23:13:12  auto_learn      
2026-09-20T23:22:15  plan            Evolutionary anachronism
2026-09-20T23:22:16  skill_reinforc  
2026-09-20T23:22:16  branch          Evolutionary anachronism
2026-09-20T23:43:31  parallel_learn  
2026-09-20T23:49:02  skill_reinforc  
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
