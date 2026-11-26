# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID à puissance auto-générée (CRFID). Il combine une fonction physique non clonable (PUF) basée sur la mémoire SRAM du dispositif avec un protocole de mise à jour firmware, afin de garantir l’intégrité et l’authenticité du code distribué, même en présence de coupures d’alimentation intermittentes et de ressources computationnelles limitées.

## Conception et architecture

La solution repose sur l’entrelacement d’une PUF SRAM intrinsèque à la procédure de mise à jour. La PUF génère un identifiant unique à chaque fois que le dispositif est alimenté, sans nécessiter de stockage permanent. Ce jeton est utilisé pour signer cryptographiquement le firmware avant son transmission. Le protocole de mise à jour est entièrement compatible avec le standard ISO‑18000‑6C, le protocole de communication le plus répandu pour les CRFID, et s’intègre à un cadre d’actualisation fourni par Texas Instruments. Le firmware est compilé et signé à l’aide d’un outil standard de l’industrie, puis distribué via le protocole ISO‑18000‑6C. Le dispositif, lorsqu’il reçoit un paquet, vérifie d’abord l’authenticité du firmware à l’aide de la signature et de la PUF, puis l’installe si les vérifications réussissent.

## Évaluation et performances

Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai dédié. Les mesures montrent que la mise à jour peut être effectuée en quelques secondes, même avec des alimentations intermittentes, et que la consommation énergétique supplémentaire reste négligeable par rapport à la capacité d’auto-génération du dispositif. Les tests de sécurité démontrent la résistance de la méthode aux attaques par falsification de firmware, aux tentatives de duplication de la PUF et aux écarts de timing. En outre, la solution respecte les exigences de conformité aux normes industrielles, notamment celles relatives à la sécurité des communications sans fil et à la gestion des mises à jour.

## Compatibilité et déploiement

SecuCode est conçu pour être déployé sans modification majeure du matériel existant. Il s’appuie sur les protocoles et outils déjà standards dans l’industrie des RFID, ce qui facilite son adoption dans les chaînes d’approvisionnement et les systèmes IoT. Les développeurs peuvent intégrer la PUF et le protocole de mise à jour dans leurs flux de travail de développement logiciel grâce à des extensions de compilateurs et de gestion de firmware déjà disponibles.

## Voir aussi

* [[Secure coding]]
* [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]]
* [[Visual Studio]]
* [[Autonomous agent]]