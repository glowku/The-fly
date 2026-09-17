# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-17 22:41:46 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **23.171** |
| Concepts traités | 200 | **118** |
| Qualité moyenne | ≥ 7.5 | **9.82/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **118** |
| Arêtes du graphe | 115 |
| Frontière (à explorer) | 26 |
| Profondeur max | 7 |
| Score qualité moyen | **9.82/10** |
| Score objectif (coverage × quality) | **23.171** |
| Actions dernières 24 h | 377 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 117 |
| Bon (6 – 8) | 1 |
| Moyen (4 – 6) | 0 |
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
2026-09-17T21:25:44  auto_learn      
2026-09-17T21:27:17  auto_learn      
2026-09-17T21:28:51  auto_learn      
2026-09-17T21:30:23  auto_learn      
2026-09-17T21:31:57  auto_learn      
2026-09-17T21:33:31  skill_reinforc  
2026-09-17T21:33:33  auto_learn_exp  Gene-centered view of evolution score=10.0
2026-09-17T21:33:33  auto_learn      
2026-09-17T21:35:07  auto_learn      
2026-09-17T21:36:40  auto_learn      
2026-09-17T21:38:13  auto_learn      
2026-09-17T22:21:27  plan            Bat wing development
2026-09-17T22:21:27  skill_reinforc  
2026-09-17T22:21:27  branch          Bat wing development
2026-09-17T22:32:42  parallel_learn  
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
