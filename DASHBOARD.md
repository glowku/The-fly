# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-09 04:56:40 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **23.117** |
| Concepts traités | 200 | **119** |
| Qualité moyenne | ≥ 7.5 | **9.71/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **119** |
| Arêtes du graphe | 55 |
| Frontière (à explorer) | 14 |
| Profondeur max | 10 |
| Score qualité moyen | **9.71/10** |
| Score objectif (coverage × quality) | **23.117** |
| Actions dernières 24 h | 175 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 295 |
| Bon (6 – 8) | 7 |
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
2026-11-09T01:54:21  triage_restore  
2026-11-09T01:54:22  triage          
2026-11-09T01:55:25  skill_reinforc  
2026-11-09T01:55:25  skill_learn_ar  Neural ranking models for document retrieval
2026-11-09T01:56:32  auto_learn_cyc  
2026-11-09T01:57:37  skill_reinforc  
2026-11-09T01:57:37  skill_learn_ar  Beware of Validation by Eye: Visual Validation of Linear Trends in Scatterplots
2026-11-09T01:58:45  auto_learn_cyc  
2026-11-09T01:58:47  triage_restore  
2026-11-09T01:58:47  triage          
2026-11-09T01:59:50  skill_reinforc  
2026-11-09T02:00:56  auto_learn_cyc  
2026-11-09T02:54:03  plan            Thorax
2026-11-09T02:54:03  skill_reinforc  
2026-11-09T02:54:03  branch          Thorax
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
