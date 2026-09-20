# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-20 09:06:54 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **35.804** |
| Concepts traités | 200 | **184** |
| Qualité moyenne | ≥ 7.5 | **9.73/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **184** |
| Arêtes du graphe | 219 |
| Frontière (à explorer) | 22 |
| Profondeur max | 7 |
| Score qualité moyen | **9.73/10** |
| Score objectif (coverage × quality) | **35.804** |
| Actions dernières 24 h | 187 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 180 |
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
2026-09-20T03:41:46  auto_learn      
2026-09-20T03:43:23  auto_learn      
2026-09-20T03:44:59  auto_learn      
2026-09-20T03:46:35  auto_learn      
2026-09-20T03:48:12  auto_learn      
2026-09-20T03:49:48  auto_learn      
2026-09-20T03:51:24  auto_learn      
2026-09-20T03:53:01  skill_reinforc  
2026-09-20T03:53:03  auto_learn_exp  Bibliography of fly fishing (species related) score=10.0
2026-09-20T03:53:03  auto_learn      
2026-09-20T04:49:36  auto_learn      
2026-09-20T06:47:22  plan            Bamboo fly rod
2026-09-20T06:47:24  skill_reinforc  
2026-09-20T06:47:24  branch          Bamboo fly rod
2026-09-20T08:55:32  parallel_learn  
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
