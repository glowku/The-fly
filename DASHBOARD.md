# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-10-04 13:44:42 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.988** |
| Concepts traités | 200 | **264** |
| Qualité moyenne | ≥ 7.5 | **9.75/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **264** |
| Arêtes du graphe | 407 |
| Frontière (à explorer) | 34 |
| Profondeur max | 9 |
| Score qualité moyen | **9.75/10** |
| Score objectif (coverage × quality) | **38.988** |
| Actions dernières 24 h | 107 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 257 |
| Bon (6 – 8) | 5 |
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
2026-10-04T08:07:05  auto_learn      
2026-10-04T08:08:48  auto_learn      
2026-10-04T08:10:31  auto_learn      
2026-10-04T08:12:13  auto_learn      
2026-10-04T08:13:55  auto_learn      
2026-10-04T08:15:37  auto_learn      
2026-10-04T08:17:19  auto_learn      
2026-10-04T08:19:01  auto_learn      
2026-10-04T08:20:41  auto_learn      
2026-10-04T08:22:22  auto_learn      
2026-10-04T08:24:02  auto_learn      
2026-10-04T08:25:41  auto_learn      
2026-10-04T08:27:21  auto_learn      
2026-10-04T12:16:16  auto_learn      
2026-10-04T13:34:21  parallel_learn  
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
