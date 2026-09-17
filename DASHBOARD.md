# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-17 14:43:40 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **20.971** |
| Concepts traités | 200 | **107** |
| Qualité moyenne | ≥ 7.5 | **9.8/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **107** |
| Arêtes du graphe | 99 |
| Frontière (à explorer) | 27 |
| Profondeur max | 6 |
| Score qualité moyen | **9.8/10** |
| Score objectif (coverage × quality) | **20.971** |
| Actions dernières 24 h | 360 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 106 |
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
2026-09-17T13:33:02  skill_reinforc  
2026-09-17T13:33:04  auto_learn_exp  Automimicry score=10.0
2026-09-17T13:33:05  auto_learn      
2026-09-17T13:34:42  skill_reinforc  
2026-09-17T13:34:44  auto_learn_exp  Chemical mimicry score=10.0
2026-09-17T13:34:44  auto_learn      
2026-09-17T13:36:20  skill_reinforc  
2026-09-17T13:36:22  auto_learn_exp  Community (ecology) score=10.0
2026-09-17T13:36:22  auto_learn      
2026-09-17T13:37:58  auto_learn      
2026-09-17T13:39:32  auto_learn      
2026-09-17T13:41:06  auto_learn      
2026-09-17T13:42:40  auto_learn      
2026-09-17T13:44:14  auto_learn      
2026-09-17T14:33:25  parallel_learn  
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
