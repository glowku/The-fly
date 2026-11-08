# REST

REST (Representational State Transfer) est un style d’architecture logicielle conçu pour décrire et guider la conception des systèmes distribués à l’échelle d’Internet, notamment le World Wide Web. Il définit un ensemble de contraintes qui régissent le comportement d’un système hypermedia distribué, tel que le Web. Le style REST met l’accent sur des interfaces uniformes, le déploiement indépendant des composants, la scalabilité des interactions, et l’architecture en couches afin de favoriser la mise en cache, la sécurité et l’encapsulation des systèmes hérités.

## Principes fondamentaux

Les contraintes de REST se concentrent sur quatre axes principaux :  
1. **Interface uniforme** : chaque ressource est identifiée par une URI et manipulée via un ensemble limité de verbes HTTP (GET, POST, PUT, DELETE, etc.).  
2. **Statelessness** : chaque requête du client contient toutes les informations nécessaires à son traitement, sans dépendance sur un état côté serveur.  
3. **Cachabilité** : les réponses peuvent être mises en cache pour réduire la latence perçue par l’utilisateur.  
4. **Architecture en couches** : le système est composé de couches distinctes (proxy, serveur d’application, base de données) qui peuvent être déployées indépendamment tout en conservant la cohérence globale.

## Contraintes et avantages

REST impose également la **séparation des préoccupations** entre le client et le serveur, ce qui permet une évolution indépendante des deux parties. La **scalabilité** est favorisée par la statelessness et la mise en cache, tandis que la **sécurité** est renforcée grâce à l’utilisation de mécanismes standards HTTP (authentification, autorisation, HTTPS). Enfin, le style REST facilite l’intégration de **systèmes hérités** en les encapsulant derrière une interface hypermedia, permettant ainsi une transition progressive vers des architectures modernes.

## Voir aussi

* [[Architecture logicielle]]  
* [[HTTP]]  
* [[Web services]]  
* [[API]]  
* [[HATEOAS]]