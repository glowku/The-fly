# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-15 13:32:04 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **29.567** |
| Concepts traités | 200 | **152** |
| Qualité moyenne | ≥ 7.5 | **9.73/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **152** |
| Arêtes du graphe | 127 |
| Frontière (à explorer) | 16 |
| Profondeur max | 10 |
| Score qualité moyen | **9.73/10** |
| Score objectif (coverage × quality) | **29.567** |
| Actions dernières 24 h | 143 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 345 |
| Bon (6 – 8) | 8 |
| Moyen (4 – 6) | 5 |
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
2026-11-15T09:47:09  auto_learn_cyc  
2026-11-15T09:48:15  skill_reinforc  
2026-11-15T09:48:15  skill_learn_ar  SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices
2026-11-15T09:49:21  auto_learn_cyc  
2026-11-15T09:49:23  triage_restore  
2026-11-15T09:49:23  triage          
2026-11-15T09:50:25  skill_reinforc  
2026-11-15T09:50:25  skill_learn_ar  What Would a Graph Look Like in This Layout? A Machine Learning Approach to Large Graph Visualization
2026-11-15T09:51:33  auto_learn_cyc  
2026-11-15T09:52:44  skill_reinforc  
2026-11-15T09:52:44  skill_learn_ar  Challenges for Inclusion in Software Engineering: The Case of the Emerging Papua New Guinean Society
2026-11-15T09:53:55  auto_learn_cyc  
2026-11-15T09:53:56  triage_restore  
2026-11-15T09:53:56  triage          
2026-11-15T09:56:02  auto_learn_cyc  
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
