# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-08 12:51:39 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **22.936** |
| Concepts traités | 200 | **118** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **118** |
| Arêtes du graphe | 48 |
| Frontière (à explorer) | 12 |
| Profondeur max | 9 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **22.936** |
| Actions dernières 24 h | 137 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 271 |
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
2026-11-08T10:16:37  skill_reinforc  
2026-11-08T10:16:37  skill_learn_ar  What Would a Graph Look Like in This Layout? A Machine Learning Approach to Large Graph Visualization
2026-11-08T10:17:23  skill_reinforc  
2026-11-08T10:17:23  skill_learn_ar  Domain-specific information retrieval
2026-11-08T10:18:05  skill_reinforc  
2026-11-08T10:18:46  skill_reinforc  
2026-11-08T10:19:28  skill_reinforc  
2026-11-08T10:19:28  skill_learn_ar  Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective
2026-11-08T10:20:12  skill_reinforc  
2026-11-08T10:20:53  skill_reinforc  
2026-11-08T10:20:53  skill_learn_ar  IPPOG : Bridging the gap between science education at school and modern scientific research
2026-11-08T10:21:38  skill_reinforc  
2026-11-08T10:22:22  skill_reinforc  
2026-11-08T10:22:22  skill_learn_ar  Intelligent Interaction Strategies for Context-Aware Cognitive Augmentation
2026-11-08T10:23:03  skill_reinforc  
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
