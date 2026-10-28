# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-10-28 01:00:02 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.976** |
| Concepts traités | 200 | **266** |
| Qualité moyenne | ≥ 7.5 | **9.74/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **266** |
| Arêtes du graphe | 414 |
| Frontière (à explorer) | 35 |
| Profondeur max | 9 |
| Score qualité moyen | **9.74/10** |
| Score objectif (coverage × quality) | **38.976** |
| Actions dernières 24 h | 51 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 259 |
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
2026-10-27T20:53:42  auto_learn      
2026-10-27T20:55:16  auto_learn      
2026-10-27T20:56:50  auto_learn      
2026-10-27T20:58:24  auto_learn      
2026-10-27T20:59:57  auto_learn      
2026-10-27T21:01:31  auto_learn      
2026-10-27T21:03:04  auto_learn      
2026-10-27T21:04:38  auto_learn      
2026-10-27T21:06:12  auto_learn      
2026-10-27T21:07:46  auto_learn      
2026-10-27T22:09:01  auto_learn      
2026-10-27T23:57:24  plan            Behavioral economics
2026-10-27T23:57:24  skill_reinforc  
2026-10-27T23:57:24  branch          Behavioral economics
2026-10-28T00:50:15  parallel_learn  
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
