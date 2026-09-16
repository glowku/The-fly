# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-16 08:57:00 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« Fly »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **0.2** |
| Concepts traités | 200 | **1** |
| Qualité moyenne | ≥ 7.5 | **10.0/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **1** |
| Arêtes du graphe | 22 |
| Frontière (à explorer) | 22 |
| Profondeur max | 1 |
| Score qualité moyen | **10.0/10** |
| Score objectif (coverage × quality) | **0.2** |
| Actions dernières 24 h | 1 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 1 |
| Bon (6 – 8) | 0 |
| Moyen (4 – 6) | 0 |
| Faible (< 4) | 0 |

## Top articles par qualité

| Titre | Score | Mots | Liens |
|-------|-------|------|-------|
| [[Fly]] | 10.00 | 208 | 5 |

## Derniers événements de l'agent

```
2026-09-16T08:57:00  expand          Fly score=10.0
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
