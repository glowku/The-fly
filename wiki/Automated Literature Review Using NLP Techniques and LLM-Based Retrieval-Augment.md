# Automated Literature Review Using NLP Techniques and LLM-Based Retrieval-Augmented Generation

Cette étude présente et compare plusieurs approches visant à automatiser la génération de revues de littérature à partir de fichiers PDF. Face à l’augmentation exponentielle du nombre d’articles scientifiques, l’automatisation devient indispensable pour synthétiser rapidement les connaissances existantes. Le travail se concentre sur l’évaluation de trois stratégies NLP et sur l’utilisation d’une génération augmentée par récupération (RAG) avec un modèle de langage large (LLM). Le dataset SciTLDR est employé pour les expériences, et les performances sont mesurées par les scores ROUGE.

## Objectif et contexte

L’objectif principal est de développer un système capable de produire automatiquement des revues de littérature uniquement à partir de documents PDF. Cette ambition répond à la nécessité de réduire le temps et les ressources humaines nécessaires à la lecture et à la synthèse manuelle des travaux de recherche. Le cadre expérimental repose sur le dataset SciTLDR, qui fournit des articles scientifiques et leurs résumés correspondants, offrant un environnement standardisé pour tester les approches proposées.

## Méthodologies comparées

Trois techniques distinctes ont été mises en œuvre :  
1. **Méthode basée sur la fréquence** utilisant spaCy pour extraire les termes les plus fréquents.  
2. **Modèle transformeur Simple T5**, qui génère des résumés à partir de représentations encodées.  
3. **RAG avec GPT‑3.5‑turbo**, combinant la récupération d’extraits pertinents et la génération de texte par un LLM.  
Les systèmes ont été