# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-16 19:23:37 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **1.154** |
| Concepts traités | 200 | **6** |
| Qualité moyenne | ≥ 7.5 | **9.62/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **6** |
| Arêtes du graphe | 11 |
| Frontière (à explorer) | 8 |
| Profondeur max | 2 |
| Score qualité moyen | **9.62/10** |
| Score objectif (coverage × quality) | **1.154** |
| Actions dernières 24 h | 51 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 6 |
| Bon (6 – 8) | 0 |
| Moyen (4 – 6) | 0 |
| Faible (< 4) | 0 |

## Top articles par qualité

| Titre | Score | Mots | Liens |
|-------|-------|------|-------|
| [[Evolution]] | 10.00 | 298 | 6 |
| [[Halteres]] | 10.00 | 360 | 6 |
| [[Fly]] | 10.00 | 357 | 6 |
| [[Wing]] | 10.00 | 378 | 5 |
| [[Insect flight]] | 9.00 | 331 | 2 |
| [[Devonian]] | 8.70 | 149 | 4 |

## Derniers événements de l'agent

```
2026-09-16T13:23:44  skill_reinforc  
2026-09-16T13:23:46  auto_learn_exp  Halteres score=10.0
2026-09-16T13:23:46  auto_learn      
2026-09-16T13:55:50  skill_reinforc  
2026-09-16T13:55:52  auto_learn_exp  Insect flight score=9.0
2026-09-16T13:55:52  auto_learn      
2026-09-16T14:04:49  plan            Fly
2026-09-16T14:04:50  skill_reinforc  
2026-09-16T14:04:52  expand          Fly score=10.0
2026-09-16T16:49:14  skill_reinforc  
2026-09-16T16:49:16  auto_learn_exp  Devonian score=8.7
2026-09-16T16:49:16  auto_learn      
2026-09-16T18:19:33  plan            Wing
2026-09-16T18:19:34  skill_reinforc  
2026-09-16T18:19:36  expand          Wing score=10.0
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
