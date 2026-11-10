# Retrieval-augmented generation

Retrieval-augmented generation (RAG) est une technique qui permet aux grands modèles de langage (LLMs) de récupérer et d’intégrer des informations provenant de sources externes. En pratique, un LLM consulte d’abord un corpus de documents prédéfinis avant de répondre à une requête utilisateur. Ces documents complètent les connaissances déjà présentes dans le modèle, offrant ainsi un accès à des données de domaine spécifique ou à des informations actualisées qui ne figuraient pas dans le jeu de données d’entraînement. Cette approche a été proposée pour la première fois en 2020 et s’est rapidement imposée comme une méthode courante dans les systèmes d’IA modernes, notamment pour les chatbots d’entreprise capables d’accéder à des bases internes ou de se baser sur des sources autorisées.

## Mécanisme de fonctionnement

Le processus RAG se décompose en deux phases principales :  
1. **Récupération** – le LLM interroge un index de documents (souvent construit à l’aide de techniques de vectorisation ou de recherche par similarité) pour sélectionner les passages les plus pertinents.  
2. **Génération** – le modèle intègre ces passages dans son contexte de génération afin de produire une réponse cohérente et informée.  

Cette combinaison de recherche et de génération permet de surmonter les limites de la mémoire interne du modèle et de garantir que les réponses reflètent les dernières connaissances disponibles.

## Applications et perspectives

RAG est particulièrement utile dans des domaines où la précision et la mise à jour des informations sont critiques, comme la recherche scientifique, le support technique ou la conformité réglementaire. En exploitant des sources fiables, les systèmes RAG peuvent fournir des réponses plus exactes et réduire le risque de désinformation. De plus, la méthode s’intègre naturellement aux architectures multi‑agents et aux workflows de recherche automatisée, ouvrant la voie à des applications avancées telles que la recherche scientifique en temps réel ou la génération de code basée sur des bibliothèques actualisées.

## Voir aussi

[[Graph theory]]  
[[Automated reasoning]]  
[[Searching Scientific Literature for Answers on COVID-19 Questions]]  
[[Application security]]  
[[Diagrammatic reasoning]]