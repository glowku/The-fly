# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-19 20:08:42 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **34.404** |
| Concepts traités | 200 | **177** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **177** |
| Arêtes du graphe | 202 |
| Frontière (à explorer) | 25 |
| Profondeur max | 7 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **34.404** |
| Actions dernières 24 h | 228 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 173 |
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
2026-09-19T17:26:40  auto_learn      
2026-09-19T17:28:16  auto_learn      
2026-09-19T17:29:53  auto_learn      
2026-09-19T17:31:29  auto_learn      
2026-09-19T17:33:06  auto_learn      
2026-09-19T17:34:42  auto_learn      
2026-09-19T17:36:19  auto_learn      
2026-09-19T17:37:55  auto_learn      
2026-09-19T17:39:32  auto_learn      
2026-09-19T17:41:08  auto_learn      
2026-09-19T17:42:45  auto_learn      
2026-09-19T18:33:34  plan            Two Brothers Brewing
2026-09-19T18:33:34  skill_reinforc  
2026-09-19T18:33:34  branch          Two Brothers Brewing
2026-09-19T19:47:46  parallel_learn  
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
