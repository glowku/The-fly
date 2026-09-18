# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-18 14:08:11 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **27.999** |
| Concepts traités | 200 | **143** |
| Qualité moyenne | ≥ 7.5 | **9.79/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **143** |
| Arêtes du graphe | 143 |
| Frontière (à explorer) | 21 |
| Profondeur max | 7 |
| Score qualité moyen | **9.79/10** |
| Score objectif (coverage × quality) | **27.999** |
| Actions dernières 24 h | 240 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 141 |
| Bon (6 – 8) | 2 |
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
2026-09-18T09:22:04  auto_learn      
2026-09-18T09:23:39  skill_reinforc  
2026-09-18T09:23:41  auto_learn_exp  Evolutionary arms race score=10.0
2026-09-18T09:23:41  auto_learn      
2026-09-18T09:25:21  auto_learn      
2026-09-18T09:26:57  auto_learn      
2026-09-18T10:45:04  plan            Blue-tailed damselfly
2026-09-18T10:45:05  skill_reinforc  
2026-09-18T10:45:05  branch          Blue-tailed damselfly
2026-09-18T11:08:34  skill_reinforc  
2026-09-18T11:08:36  auto_learn_exp  Abundance (ecology) score=10.0
2026-09-18T11:08:36  auto_learn      
2026-09-18T13:59:02  skill_reinforc  
2026-09-18T13:59:04  parallel_learn  
2026-09-18T14:04:02  skill_reinforc  
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
