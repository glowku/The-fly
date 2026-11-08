# AI Agent-Driven Framework for Automated Product Knowledge Graph Construction in E-Commerce

Le cadre proposé présente une approche entièrement automatisée pour la construction de graphes de connaissances produits à partir de descriptions non structurées. En exploitant les modèles de langage de grande taille (LLM), le système déploie trois agents dédiés : création d’ontologie, raffinement d’ontologie et population du graphe. Cette architecture élimine la dépendance aux schémas prédéfinis ou aux règles d’extraction manuelles, tout en assurant cohérence sémantique et évolutivité.

## Contexte et Motivation

Les plateformes de commerce électronique génèrent quotidiennement d’énormes volumes de données produit non structurées, ce qui complique les tâches de recherche d’information, de recommandation et d’analyse. Les graphes de connaissances offrent une représentation structurée et interprétable, mais leur construction reste laborieuse et dépendante d’experts. Le cadre décrit vise à automatiser ce processus, réduisant ainsi les coûts de mise en œuvre et accélérant l’intégration de nouvelles catégories de produits.

## Architecture du Cadre

1. **Agent de création d’ontologie** : Le premier agent analyse les descriptions pour identifier les entités, relations et propriétés pertinentes, générant une ontologie initiale sans schéma préexistant.  
2. **Agent de raffinement d’ontologie** : Cet agent vérifie la cohérence sémantique, élimine les redondances et enrichit l’ontologie en ajoutant des concepts manquants.  
3. **Agent de population du graphe** : Enfin, le troisième agent extrait les faits à partir des textes et les insère dans le graphe, garantissant une couverture de propriété supérieure à 97 % et une faible duplication.

Le pipeline est entièrement orchestré par des LLM, qui interprètent les instructions des agents et génèrent les sorties nécessaires à chaque étape. Cette approche garantit une adaptation rapide aux nouveaux types de produits sans intervention humaine.

## Évaluation et Résultats

Le cadre a été testé sur un jeu de données réel de descriptions d’air‑conditionneurs. Les métriques montrent une couverture de propriété de 97 % et une réduction notable de la redondance par rapport aux méthodes traditionnelles. Les évaluations qualitatives confirment la cohérence sémantique du graphe produit, attestant de la robustesse de l’architecture agent‑driven.

## Voir aussi

- [[Blowfly (musician)]]
- [[Adaptive compliant wing]]
- [[Helicopter flight controls]]
- [[Insect Festival]]