# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-24 09:02:13 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.964** |
| Concepts traités | 200 | **258** |
| Qualité moyenne | ≥ 7.5 | **9.74/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **258** |
| Arêtes du graphe | 397 |
| Frontière (à explorer) | 38 |
| Profondeur max | 9 |
| Score qualité moyen | **9.74/10** |
| Score objectif (coverage × quality) | **38.964** |
| Actions dernières 24 h | 179 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 251 |
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
2026-09-24T03:22:26  auto_learn      
2026-09-24T03:24:01  skill_reinforc  
2026-09-24T03:24:03  auto_learn_exp  Radical behaviorism score=10.0
2026-09-24T03:24:03  auto_learn      
2026-09-24T03:25:38  auto_learn      
2026-09-24T03:27:13  auto_learn      
2026-09-24T03:28:48  auto_learn      
2026-09-24T03:30:22  auto_learn      
2026-09-24T03:32:02  skill_reinforc  
2026-09-24T03:40:58  plan            Adaptation (arts)
2026-09-24T03:41:00  skill_reinforc  
2026-09-24T03:41:03  expand          Adaptation (arts) score=10.0
2026-09-24T04:42:40  auto_learn      
2026-09-24T08:52:31  parallel_learn  
2026-09-24T08:58:04  skill_reinforc  
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
