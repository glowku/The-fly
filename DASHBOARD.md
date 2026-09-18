# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-18 22:20:50 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **29.497** |
| Concepts traités | 200 | **151** |
| Qualité moyenne | ≥ 7.5 | **9.77/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **151** |
| Arêtes du graphe | 164 |
| Frontière (à explorer) | 28 |
| Profondeur max | 7 |
| Score qualité moyen | **9.77/10** |
| Score objectif (coverage × quality) | **29.497** |
| Actions dernières 24 h | 230 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 148 |
| Bon (6 – 8) | 2 |
| Moyen (4 – 6) | 1 |
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
2026-09-18T19:29:55  auto_learn      
2026-09-18T19:31:30  skill_reinforc  
2026-09-18T19:31:32  auto_learn_exp  Climate change adaptation score=10.0
2026-09-18T19:31:32  auto_learn      
2026-09-18T19:33:08  skill_reinforc  
2026-09-18T19:33:10  auto_learn_exp  Domain adaptation score=10.0
2026-09-18T19:33:10  auto_learn      
2026-09-18T19:34:46  skill_reinforc  
2026-09-18T19:34:48  auto_learn_exp  Ecosystem-based adaptation score=9.5
2026-09-18T19:34:48  auto_learn      
2026-09-18T20:10:58  parallel_learn  
2026-09-18T20:51:52  auto_learn      
2026-09-18T21:07:41  plan            Evolution (journal)
2026-09-18T21:07:41  skill_reinforc  
2026-09-18T21:07:41  branch          Evolution (journal)
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
