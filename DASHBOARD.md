# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-08 18:40:43 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **21.742** |
| Concepts traités | 200 | **112** |
| Qualité moyenne | ≥ 7.5 | **9.71/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **112** |
| Arêtes du graphe | 52 |
| Frontière (à explorer) | 13 |
| Profondeur max | 9 |
| Score qualité moyen | **9.71/10** |
| Score objectif (coverage × quality) | **21.742** |
| Actions dernières 24 h | 173 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 280 |
| Bon (6 – 8) | 6 |
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
2026-11-08T16:51:59  skill_reinforc  
2026-11-08T16:53:04  skill_reinforc  
2026-11-08T16:53:06  auto_learn_exp  Area (graph drawing) score=10.0
2026-11-08T16:53:06  auto_learn_cyc  
2026-11-08T16:53:08  triage_restore  
2026-11-08T16:53:08  triage          
2026-11-08T16:54:12  skill_reinforc  
2026-11-08T16:55:18  skill_reinforc  
2026-11-08T16:55:20  auto_learn_exp  Graph drawing score=8.7
2026-11-08T16:55:20  auto_learn_cyc  
2026-11-08T17:53:58  triage_restore  
2026-11-08T17:53:58  triage_restore  
2026-11-08T17:53:58  triage          
2026-11-08T17:54:02  skill_reinforc  
2026-11-08T17:54:08  auto_learn_cyc  
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
