---
skill: code_et_outils
topic: clean architecture for autonomous agents
created: 2026-11-08T09:53:45.757281+00:00
---

## Contexte  
Les agents autonomes (IA, robots, systèmes de décision) doivent évoluer dans des environnements complexes tout en restant maintenables, testables et sécurisés.  
La **clean architecture** (architecture propre) sépare clairement les responsabilités :  
- **Domain** (logique métier)  
- **Use‑cases** (scénarios d’usage)  
- **Interface adapters** (adaptateurs d’entrée/sortie)  
- **Frameworks & Drivers** (bases de données, APIs, UI)  

Cette séparation permet de modifier l’une sans impacter les autres, ce qui est crucial pour les agents qui doivent intégrer de nouveaux capteurs, algorithmes ou services sans réécrire l’ensemble du code.

## Méthode  
1. **Définir le domaine**  
   - Listez les entités métier (ex. : `Perception`, `Planification`, `Action`) et leurs invariants.  
   - Écrivez des interfaces (`IPerception`, `IPlanification`) sans dépendances externes.  

2. **Concevoir les use‑cases**  
   - Chaque use‑case représente un scénario complet (ex. : « Réagir à un obstacle »).  
   - Implémentez‑les en classes concrètes qui dépendent uniquement des interfaces du domaine.  

3. **Adapter les interfaces**  
   - Créez des adaptateurs pour chaque technologie (capteurs, moteurs, services cloud).  
   - Utilisez des *ports* (entrée) et *adapters* (sortie) pour isoler le domaine des frameworks.  

4. **Intégrer les graphes de décision**  
   - Modélisez les flux d’action sous forme de graphes (ex. : graphes de décision, arbres de décision, réseaux de Markov).  
   - Implémentez un *graph engine* qui consomme les use‑cases et renvoie des actions.  

5. **Sécurité défensive**  
   - **Validation** : chaque entrée (capteur, commande externe) doit être validée contre un schéma strict.  
   - **Isolation** : exécutez les use‑cases dans des processus ou conteneurs séparés (sandbox).  
   - **Audit** : loggez toutes les décisions et actions avec horodatage, identifiant de l’agent, et hash de la configuration.  

6. **Tests**  
   - Unitaires sur le domaine et les use‑cases.  
   - Tests d’intégration sur les adaptateurs.  
   - Tests de résistance sur le graph engine (ex. : injection de données erronées).  

## Pièges  
- **Couplage fort** : ne pas introduire de dépendances directes vers les frameworks dans le domaine.  
- **Sur‑spécialisation** : éviter de créer trop de petites interfaces qui compliquent la maintenance.  
- **Graphes non testables** : si le moteur de graph n’est pas isolé, les tests deviennent intrusifs.  
- **Sécurité négligée** : oublier de sandboxer les modules externes expose l’agent à des attaques de type injection.  

## Checklist  
- [ ] Entités métier définies avec invariants clairs.  
- [ ] Interfaces de domaine sans dépendances externes.  
- [ ] Use‑cases implémentés, testés isolément.  
- [ ] Adaptateurs pour chaque technologie, validant les données.  
- [ ] Graph engine séparé, testable.  
- [ ] Validation stricte des entrées.  
- [ ] Sandbox ou conteneurisation des modules externes.  
- [ ] Journalisation complète des décisions.  
- [ ] Suite de tests unitaires, d’intégration et de résistance.  
- [ ] Documentation de l’architecture (diagrammes, conventions).  

En suivant cette démarche, l’agent reste modulaire, testable et résistant aux attaques, tout en permettant une évolution rapide grâce à la séparation claire des responsabilités.
