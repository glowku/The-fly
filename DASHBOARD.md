# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-19 08:35:43 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **31.271** |
| Concepts traités | 200 | **160** |
| Qualité moyenne | ≥ 7.5 | **9.77/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **160** |
| Arêtes du graphe | 173 |
| Frontière (à explorer) | 28 |
| Profondeur max | 7 |
| Score qualité moyen | **9.77/10** |
| Score objectif (coverage × quality) | **31.271** |
| Actions dernières 24 h | 218 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 157 |
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
2026-09-19T03:31:14  auto_learn      
2026-09-19T03:32:48  skill_reinforc  
2026-09-19T03:32:50  auto_learn_exp  Bamboo fly rod score=10.0
2026-09-19T03:32:50  auto_learn      
2026-09-19T03:34:23  auto_learn      
2026-09-19T03:35:56  auto_learn      
2026-09-19T03:37:28  auto_learn      
2026-09-19T03:39:03  skill_reinforc  
2026-09-19T03:39:05  auto_learn_exp  Sexual antagonistic coevolution score=10.0
2026-09-19T03:39:05  auto_learn      
2026-09-19T04:32:57  auto_learn      
2026-09-19T07:07:43  plan            Blowfly's Punk Rock Party
2026-09-19T07:07:44  skill_reinforc  
2026-09-19T07:07:44  branch          Blowfly's Punk Rock Party
2026-09-19T08:24:09  parallel_learn  
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
