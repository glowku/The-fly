# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-23 13:24:01 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **38.866** |
| Concepts traités | 200 | **252** |
| Qualité moyenne | ≥ 7.5 | **9.72/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **252** |
| Arêtes du graphe | 377 |
| Frontière (à explorer) | 37 |
| Profondeur max | 9 |
| Score qualité moyen | **9.72/10** |
| Score objectif (coverage × quality) | **38.866** |
| Actions dernières 24 h | 214 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 244 |
| Bon (6 – 8) | 5 |
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
2026-09-23T11:15:22  auto_learn      
2026-09-23T11:17:02  skill_reinforc  
2026-09-23T11:17:04  auto_learn_exp  Chemical ecology score=10.0
2026-09-23T11:17:04  auto_learn      
2026-09-23T11:18:47  auto_learn      
2026-09-23T11:20:30  auto_learn      
2026-09-23T11:22:14  auto_learn      
2026-09-23T11:23:57  auto_learn      
2026-09-23T11:25:40  auto_learn      
2026-09-23T11:29:02  skill_reinforc  
2026-09-23T11:29:04  auto_learn_exp  Social and behavior change communication score=10.0
2026-09-23T11:29:04  auto_learn      
2026-09-23T12:58:12  plan            Abundance (ecology)
2026-09-23T12:58:23  skill_reinforc  
2026-09-23T12:58:23  branch          Abundance (ecology)
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
