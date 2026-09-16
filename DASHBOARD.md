# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-16 11:06:20 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

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
| Arêtes du graphe | 5 |
| Frontière (à explorer) | 5 |
| Profondeur max | 1 |
| Score qualité moyen | **10.0/10** |
| Score objectif (coverage × quality) | **0.2** |
| Actions dernières 24 h | 33 |

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
| [[Evolution]] | 10.00 | 298 | 6 |

## Derniers événements de l'agent

```
2026-09-16T10:34:40  reset_root      
2026-09-16T10:34:41  skip            Fly intelligence
2026-09-16T10:35:17  reset_root      
2026-09-16T10:35:18  skip            insect flying
2026-09-16T10:58:37  reset_root      
2026-09-16T10:58:42  skip            ecology fly
2026-09-16T11:04:05  reset_root      
2026-09-16T11:04:09  skill_reinforc  
2026-09-16T11:04:11  expand          Ecology score=10.0
2026-09-16T11:04:33  reset_root      
2026-09-16T11:04:41  skill_reinforc  
2026-09-16T11:04:42  expand          Computer security score=10.0
2026-09-16T11:06:14  reset_root      
2026-09-16T11:06:18  skill_reinforc  
2026-09-16T11:06:19  expand          Evolution score=10.0
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
