# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-17 09:15:21 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **17.597** |
| Concepts traités | 200 | **90** |
| Qualité moyenne | ≥ 7.5 | **9.78/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **90** |
| Arêtes du graphe | 83 |
| Frontière (à explorer) | 22 |
| Profondeur max | 6 |
| Score qualité moyen | **9.78/10** |
| Score objectif (coverage × quality) | **17.597** |
| Actions dernières 24 h | 335 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 89 |
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
2026-09-17T07:42:05  auto_learn_exp  Maggot score=10.0
2026-09-17T07:42:05  auto_learn      
2026-09-17T07:43:40  skill_reinforc  
2026-09-17T07:43:42  auto_learn_exp  Courtship score=10.0
2026-09-17T07:43:42  auto_learn      
2026-09-17T07:45:17  skill_reinforc  
2026-09-17T07:45:19  auto_learn_exp  Animal sexual behaviour score=10.0
2026-09-17T07:45:19  auto_learn      
2026-09-17T07:46:55  skill_reinforc  
2026-09-17T07:46:57  auto_learn_exp  Alternative mating strategy score=10.0
2026-09-17T07:46:57  auto_learn      
2026-09-17T07:48:31  auto_learn      
2026-09-17T07:50:05  auto_learn      
2026-09-17T09:02:16  skill_reinforc  
2026-09-17T09:02:18  parallel_learn  
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
