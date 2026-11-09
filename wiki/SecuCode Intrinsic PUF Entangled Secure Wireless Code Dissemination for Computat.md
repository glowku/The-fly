# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Il associe la fonction physique unique (PUF) d’une mémoire SRAM interne à un protocole de mise à jour firmware, afin de surmonter les contraintes d’alimentation intermittente et de ressources limitées propres aux CRFID. Le système est entièrement compatible avec le protocole ISO‑18000‑6C et s’appuie sur un cadre d’actualisation firmware standardisé fourni par Texas Instruments.

## Contexte et motivation

Les dispositifs CRFID représentent une nouvelle génération d’objets connectés sans batterie, qui tirent leur énergie de l’environnement électromagnétique. Cette approche offre une simplicité de déploiement et une autonomie quasi‑perpétuelle, mais elle rend difficile la sécurisation des mises à jour logicielles. Les contraintes d’alimentation intermittente, la puissance de calcul réduite et l’absence d’un système d’exploitation supervisé compliquent la mise en œuvre de mécanismes de mise à jour traditionnels. SecuCode répond à ces défis en exploitant la PUF SRAM, une primitive de sécurité matérielle intrinsèque, pour authentifier et sécuriser chaque transmission de firmware.

## Architecture et mécanismes

Le cœur de SecuCode repose sur l’entrelacement de la PUF SRAM avec le protocole de mise à jour. Lorsqu’un dispositif reçoit une nouvelle image firmware, la PUF génère un identifiant unique à partir de l’état de la mémoire SRAM, qui est alors utilisé pour chiffrer et signer le paquet de mise à jour. Le dispositif, à son tour, vérifie l’authenticité du firmware en recomputant la réponse PUF et en comparant les signatures. Cette approche élimine le besoin d’une infrastructure de gestion de clés externe et garantit que seule la même unité physique peut accepter la mise à jour. Le système reste conforme aux normes ISO‑18000‑6C grâce à une extension du cadre de mise à jour fourni par Texas Instruments, permettant une intégration transparente avec les protocoles de communication existants.

## Évaluation et conformité

Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai CRFID. Les expérimentations ont démontré la conformité aux standards ISO, la robustesse contre les attaques par rejeu et la capacité à fonctionner sans interruption d’alimentation. Les performances mesurées montrent un temps de mise à jour acceptable pour les applications IoT, tout en conservant une faible consommation d’énergie. Les résultats sont présentés sous forme de visualisations de données, illustrant la fiabilité et la rapidité du processus de mise à jour.

## Voir aussi

* [[Application security]]
* [[Network theory]]
* [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]]
* [[Data and information visualization]]
* [[Diagrammatic reasoning]]