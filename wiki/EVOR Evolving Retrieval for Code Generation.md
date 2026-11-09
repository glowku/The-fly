# EVOR: Evolving Retrieval for Code Generation

EVOR (Evolving Retrieval for Code Generation) est une approche de génération de code augmentée par recherche (RAG) qui introduit une évolution simultanée des requêtes et des bases de connaissances. Contrairement aux pipelines traditionnels qui utilisent des bases statiques et unique, EVOR exploite des sources multiples et dynamiques afin d’adapter les grands modèles de langage (LLM) aux domaines où leurs connaissances sont limitées. Le système a été évalué sur deux scénarios réalistes nécessitant des connaissances externes, avec la création de quatre nouveaux jeux de données, nommés EVOR‑BENCH, couvrant des bibliothèques fréquemment mises à jour et des langages de programmation de niche.

## Fonctionnement et architecture

Le cœur d’EVOR repose sur un processus itératif où la requête d’un LLM est raffinée en fonction des résultats de recherche obtenus à chaque étape. À chaque itération, le modèle interroge simultanément plusieurs bases de connaissances – documents techniques, API, dépôts GitHub, etc. – et réévalue la requête en fonction des informations extraites. Cette évolution synchronisée permet de corriger les biais initiaux, d’intégrer de nouvelles données et de guider le modèle vers des solutions plus précises. Le pipeline est conçu pour être modulable, ce qui permet de l’intégrer facilement à d’autres méthodes RAG, telles que Reflexion ou DocPrompting, pour un gain supplémentaire en précision.

## Performances et impact

Les expériences menées sur EVOR‑BENCH montrent que EVOR améliore l’exécution correcte du code généré de deux à quatre fois par rapport aux approches existantes. Les gains sont attribués à la diversité des sources d’information et à l’évolution conjointe des requêtes et des documents. Les auteurs soulignent que cette méthode ouvre la voie à des pipelines RACG plus adaptatifs, capables de s’ajuster aux évolutions rapides des bibliothèques logicielles et aux langages émergents. Le code, les modèles et les jeux de données sont publiés sur https://arks-codegen.github.io, favorisant la reproduction et l’expansion de la recherche.

## Voir aussi

- [[Graph database]]
- [[Network theory]]
- [[Cross-origin resource sharing]]
- [[Data and information visualization]]
- [[Technical drawing]]