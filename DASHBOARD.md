# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-23 22:44:18 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.879** |
| Concepts traités | 200 | **255** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **255** |
| Arêtes du graphe | 388 |
| Frontière (à explorer) | 38 |
| Profondeur max | 9 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **38.879** |
| Actions dernières 24 h | 190 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 247 |
| Bon (6 – 8) | 5 |
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
2026-09-23T20:08:03  auto_learn      
2026-09-23T20:09:38  auto_learn      
2026-09-23T20:11:12  auto_learn      
2026-09-23T20:12:47  auto_learn      
2026-09-23T20:14:21  auto_learn      
2026-09-23T20:15:56  auto_learn      
2026-09-23T20:17:30  auto_learn      
2026-09-23T20:19:11  auto_learn      
2026-09-23T20:20:47  auto_learn      
2026-09-23T20:22:21  auto_learn      
2026-09-23T21:13:59  plan            Vineland Adaptive Behavior Scale
2026-09-23T21:13:59  skill_reinforc  
2026-09-23T21:13:59  branch          Vineland Adaptive Behavior Scale
2026-09-23T21:27:46  auto_learn      
2026-09-23T22:34:08  parallel_learn  
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
