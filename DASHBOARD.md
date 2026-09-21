# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-21 09:40:33 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.864** |
| Concepts traités | 200 | **210** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **210** |
| Arêtes du graphe | 278 |
| Frontière (à explorer) | 30 |
| Profondeur max | 9 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **38.864** |
| Actions dernières 24 h | 216 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 205 |
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
2026-09-21T03:41:03  auto_learn      
2026-09-21T03:42:38  auto_learn      
2026-09-21T03:44:12  auto_learn      
2026-09-21T03:45:46  auto_learn      
2026-09-21T03:47:20  auto_learn      
2026-09-21T03:48:54  auto_learn      
2026-09-21T04:49:49  auto_learn      
2026-09-21T06:50:36  plan            List of flying boats and floatplanes
2026-09-21T06:50:36  skill_reinforc  
2026-09-21T06:50:36  branch          List of flying boats and floatplanes
2026-09-21T09:26:36  parallel_learn  
2026-09-21T09:33:08  skill_reinforc  
2026-09-21T09:33:10  auto_learn_exp  Behavior selection algorithm score=8.7
2026-09-21T09:33:10  auto_learn      
2026-09-21T09:34:46  skill_reinforc  
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
