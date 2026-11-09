# A Case-Driven Multi-Agent Framework for E-Commerce Search Relevance

L’optimisation de la pertinence est un pilier de l’expérience utilisateur dans le commerce électronique. Le cadre proposé, intitulé *A Case-Driven Multi-Agent Framework for E-Commerce Search Relevance*, reconsidère l’écosystème traditionnel de la pertinence en remplaçant les rôles humains (utilisateurs, chefs de produit, annotateurs, ingénieurs modèles, évaluateurs) par des agents autonomes. L’objectif est de transformer le processus de résolution des « bad cases » (cas où la pertinence est jugée insuffisante) en un cycle fermé et continu, entièrement automatisé.

## Composants du cadre multi‑agent

Le système se compose de trois agents principaux, chacun incarnant une fonction clé de l’écosystème original :

* **User Agent** – Interagit avec les utilisateurs via un chatbot conversationnel pour identifier les cas de mauvaise pertinence. Il recueille des retours explicites et implicitement, créant ainsi un flux continu de données de mauvaise qualité.
* **Annotator Agent** – Réalise l’annotation multi‑tour des données identifiées, remplaçant les annotateurs humains. Il applique des règles d’annotation cohérentes et met à jour les jeux de données d’entraînement en temps réel.
* **Optimizer Agent** – Analyse les cas annotés, détecte les schémas de défaillance et propose des ajustements de modèles. Il intègre un modèle de pertinence unifié (retrieval‑and‑ranking) pour l’entraînement efficace, ainsi qu’un modèle d’instruction‑following dédié à la résolution instantanée des cas.

Un **Deep Search Agent** cible spécifiquement les échecs d’estimation sous‑optimale, tandis qu’un **Global Memory** assure la réduction de l’asymétrie d’information entre les agents, garantissant une cohérence et une évolution continue du système.

## Implémentation et résultats

Pour rendre le cadre viable en production, les auteurs adoptent une approche « harness‑engineering », construisant un modèle de pertinence unifié qui combine récupération et classement. Ce modèle sert de base à l’entraînement, tandis qu’un modèle d’instruction‑following permet une résolution en temps réel des cas. L’intégration d’un chatbot agent facilite la collaboration homme‑agent, permettant aux humains d’intervenir lorsque nécessaire.

Des évaluations humaines approfondies démontrent que le cadre exécute efficacement les tâches liées à la pertinence, réduisant la fréquence des mauvais cas et améliorant la satisfaction utilisateur. Les agents apprennent continuellement, adaptant les modèles et les annotations sans intervention humaine directe.

## Voir aussi

* [[Data and information visualization]]
* [[Graph database]]
* [[Network theory]]
* [[Cross-origin resource sharing]]