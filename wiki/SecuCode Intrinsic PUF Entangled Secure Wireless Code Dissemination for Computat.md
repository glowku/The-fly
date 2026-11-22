# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé spécialement conçu pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés uniquement par l’énergie captée dans l’environnement, présentent des contraintes uniques : alimentation intermittente, capacités de calcul limitées et absence d’un système d’exploitation supervisé. SecuCode surmonte ces obstacles en associant une fonction physique non clonable (PUF) intégrée à la mémoire SRAM à un protocole de mise à jour firmware.

## Contexte et problématique

Les CRFID sont de plus en plus utilisés dans l’Internet des objets grâce à leur simplicité de déploiement et leur autonomie énergétique. Cependant, la mise à jour sécurisée de leur firmware reste un défi majeur. Les interruptions fréquentes d’alimentation rendent les protocoles classiques inefficaces, tandis que la faible puissance de calcul empêche l’utilisation de mécanismes cryptographiques lourds. De plus, l’absence d’un système d’exploitation dédié limite les options de sécurisation.

## Principe de fonctionnement

SecuCode intègre la PUF SRAM, un primitive de sécurité matériel intrinsèque, dans le flux de mise à jour. La PUF génère un identifiant unique et difficilement reproductible à partir de la mémoire volatile de l’appareil. Ce dernier est utilisé pour authentifier le firmware et garantir son intégrité avant l’installation. Le protocole est entièrement compatible avec le standard ISO‑18000‑6C, le protocole de communication couramment employé par les CRFID, et s’appuie sur une extension de la plateforme de mise à jour logicielle fournie par Texas Instruments. Ainsi, la mise à jour reste légère, adaptée aux ressources limitées et ne nécessite aucun système d’exploitation supplémentaire.

## Implémentation et résultats

Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai dédié. Les expériences démontrent la conformité aux normes ISO, une faible consommation d’énergie pendant la mise à jour et une robustesse contre les attaques par rejeu ou par falsification de firmware. Les performances mesurées montrent que la procédure de mise à jour peut être exécutée en quelques secondes, même avec des alimentations intermittentes, tout en maintenant un niveau de sécurité élevé grâce à l’utilisation de la PUF.

## Voir aussi

[[Secure coding]], [[Code]], [[Web]], [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]], [[Template-Based Graph Clustering]], [[What Would a Graph Look Like in This Layout A Machine Learning Approach to Large]]