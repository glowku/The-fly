# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Il combine une fonction physique non clonable (PUF) basée sur la mémoire SRAM avec un protocole de mise à jour firmware, afin de surmonter les contraintes d’alimentation intermittente, de ressources limitées et l’absence de système d’exploitation supervisé. Le système est entièrement compatible avec les protocoles de communication existants, notamment ISO‑18000‑6C, et s’appuie sur une méthode d’assemblage et de mise à jour firmware conforme aux normes industrielles, étendue d’un cadre récent fourni par Texas Instruments.

## Contexte et défis
Les dispositifs CRFID tirent leur énergie de l’environnement radio, ce qui les rend autonomes mais aussi sujets à des interruptions d’alimentation fréquentes. Leur faible puissance de calcul et l’absence de système d’exploitation rendent les mises à jour logicielles vulnérables aux attaques de falsification et de relecture. De plus, l’absence de mécanismes de chiffrement robustes et de vérification d’intégrité rend difficile la diffusion sécurisée de firmware sur le réseau sans fil.

## Architecture et fonctionnement
SecuCode intègre la PUF SRAM comme clé unique et intrinsèque à chaque dispositif. Lors d’une mise à jour, le serveur génère un challenge PUF et un code de mise à jour signé. Le dispositif, en récupérant l’énergie nécessaire, exécute la PUF pour produire la réponse, qui est comparée à la valeur attendue. Si la vérification réussit, le firmware est décrypté et flashé. Cette approche élimine le besoin d’une clé de stockage permanente et garantit que seule la cible authentique peut accepter la mise à jour. Le protocole exploite les échanges ISO‑18000‑6C, ce qui permet une intégration transparente avec les lecteurs RFID existants.

## Évaluation et conformité
Une implémentation complète a été réalisée et testée sur des plateformes CRFID réelles. Les résultats montrent une conformité totale aux spécifications ISO‑18000‑6C, une latence de mise à jour acceptable (quelques dizaines de secondes) et une robustesse contre les attaques par relecture et par falsification. Les mesures de performance indiquent que la consommation énergétique supplémentaire due à la PUF reste bien en dessous de la capacité d’énergie disponible, assurant ainsi une opération perpétuelle sans compromis sur la durée de vie de la batterie.

## Voir aussi
[[Secure coding]], [[Visual Studio]], [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]], [[Diagrammatology]]