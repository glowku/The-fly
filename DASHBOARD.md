# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-28 01:11:51 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **31.744** |
| Concepts traités | 200 | **163** |
| Qualité moyenne | ≥ 7.5 | **9.74/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **163** |
| Arêtes du graphe | 251 |
| Frontière (à explorer) | 16 |
| Profondeur max | 10 |
| Score qualité moyen | **9.74/10** |
| Score objectif (coverage × quality) | **31.744** |
| Actions dernières 24 h | 97 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 354 |
| Bon (6 – 8) | 8 |
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
2026-11-27T22:35:29  triage_restore  
2026-11-27T22:35:29  triage_restore  
2026-11-27T22:35:30  triage          
2026-11-27T22:36:16  auto_learn_cyc  
2026-11-27T22:37:40  auto_learn_cyc  
2026-11-27T22:37:41  triage_restore  
2026-11-27T22:37:41  triage          
2026-11-27T22:39:06  auto_learn_cyc  
2026-11-27T22:40:30  auto_learn_cyc  
2026-11-27T22:40:32  triage_restore  
2026-11-27T22:40:32  triage          
2026-11-27T23:40:11  plan            Saro Windhover
2026-11-27T23:40:12  skill_reinforc  
2026-11-27T23:40:12  branch          Saro Windhover
2026-11-27T23:50:37  parallel_learn  
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
