# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-14 08:40:20 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **28.608** |
| Concepts traités | 200 | **147** |
| Qualité moyenne | ≥ 7.5 | **9.73/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **147** |
| Arêtes du graphe | 122 |
| Frontière (à explorer) | 14 |
| Profondeur max | 10 |
| Score qualité moyen | **9.73/10** |
| Score objectif (coverage × quality) | **28.608** |
| Actions dernières 24 h | 141 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 340 |
| Bon (6 – 8) | 9 |
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
2026-11-14T05:53:21  triage          
2026-11-14T06:53:27  triage_restore  
2026-11-14T06:53:27  triage_restore  
2026-11-14T06:53:27  triage          
2026-11-14T06:54:35  auto_learn_cyc  
2026-11-14T06:56:41  auto_learn_cyc  
2026-11-14T06:56:42  triage_restore  
2026-11-14T06:56:42  triage          
2026-11-14T06:58:48  auto_learn_cyc  
2026-11-14T07:00:53  auto_learn_cyc  
2026-11-14T07:00:55  triage_restore  
2026-11-14T07:00:55  triage          
2026-11-14T07:03:02  auto_learn_cyc  
2026-11-14T07:04:00  densify_edges   
2026-11-14T08:19:39  parallel_learn  
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
