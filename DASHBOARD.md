# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-10-17 08:18:07 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.992** |
| Concepts traités | 200 | **265** |
| Qualité moyenne | ≥ 7.5 | **9.75/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **265** |
| Arêtes du graphe | 412 |
| Frontière (à explorer) | 35 |
| Profondeur max | 9 |
| Score qualité moyen | **9.75/10** |
| Score objectif (coverage × quality) | **38.992** |
| Actions dernières 24 h | 116 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 258 |
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
2026-10-17T03:18:15  auto_learn      
2026-10-17T03:19:49  auto_learn      
2026-10-17T03:21:22  auto_learn      
2026-10-17T03:22:55  auto_learn      
2026-10-17T03:24:27  auto_learn      
2026-10-17T03:26:01  auto_learn      
2026-10-17T03:27:34  auto_learn      
2026-10-17T03:29:06  auto_learn      
2026-10-17T03:30:40  auto_learn      
2026-10-17T03:32:13  auto_learn      
2026-10-17T04:18:56  auto_learn      
2026-10-17T05:56:49  plan            Chewing gum
2026-10-17T05:56:49  skill_reinforc  
2026-10-17T05:56:49  branch          Chewing gum
2026-10-17T08:09:10  parallel_learn  
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
