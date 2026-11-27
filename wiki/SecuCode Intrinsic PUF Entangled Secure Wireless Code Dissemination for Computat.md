# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, spécialement conçu pour les dispositifs RFID computationnels (CRFID). Ces appareils, dépourvus de batterie, récupèrent toute leur énergie via l’harvesting électromagnétique, ce qui rend la gestion de la sécurité et des mises à jour particulièrement délicate.

## Principe de fonctionnement

Le cœur de SecuCode réside dans l’entrelacement d’une fonction physique unique (PUF) basée sur la mémoire SRAM du dispositif avec le protocole de mise à jour firmware. La PUF, intrinsèque à chaque puce, génère un identifiant matériel non clonable qui sert à authentifier le firmware avant son déploiement. Cette approche permet de contourner les contraintes d’alimentation intermittente et de ressources limitées propres aux CRFID, tout en évitant l’intervention d’un système d’exploitation supervisé.

## Implémentation et performances

SecuCode a été intégré dans un pipeline complet de compilation et de mise à jour fourni par Texas Instruments, en étendant un cadre récent dédié aux firmware CRFID. L’implémentation respecte les spécifications ISO‑18000‑6C, assurant ainsi la compatibilité avec les protocoles de communication déjà utilisés par les dispositifs. Des expériences de terrain ont montré que le processus de mise à jour reste fiable même sous des conditions d’alimentation très variables, tout en maintenant un niveau de sécurité élevé grâce à la PUF.

## Conformité aux normes et sécurité

Le système a été validé par rapport aux normes industrielles en vigueur, garantissant que les mises à jour sont délivrées de manière authentifiée et intégrité vérifiée. L’utilisation de la PUF élimine la nécessité de stocker des clés sensibles dans la mémoire volatile, réduisant ainsi le risque de compromission. De plus, le mécanisme est conçu pour fonctionner sans supervision, ce qui le rend adapté aux environnements déployés à grande échelle où les dispositifs ne disposent pas d’un système d’exploitation dédié.

## Voir aussi

* [[Secure coding]]
* [[ISO-18000-6C protocol]]
* [[Texas Instruments firmware update framework]]
* [[Physical Unclonable Function (PUF)]]
* [[Computational RFID (CRFID)]]
* [[Energy harvesting devices]]