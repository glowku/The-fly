# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-12 02:43:40 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **28.426** |
| Concepts traités | 200 | **146** |
| Qualité moyenne | ≥ 7.5 | **9.74/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **146** |
| Arêtes du graphe | 56 |
| Frontière (à explorer) | 14 |
| Profondeur max | 10 |
| Score qualité moyen | **9.74/10** |
| Score objectif (coverage × quality) | **28.426** |
| Actions dernières 24 h | 119 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 339 |
| Bon (6 – 8) | 8 |
| Moyen (4 – 6) | 4 |
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
2026-11-12T00:56:38  skill_reinforc  
2026-11-12T00:56:38  skill_learn_ar  What Would a Graph Look Like in This Layout? A Machine Learning Approach to Large Graph Visualization
2026-11-12T00:57:47  auto_learn_cyc  
2026-11-12T00:59:55  auto_learn_cyc  
2026-11-12T00:59:57  triage_restore  
2026-11-12T00:59:57  triage          
2026-11-12T01:02:05  auto_learn_cyc  
2026-11-12T01:04:12  auto_learn_cyc  
2026-11-12T01:04:14  triage_restore  
2026-11-12T01:04:14  triage          
2026-11-12T01:06:21  auto_learn_cyc  
2026-11-12T02:14:13  triage_restore  
2026-11-12T02:14:13  triage_restore  
2026-11-12T02:14:13  triage          
2026-11-12T02:14:19  auto_learn_cyc  
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
