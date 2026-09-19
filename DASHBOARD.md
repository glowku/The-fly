# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-19 23:55:34 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **34.804** |
| Concepts traités | 200 | **179** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **179** |
| Arêtes du graphe | 203 |
| Frontière (à explorer) | 23 |
| Profondeur max | 7 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **34.804** |
| Actions dernières 24 h | 217 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 175 |
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
2026-09-19T22:37:17  auto_learn      
2026-09-19T22:38:49  auto_learn      
2026-09-19T22:40:22  auto_learn      
2026-09-19T22:41:55  auto_learn      
2026-09-19T22:43:28  auto_learn      
2026-09-19T22:45:01  auto_learn      
2026-09-19T22:46:34  auto_learn      
2026-09-19T22:48:07  auto_learn      
2026-09-19T22:49:40  auto_learn      
2026-09-19T22:51:16  skill_reinforc  
2026-09-19T22:58:26  auto_learn      
2026-09-19T23:22:06  plan            Sexual antagonistic coevolution
2026-09-19T23:22:07  skill_reinforc  
2026-09-19T23:22:07  branch          Sexual antagonistic coevolution
2026-09-19T23:53:20  parallel_learn  
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
