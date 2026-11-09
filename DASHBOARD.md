# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-09 15:24:19 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **25.635** |
| Concepts traités | 200 | **132** |
| Qualité moyenne | ≥ 7.5 | **9.71/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **132** |
| Arêtes du graphe | 55 |
| Frontière (à explorer) | 14 |
| Profondeur max | 10 |
| Score qualité moyen | **9.71/10** |
| Score objectif (coverage × quality) | **25.635** |
| Actions dernières 24 h | 197 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 309 |
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
2026-11-09T12:38:03  skill_reinforc  
2026-11-09T12:38:43  skill_reinforc  
2026-11-09T12:38:43  skill_learn_ar  LMap: Shape-Preserving Local Mappings for Biomedical Visualization
2026-11-09T12:39:26  skill_reinforc  
2026-11-09T12:39:26  skill_learn_ar  What Would a Graph Look Like in This Layout? A Machine Learning Approach to Large Graph Visualization
2026-11-09T12:40:13  skill_reinforc  
2026-11-09T12:40:13  skill_learn_ar  Navigating the State of Cognitive Flow: Context-Aware AI Interventions for Effective Reasoning Support
2026-11-09T12:40:58  skill_reinforc  
2026-11-09T12:40:58  skill_learn_ar  Automated Literature Review Using NLP Techniques and LLM-Based Retrieval-Augmented Generation
2026-11-09T12:41:43  skill_reinforc  
2026-11-09T12:42:25  skill_reinforc  
2026-11-09T12:42:25  skill_learn_ar  A Case-Driven Multi-Agent Framework for E-Commerce Search Relevance
2026-11-09T12:43:08  skill_reinforc  
2026-11-09T12:43:48  skill_reinforc  
2026-11-09T12:44:27  skill_reinforc  
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
