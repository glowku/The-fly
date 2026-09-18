# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-18 03:31:40 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **25.493** |
| Concepts traités | 200 | **130** |
| Qualité moyenne | ≥ 7.5 | **9.8/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **130** |
| Arêtes du graphe | 128 |
| Frontière (à explorer) | 24 |
| Profondeur max | 7 |
| Score qualité moyen | **9.8/10** |
| Score objectif (coverage × quality) | **25.493** |
| Actions dernières 24 h | 297 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 129 |
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
2026-09-18T03:08:33  auto_learn      
2026-09-18T03:10:09  auto_learn      
2026-09-18T03:11:46  auto_learn      
2026-09-18T03:13:22  auto_learn      
2026-09-18T03:14:58  auto_learn      
2026-09-18T03:16:35  auto_learn      
2026-09-18T03:18:11  auto_learn      
2026-09-18T03:19:47  auto_learn      
2026-09-18T03:21:24  auto_learn      
2026-09-18T03:23:00  auto_learn      
2026-09-18T03:24:36  auto_learn      
2026-09-18T03:26:12  auto_learn      
2026-09-18T03:27:48  auto_learn      
2026-09-18T03:29:24  auto_learn      
2026-09-18T03:31:03  skill_reinforc  
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
