# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-19 13:42:57 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **32.312** |
| Concepts traités | 200 | **166** |
| Qualité moyenne | ≥ 7.5 | **9.73/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **166** |
| Arêtes du graphe | 175 |
| Frontière (à explorer) | 24 |
| Profondeur max | 7 |
| Score qualité moyen | **9.73/10** |
| Score objectif (coverage × quality) | **32.312** |
| Actions dernières 24 h | 218 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 162 |
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
2026-09-19T09:08:05  auto_learn      
2026-09-19T09:09:39  skill_reinforc  
2026-09-19T09:09:41  auto_learn_exp  Literary adaptation score=10.0
2026-09-19T09:09:41  auto_learn      
2026-09-19T09:11:14  auto_learn      
2026-09-19T09:12:46  auto_learn      
2026-09-19T10:53:07  auto_learn      
2026-09-19T12:00:16  plan            Sexual antagonistic coevolution
2026-09-19T12:00:16  skill_reinforc  
2026-09-19T12:00:16  branch          Sexual antagonistic coevolution
2026-09-19T13:35:09  parallel_learn  
2026-09-19T13:40:02  skill_reinforc  
2026-09-19T13:40:04  auto_learn_exp  Saro Windhover score=8.7
2026-09-19T13:40:04  auto_learn      
2026-09-19T13:41:39  skill_reinforc  
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
