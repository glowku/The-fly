# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-16 09:53:06 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« Fly away »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **0.0** |
| Concepts traités | 200 | **0** |
| Qualité moyenne | ≥ 7.5 | **0.0/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **0** |
| Arêtes du graphe | 0 |
| Frontière (à explorer) | 0 |
| Profondeur max | 0 |
| Score qualité moyen | **0.0/10** |
| Score objectif (coverage × quality) | **0.0** |
| Actions dernières 24 h | 13 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 0 |
| Bon (6 – 8) | 0 |
| Moyen (4 – 6) | 0 |
| Faible (< 4) | 0 |

## Top articles par qualité

| Titre | Score | Mots | Liens |
|-------|-------|------|-------|

## Derniers événements de l'agent

```
2026-09-16T08:57:00  expand          Fly score=10.0
2026-09-16T08:59:40  plan            Anus
2026-09-16T08:59:43  expand          Anus score=10.0
2026-09-16T09:25:46  skill_reinforc  
2026-09-16T09:25:47  expand          Fly score=10.0
2026-09-16T09:40:57  skill_reinforc  
2026-09-16T09:40:58  expand          Fly score=10.0
2026-09-16T09:42:59  skill_reinforc  
2026-09-16T09:43:00  expand          Fly score=10.0
2026-09-16T09:49:00  skill_reinforc  
2026-09-16T09:49:02  expand          Fly score=10.0
2026-09-16T09:53:04  reset_root      
2026-09-16T09:53:06  skip            Fly away
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
