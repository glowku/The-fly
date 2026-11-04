# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-04 08:41:47 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.95** |
| Concepts traités | 200 | **267** |
| Qualité moyenne | ≥ 7.5 | **9.74/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **267** |
| Arêtes du graphe | 430 |
| Frontière (à explorer) | 35 |
| Profondeur max | 9 |
| Score qualité moyen | **9.74/10** |
| Score objectif (coverage × quality) | **38.95** |
| Actions dernières 24 h | 74 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 260 |
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
2026-11-04T02:21:42  auto_learn      
2026-11-04T02:23:19  auto_learn      
2026-11-04T02:24:56  auto_learn      
2026-11-04T02:26:34  auto_learn      
2026-11-04T02:28:10  auto_learn      
2026-11-04T02:29:47  auto_learn      
2026-11-04T02:31:25  auto_learn      
2026-11-04T02:33:01  auto_learn      
2026-11-04T02:34:37  auto_learn      
2026-11-04T02:36:13  auto_learn      
2026-11-04T03:59:50  parallel_learn  
2026-11-04T06:08:45  auto_learn      
2026-11-04T06:52:58  plan            Chewing gum
2026-11-04T06:52:58  skill_reinforc  
2026-11-04T06:52:58  branch          Chewing gum
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
