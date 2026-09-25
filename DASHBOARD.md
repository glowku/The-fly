# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-25 15:01:19 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.984** |
| Concepts traités | 200 | **263** |
| Qualité moyenne | ≥ 7.5 | **9.75/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **263** |
| Arêtes du graphe | 403 |
| Frontière (à explorer) | 34 |
| Profondeur max | 9 |
| Score qualité moyen | **9.75/10** |
| Score objectif (coverage × quality) | **38.984** |
| Actions dernières 24 h | 157 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 256 |
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
2026-09-25T09:50:42  auto_learn      
2026-09-25T09:52:15  auto_learn      
2026-09-25T09:53:48  auto_learn      
2026-09-25T09:55:21  auto_learn      
2026-09-25T09:56:54  auto_learn      
2026-09-25T09:58:27  auto_learn      
2026-09-25T10:00:01  auto_learn      
2026-09-25T10:01:33  auto_learn      
2026-09-25T10:03:06  auto_learn      
2026-09-25T10:04:40  auto_learn      
2026-09-25T11:29:54  plan            Chewing gum
2026-09-25T11:29:56  skill_reinforc  
2026-09-25T11:29:56  branch          Chewing gum
2026-09-25T11:45:55  auto_learn      
2026-09-25T14:52:39  parallel_learn  
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
