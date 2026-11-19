# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, dépourvus de batterie, tirent toute leur énergie de la radiofréquence et disposent de capacités de calcul limitées. Le principal défi est de garantir l’intégrité et la confidentialité des firmwares transmis alors que l’alimentation est intermittente et qu’aucun système d’exploitation supervisé n’existe.

## Contexte et enjeux
Les CRFID représentent une nouvelle classe d’objets connectés à l’Internet des objets, grâce à leur simplicité de déploiement et à leur fonctionnement continu grâce à la récupération d’énergie. Cependant, la mise à jour sans fil de leur firmware reste problématique : l’alimentation sporadique, les ressources de calcul restreintes et l’absence d’un OS de supervision rendent les protocoles classiques inadaptés. De plus, la sécurité de la chaîne d'approvisionnement est cruciale pour éviter la propagation de logiciels malveillants dans l’écosystème IoT.

## Architecture et fonctionnement de SecuCode
SecuCode intègre une fonction physique non clonable (PUF) basée sur la mémoire SRAM du dispositif. Cette PUF intrinsèque sert de clé d’authentification unique, liée à l’appareil, et est combinée à un protocole de mise à jour firmware. Le design repose sur un cadre d’actualisation fourni par Texas Instruments, étendu pour être compatible avec le protocole ISO‑18000‑6C largement utilisé par les CRFID. Ainsi, la mise à jour reste conforme aux normes industrielles tout en restant adaptée aux contraintes énergétiques et de calcul des appareils.

## Évaluation et conformité
Une implémentation complète de SecuCode a été réalisée et testée sur plusieurs dispositifs CRFID. Les expérimentations démontrent la conformité aux standards ISO‑18000‑6C, évaluent les performances (temps de mise à jour, consommation énergétique) et attestent de la robustesse contre les attaques classiques (replay, falsification de firmware). Les résultats indiquent que SecuCode offre une solution viable pour la sécurisation des mises à jour sans fil dans un environnement à ressources limitées.

## Voir aussi
[[Computational RFID]], [[Physical Unclonable Function]], [[ISO-18000-6C]], [[Firmware update]], [[Texas Instruments]], [[ArXiv]]