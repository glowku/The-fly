# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-20 13:58:50 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **37.604** |
| Concepts traités | 200 | **193** |
| Qualité moyenne | ≥ 7.5 | **9.74/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **193** |
| Arêtes du graphe | 242 |
| Frontière (à explorer) | 29 |
| Profondeur max | 8 |
| Score qualité moyen | **9.74/10** |
| Score objectif (coverage × quality) | **37.604** |
| Actions dernières 24 h | 207 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 189 |
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
2026-09-20T09:39:35  auto_learn_exp  Behavior informatics score=10.0
2026-09-20T09:39:35  auto_learn      
2026-09-20T09:41:09  auto_learn      
2026-09-20T09:42:43  skill_reinforc  
2026-09-20T09:42:44  auto_learn_exp  Behavioural sciences score=10.0
2026-09-20T09:42:44  auto_learn      
2026-09-20T09:44:18  auto_learn      
2026-09-20T11:16:50  skill_reinforc  
2026-09-20T11:16:52  auto_learn_exp  Behavioral neuroscience score=10.0
2026-09-20T11:16:52  auto_learn      
2026-09-20T12:05:21  plan            Evolutionary anachronism
2026-09-20T12:05:22  skill_reinforc  
2026-09-20T12:05:22  branch          Evolutionary anachronism
2026-09-20T13:49:57  skill_reinforc  
2026-09-20T13:49:59  parallel_learn  
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
