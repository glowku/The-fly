# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Il exploite la fonction physique non clonable (PUF) intégrée dans la mémoire SRAM du dispositif afin de lier la sécurité du firmware à une caractéristique matérielle unique. Cette approche permet de surmonter les contraintes de puissance intermittente, de capacité de calcul limitée et l’absence de système d’exploitation supervisé propres aux CRFID.

## Contexte et motivation

Les dispositifs CRFID tirent leur énergie de l’environnement grâce à la récupération d’énergie sans fil, ce qui les rend autonomes et sans batterie. Cependant, cette même caractéristique rend difficile la distribution sécurisée de mises à jour logicielles, car les dispositifs peuvent être déconnectés ou perdre de l’énergie à tout moment. De plus, leur faible puissance de calcul empêche l’utilisation de protocoles de mise à jour classiques. SecuCode répond à ces défis en intégrant la PUF SRAM dans le protocole de mise à jour, assurant ainsi l’authenticité et l’intégrité du firmware sans nécessiter de ressources supplémentaires.

## Architecture et mise en œuvre

Le système se compose de trois éléments clés : (1) la PUF SRAM, qui génère un identifiant matériel unique à chaque dispositif ; (2) un protocole de mise à jour firmware compatible avec le standard ISO‑18000‑6C, utilisé couramment par les CRFID ; (3) une extension du cadre de mise à jour fourni par Texas Instruments, qui permet de compiler et de déployer le firmware de façon standardisée. L’implémentation de SecuCode a été testée sur un dispositif CRFID réel, démontrant la conformité aux normes existantes, une faible consommation énergétique et une robustesse contre les attaques par falsification de firmware.

## Évaluation et perspectives

Des expériences approfondies ont montré que SecuCode maintient la sécurité même en présence de pertes d’alimentation fréquentes. Les performances de mise à jour restent acceptables pour les applications IoT, et la compatibilité avec les protocoles existants facilite son adoption. Les auteurs suggèrent que cette approche pourrait être étendue à d’autres classes de dispositifs sans batterie, ouvrant la voie à une sécurisation généralisée des mises à jour logicielles dans l’Internet des objets.

## Voir aussi

[[Canvassing]], [[Image]], [[Graph theory]], [[Supply chain security]], [[ArXiv]], [[ISO‑18000‑6C]]