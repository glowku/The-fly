# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-20 20:25:26 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.922** |
| Concepts traités | 200 | **202** |
| Qualité moyenne | ≥ 7.5 | **9.73/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **202** |
| Arêtes du graphe | 257 |
| Frontière (à explorer) | 28 |
| Profondeur max | 9 |
| Score qualité moyen | **9.73/10** |
| Score objectif (coverage × quality) | **38.922** |
| Actions dernières 24 h | 218 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 197 |
| Bon (6 – 8) | 2 |
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
2026-09-20T17:43:37  auto_learn      
2026-09-20T17:45:10  auto_learn      
2026-09-20T17:46:44  auto_learn      
2026-09-20T17:48:18  auto_learn      
2026-09-20T17:49:51  auto_learn      
2026-09-20T17:51:24  auto_learn      
2026-09-20T17:52:59  auto_learn      
2026-09-20T17:54:33  auto_learn      
2026-09-20T17:56:06  auto_learn      
2026-09-20T17:57:40  auto_learn      
2026-09-20T17:59:14  auto_learn      
2026-09-20T18:58:01  plan            Acoustic ecology
2026-09-20T18:58:01  skill_reinforc  
2026-09-20T18:58:01  branch          Acoustic ecology
2026-09-20T20:00:21  parallel_learn  
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
