# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-22 07:23:25 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.772** |
| Concepts traités | 200 | **224** |
| Qualité moyenne | ≥ 7.5 | **9.69/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **224** |
| Arêtes du graphe | 313 |
| Frontière (à explorer) | 35 |
| Profondeur max | 9 |
| Score qualité moyen | **9.69/10** |
| Score objectif (coverage × quality) | **38.772** |
| Actions dernières 24 h | 137 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 217 |
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
2026-09-22T01:06:05  auto_learn      
2026-09-22T01:07:51  auto_learn      
2026-09-22T01:09:38  auto_learn      
2026-09-22T01:11:23  auto_learn      
2026-09-22T01:12:58  auto_learn      
2026-09-22T01:14:43  auto_learn      
2026-09-22T01:16:28  auto_learn      
2026-09-22T01:28:48  plan            Desert ecology
2026-09-22T01:28:49  skill_reinforc  
2026-09-22T01:28:49  branch          Desert ecology
2026-09-22T04:48:55  auto_learn      
2026-09-22T06:44:25  plan            E. coli long-term evolution experiment
2026-09-22T06:44:25  skill_reinforc  
2026-09-22T06:44:25  branch          E. coli long-term evolution experiment
2026-09-22T07:04:18  parallel_learn  
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
