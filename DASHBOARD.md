# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-18 08:49:37 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **26.399** |
| Concepts traités | 200 | **135** |
| Qualité moyenne | ≥ 7.5 | **9.78/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **135** |
| Arêtes du graphe | 133 |
| Frontière (à explorer) | 25 |
| Profondeur max | 7 |
| Score qualité moyen | **9.78/10** |
| Score objectif (coverage × quality) | **26.399** |
| Actions dernières 24 h | 260 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 133 |
| Bon (6 – 8) | 2 |
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
2026-09-18T03:35:55  skill_reinforc  
2026-09-18T03:35:57  auto_learn_exp  Brewing score=7.33
2026-09-18T03:35:57  auto_learn      
2026-09-18T03:37:33  skill_reinforc  
2026-09-18T03:37:35  auto_learn_exp  Drafting (aerodynamics) score=8.0
2026-09-18T03:37:35  auto_learn      
2026-09-18T03:39:09  skill_reinforc  
2026-09-18T03:39:11  auto_learn_exp  Spiracle (vertebrates) score=10.0
2026-09-18T03:39:11  auto_learn      
2026-09-18T03:40:48  auto_learn      
2026-09-18T04:37:39  auto_learn      
2026-09-18T05:36:45  plan            Housefly
2026-09-18T05:36:45  skill_reinforc  
2026-09-18T05:36:45  branch          Housefly
2026-09-18T08:36:54  parallel_learn  
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
