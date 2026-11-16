# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés uniquement par l’énergie captée dans leur environnement, offrent une autonomie sans batterie mais posent des défis majeurs en matière de sécurité. L’article décrit comment l’intégration d’une fonction physique non clonable (PUF) basée sur la mémoire SRAM permet de sécuriser les transmissions de firmware tout en respectant les contraintes de puissance et de calcul propres aux CRFID.

## Contexte et défis des CRFID

Les CRFID représentent une nouvelle génération d’objets connectés, capables de réaliser des tâches de calcul et de capteur tout en se rechargeant grâce à l’énergie radio. Leur absence d’alimentation permanente et de système d’exploitation supervisé rend les mises à jour logicielles particulièrement fragiles : les interruptions de courant peuvent interrompre la transmission, et les ressources limitées limitent les protocoles cryptographiques classiques. De plus, la communication se fait généralement via le protocole ISO‑18000‑6C, imposant des contraintes de format et de timing.

## Architecture et mécanismes de SecuCode

SecuCode repose sur l’entrelacement d’une PUF SRAM intrinsèque avec un protocole d’update. La PUF, générée à partir de la mémoire volatile du dispositif, fournit une identité unique et difficilement reproductible. Lorsqu’un firmware est envoyé, le serveur calcule un hachage signé qui est vérifié par la PUF du CRFID, garantissant l’authenticité et l’intégrité du code sans nécessiter de stockage persistant. Le protocole est implémenté en étendant un cadre de mise à jour fourni par Texas Instruments, assurant ainsi la compatibilité avec les compilateurs et outils industriels existants.

## Évaluation et conformité aux standards

Une implémentation complète a été réalisée et testée sur des plateformes CRFID réelles. Les expérimentations montrent que SecuCode respecte les spécifications ISO‑18000‑6C, tout en maintenant un temps de mise à jour acceptable malgré l’alimentation intermittente. Les mesures de performance indiquent que la surcharge cryptographique est négligeable par rapport aux ressources disponibles, et les tests de sécurité démontrent la résistance aux attaques par falsification de firmware et aux tentatives de clonage matériel.

## Voir aussi

[[ArXiv]] [[Code]] [[Supply chain security]] [[Visual system]] [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]]