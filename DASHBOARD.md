# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-19 03:28:33 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **30.671** |
| Concepts traités | 200 | **157** |
| Qualité moyenne | ≥ 7.5 | **9.77/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **157** |
| Arêtes du graphe | 167 |
| Frontière (à explorer) | 26 |
| Profondeur max | 7 |
| Score qualité moyen | **9.77/10** |
| Score objectif (coverage × quality) | **30.671** |
| Actions dernières 24 h | 222 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 154 |
| Bon (6 – 8) | 2 |
| Moyen (4 – 6) | 1 |
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
2026-09-19T03:06:10  auto_learn      
2026-09-19T03:07:44  auto_learn      
2026-09-19T03:09:18  auto_learn      
2026-09-19T03:10:51  auto_learn      
2026-09-19T03:12:25  auto_learn      
2026-09-19T03:13:58  auto_learn      
2026-09-19T03:15:32  auto_learn      
2026-09-19T03:17:06  auto_learn      
2026-09-19T03:18:39  auto_learn      
2026-09-19T03:20:13  auto_learn      
2026-09-19T03:21:47  auto_learn      
2026-09-19T03:23:20  auto_learn      
2026-09-19T03:24:54  auto_learn      
2026-09-19T03:26:27  auto_learn      
2026-09-19T03:28:02  skill_reinforc  
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
