# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-20 03:52:49 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **35.604** |
| Concepts traités | 200 | **183** |
| Qualité moyenne | ≥ 7.5 | **9.73/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **183** |
| Arêtes du graphe | 210 |
| Frontière (à explorer) | 23 |
| Profondeur max | 7 |
| Score qualité moyen | **9.73/10** |
| Score objectif (coverage × quality) | **35.604** |
| Actions dernières 24 h | 195 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 179 |
| Bon (6 – 8) | 2 |
| Moyen (4 – 6) | 2 |
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
2026-09-20T03:09:39  auto_learn      
2026-09-20T03:11:15  auto_learn      
2026-09-20T03:12:51  auto_learn      
2026-09-20T03:14:27  auto_learn      
2026-09-20T03:16:03  skill_reinforc  
2026-09-20T03:16:05  auto_learn_exp  Chromatic adaptation score=10.0
2026-09-20T03:16:05  auto_learn      
2026-09-20T03:17:41  auto_learn      
2026-09-20T03:19:17  auto_learn      
2026-09-20T03:20:53  auto_learn      
2026-09-20T03:22:28  auto_learn      
2026-09-20T03:24:04  skill_reinforc  
2026-09-20T03:24:06  auto_learn_exp  Adaptive behavior score=10.0
2026-09-20T03:24:06  auto_learn      
2026-09-20T03:25:41  skill_reinforc  
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
