# Lightweight and Direct Document Relevance Optimization for Generative Information Retrieval

Generative information retrieval (GenIR) est un paradigme d’extraction d’information qui transforme la recherche de documents en une tâche de génération d’identifiants de documents (docid). Cette approche permet une optimisation end‑to‑end d’un objectif global de récupération. Cependant, les modèles GenIR actuels souffrent d’un désalignement au niveau des tokens : la prédiction du token suivant ne reflète pas toujours la pertinence globale du document. Les méthodes basées sur l’apprentissage par renforcement, telles que le reinforcement learning from relevance feedback (RLRF), tentent de corriger ce problème via un modèle de récompense, mais introduisent une complexité supplémentaire et une instabilité computationnelle.

## Méthodologie

Le travail propose **Direct Document Relevance Optimization (DDRO)**, une approche qui aligne directement la génération de docid avec l’estimation de la pertinence du document. Plutôt que d’optimiser une fonction de récompense auxiliaire, DDRO utilise un classement par paires pour optimiser directement la pertinence. Cette simplification élimine le besoin de fine‑tuning par renforcement et réduit considérablement la charge computationnelle.

## Résultats et Impact

Sur les jeux de données de référence MS MARCO Document et Natural Questions, DDRO dépasse les méthodes d’apprentissage par renforcement. Il obtient une amélioration de 7,4 % de MRR@10 sur MS MARCO et de 19,9 % sur Natural Questions. Ces gains démontrent que l’optimisation directe de la pertinence peut surpasser les approches plus complexes tout en restant plus stable et plus facile à mettre en œuvre. DDRO ouvre la voie à des systèmes de recherche plus efficaces, capables de s’entraîner de façon plus simple tout en conservant une performance supérieure.

## Voir aussi

* [[Common green bottle fly]]
* [[Black fly]]
* [[Blue-winged Olive flies]]
* [[Insect Festival]]
* [[Bonefish fly patterns]]
* [[Spiracle (vertebrates)]]