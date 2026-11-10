# Continuous integration

La **continuous integration** (CI) est une pratique de développement logiciel visant à intégrer fréquemment les modifications de code source et à garantir que la base de code intégrée reste dans un état fonctionnel. Les développeurs fusionnent généralement leurs changements dans une branche d’intégration, puis un système automatisé construit et teste le logiciel. Ce processus peut être déclenché à chaque commit ou selon un planning, par exemple une fois par jour.

## Principes de base

La CI repose sur trois piliers essentiels :  
1. **Intégration fréquente** – les changements sont fusionnés plusieurs fois par jour pour éviter les conflits majeurs.  
2. **Automatisation** – un serveur CI exécute automatiquement les scripts de construction et les suites de tests.  
3. **Feedback rapide** – les résultats de la construction et des tests sont immédiatement communiqués aux développeurs, permettant une correction rapide des défauts.

## Processus automatisé

Un pipeline CI typique comprend les étapes suivantes :  
- **Build** : compilation du code et génération des artefacts.  
- **Test** : exécution de tests unitaires, d’intégration et parfois de tests de performance.  
- **Analyse statique** : vérification de la qualité du code et détection de vulnérabilités potentielles.  
- **Déploiement** : mise à disposition d’une version de test dans un environnement d’intégration.  

Ces étapes sont orchestrées par un outil CI (ex. Jenkins, GitLab CI, GitHub Actions) et peuvent être configurées pour s’exécuter à chaque commit ou selon une cadence définie.

## Historique

Le terme « continuous integration » a été introduit par Grady Booch en 1991. À l’origine, Booch ne prônait pas l’intégration plusieurs fois par jour, mais la pratique a évolué pour inclure cette fréquence afin de réduire les risques de conflits et d’accélérer le cycle de livraison. Depuis, la CI est devenue un élément central des méthodologies agiles et DevOps.

## Voir aussi

- [[Graph database]]
- [[Network theory]]
- [[Application security]]
- [[Automated reasoning]]
- [[Graphics processing unit]]
- [[Diagrammatic reasoning]]