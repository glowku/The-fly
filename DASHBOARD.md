# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-08 23:26:58 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **22.345** |
| Concepts traités | 200 | **115** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **115** |
| Arêtes du graphe | 55 |
| Frontière (à explorer) | 14 |
| Profondeur max | 9 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **22.345** |
| Actions dernières 24 h | 187 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 289 |
| Bon (6 – 8) | 6 |
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
2026-11-08T22:24:16  skill_reinforc  
2026-11-08T22:25:23  auto_learn_cyc  
2026-11-08T22:25:25  triage_restore  
2026-11-08T22:25:25  triage          
2026-11-08T22:26:29  skill_reinforc  
2026-11-08T22:27:36  auto_learn_cyc  
2026-11-08T22:28:45  skill_reinforc  
2026-11-08T22:29:53  auto_learn_cyc  
2026-11-08T22:29:55  triage_restore  
2026-11-08T22:29:55  triage          
2026-11-08T22:31:01  skill_reinforc  
2026-11-08T22:32:09  auto_learn_cyc  
2026-11-08T23:01:01  plan            Technical drawing
2026-11-08T23:01:01  skill_reinforc  
2026-11-08T23:01:01  branch          Technical drawing
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
