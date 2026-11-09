# Multi-Turn Agentic Scientific Literature Search via Workflow Induction

Cette approche introduit **PaperPilot**, un agent de recherche scientifique capable d’interagir en plusieurs tours avec l’utilisateur. Contrairement aux agents traditionnels qui reposent sur des pipelines fixes ou uniquement sur le traitement du langage, PaperPilot transforme la recherche en une induction de workflow. À partir d’un article de référence (anchor paper) et d’une requête utilisateur, l’agent construit un graphe dirigé (DAG) d’opérateurs de recherche exécutables, permettant une exploration itérative et contrôlable de la littérature.

## Concepts clés

- **Workflow d’induction** : Le cœur de PaperPilot est un DAG où chaque nœud représente une opération de recherche (recherche par mots‑clés, expansion de citations, filtrage, pondération, reranking, extraction d’évidence). Les arêtes indiquent l’ordre d’exécution et la dépendance entre opérations.
- **Interaction multi‑tour** : L’utilisateur fournit des retours sur les résultats ou sur le workflow lui‑même. Ces feedbacks sont utilisés pour ajuster à la fois la requête et la structure du workflow, assurant une adaptation continue aux intentions scientifiques changeantes.
- **Editabilité explicite** : Contrairement aux agents « boîte noire », le workflow est visible et modifiable, offrant transparence et contrôle sur la stratégie de recherche.

## Architecture et fonctionnement

PaperPilot est entraîné par **imitation de workflow supervisée** et par **optimisation de préférences** sur des corruptions contrôlées de workflows. Le modèle Qwen3.5-9B sert de base, mais PaperPilot-9B intègre la capacité de générer et d’ajuster dynamiquement le DAG. Lors d’une session, l’agent :

1. Génère un workflow initial à partir de l’ancre et de la requête.
2. Exécute le DAG, produisant une liste de papiers et d’extraits pertinents.
3. Recueille les retours de l’utilisateur (ex. pertinence, suggestions de nouveaux mots‑clés).
4. Ré‑entraîne ou ré‑ordonne le workflow en fonction des préférences exprimées.

## Évaluation expérimentale

Les tests montrent que PaperPilot-9B surpasse le agent de base Qwen3.5-9B dans un cadre multi‑tour :

- **Hit@5** : 58.0 → 77.0  
- **MRR** : 47.5 → 59.4  
- **nDCG@10** : 26.8 → 32.5  
- **Erreurs d’exécution de workflow** : 9.5 % → 0 %

Ces améliorations démontrent que la représentation explicite et modifiable des workflows permet une meilleure alignement avec des intentions scientifiques complexes, tout en réduisant les erreurs d’exécution.

## Voir aussi

- [[Graph database]]
- [[Data and information visualization]]
- [[Network theory]]
- [[Technical drawing]]
- [[Area (graph drawing)]]
- [[Angular resolution (graph drawing)]]