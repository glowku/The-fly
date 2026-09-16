# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-16 08:59:43 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« Fly »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **0.4** |
| Concepts traités | 200 | **2** |
| Qualité moyenne | ≥ 7.5 | **10.0/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **2** |
| Arêtes du graphe | 44 |
| Frontière (à explorer) | 42 |
| Profondeur max | 2 |
| Score qualité moyen | **10.0/10** |
| Score objectif (coverage × quality) | **0.4** |
| Actions dernières 24 h | 3 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 2 |
| Bon (6 – 8) | 0 |
| Moyen (4 – 6) | 0 |
| Faible (< 4) | 0 |

## Top articles par qualité

| Titre | Score | Mots | Liens |
|-------|-------|------|-------|
| [[Fly]] | 10.00 | 208 | 5 |
| [[Anus]] | 10.00 | 292 | 5 |

## Derniers événements de l'agent

```
2026-09-16T08:57:00  expand          Fly score=10.0
2026-09-16T08:59:40  plan            Anus
2026-09-16T08:59:43  expand          Anus score=10.0
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
