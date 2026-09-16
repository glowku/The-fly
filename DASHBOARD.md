# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-16 22:40:42 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **5.314** |
| Concepts traités | 200 | **27** |
| Qualité moyenne | ≥ 7.5 | **9.84/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **27** |
| Arêtes du graphe | 26 |
| Frontière (à explorer) | 19 |
| Profondeur max | 3 |
| Score qualité moyen | **9.84/10** |
| Score objectif (coverage × quality) | **5.314** |
| Actions dernières 24 h | 118 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 27 |
| Bon (6 – 8) | 0 |
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
2026-09-16T22:23:35  auto_learn_exp  Angular velocity score=10.0
2026-09-16T22:23:35  auto_learn      
2026-09-16T22:28:22  skill_reinforc  
2026-09-16T22:28:24  auto_learn_exp  Arthropod score=8.0
2026-09-16T22:28:24  auto_learn      
2026-09-16T22:34:47  skill_reinforc  
2026-09-16T22:34:48  auto_learn_exp  Annual Review of Entomology score=10.0
2026-09-16T22:34:48  auto_learn      
2026-09-16T22:37:07  skill_reinforc  
2026-09-16T22:37:09  auto_learn_exp  Mimicry score=10.0
2026-09-16T22:37:09  auto_learn      
2026-09-16T22:38:42  skill_reinforc  
2026-09-16T22:38:44  auto_learn_exp  Arthropod eye score=10.0
2026-09-16T22:38:44  auto_learn      
2026-09-16T22:40:16  skill_reinforc  
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
