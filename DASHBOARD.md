# 🪰 The Fly — Agent Dashboard

**Dernière mise à jour** : 2026-11-13 02:26:05 UTC

## Objectif de l'agent

Construire un **graphe de connaissance vivant** sur le sujet racine **« mouche evolution »**.

Formule d'optimisation : `coverage_factor × average_quality`

| Objectif | Cible | Actuel |
|----------|-------|--------|
| Score global | maximiser | **28.418** |
| Concepts traités | 200 | **146** |
| Qualité moyenne | ≥ 7.5 | **9.73/10** |

## Métriques actuelles

| Métrique | Valeur |
|----------|--------|
| Concepts traités (nœuds) | **146** |
| Arêtes du graphe | 56 |
| Frontière (à explorer) | 14 |
| Profondeur max | 10 |
| Score qualité moyen | **9.73/10** |
| Score objectif (coverage × quality) | **28.418** |
| Actions dernières 24 h | 113 |

## Répartition de la qualité

| Niveau | Nombre d'articles |
|--------|-------------------|
| Excellent (≥ 8) | 339 |
| Bon (6 – 8) | 8 |
| Moyen (4 – 6) | 4 |
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
2026-11-13T01:26:21  skill_reinforc  
2026-11-13T01:26:21  skill_learn_ar  Navigating the State of Cognitive Flow: Context-Aware AI Interventions for Effective Reasoning Support
2026-11-13T01:27:30  auto_learn_cyc  
2026-11-13T01:28:37  skill_reinforc  
2026-11-13T01:28:37  skill_learn_ar  SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices
2026-11-13T01:29:45  auto_learn_cyc  
2026-11-13T01:29:47  triage_restore  
2026-11-13T01:29:47  triage          
2026-11-13T01:30:50  skill_reinforc  
2026-11-13T01:30:50  skill_learn_ar  What Would a Graph Look Like in This Layout? A Machine Learning Approach to Large Graph Visualization
2026-11-13T01:32:04  auto_learn_cyc  
2026-11-13T01:47:37  triage_restore  
2026-11-13T01:47:37  triage_restore  
2026-11-13T01:47:37  triage          
2026-11-13T01:47:43  auto_learn_cyc  
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
