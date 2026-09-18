# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-09-18 18:54:32 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **28.599** |
| Concepts traités | 200 | **146** |
| Qualité moyenne | ≥ 7.5 | **9.79/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **146** |
| Arêtes du graphe | 148 |
| Frontière (à explorer) | 19 |
| Profondeur max | 7 |
| Score qualité moyen | **9.79/10** |
| Score objectif (coverage × quality) | **28.599** |
| Actions dernières 24 h | 231 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 144 |
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
2026-09-18T14:27:38  auto_learn      
2026-09-18T14:29:12  auto_learn      
2026-09-18T14:30:46  auto_learn      
2026-09-18T14:32:20  auto_learn      
2026-09-18T14:33:54  auto_learn      
2026-09-18T14:35:28  auto_learn      
2026-09-18T14:37:02  skill_reinforc  
2026-09-18T14:48:56  plan            Evolutionary arms race
2026-09-18T14:48:57  skill_reinforc  
2026-09-18T14:48:57  branch          Evolutionary arms race
2026-09-18T16:21:06  auto_learn      
2026-09-18T17:33:42  parallel_learn  
2026-09-18T18:07:17  plan            Acoustic ecology
2026-09-18T18:07:18  skill_reinforc  
2026-09-18T18:07:18  branch          Acoustic ecology
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
