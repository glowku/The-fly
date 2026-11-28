# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés uniquement par l’énergie captée dans l’environnement, doivent rester opérationnels malgré des alimentations intermittentes et des ressources de calcul limitées. SecuCode résout ce défi en associant une fonction physique non clonable (PUF) intégrée à la mémoire SRAM du dispositif à un protocole de mise à jour firmware, tout en restant compatible avec les normes industrielles existantes.

## Contexte et motivation

Les CRFID représentent une nouvelle catégorie d’appareils IoT sans batterie, capables de capter, de traiter et de transmettre des données grâce à l’énergie électromagnétique ambiante. Leur architecture dépourvue de système d’exploitation supervisé rend la distribution sécurisée de mises à jour logicielles particulièrement complexe. Les contraintes d’alimentation intermittente et de puissance de calcul réduite empêchent l’utilisation de méthodes de mise à jour classiques, qui exigent souvent une authentification robuste et une vérification de l’intégrité du firmware.

## Architecture et mécanismes

SecuCode intègre la PUF SRAM, un primitive de sécurité matérielle intrinsèque, dans le flux de mise à jour. La PUF génère un identifiant unique à chaque appareil, sans nécessiter de stockage externe, ce qui permet d’authentifier le dispositif lors de la réception du firmware. Le protocole de mise à jour est étendu à partir d’un cadre récent de Texas Instruments, garantissant la conformité aux méthodes de compilation et de mise à jour standard de l’industrie. De plus, SecuCode fonctionne sur le protocole ISO‑18000‑6C, le standard de communication couramment utilisé par les CRFID, assurant ainsi une intégration transparente avec les équipements existants.

## Évaluation et résultats

Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai dédié. Les expérimentations ont démontré la conformité aux normes ISO‑18000‑6C, la robustesse de l’authentification basée sur la PUF SRAM, ainsi que des performances acceptables malgré les contraintes énergétiques. Les résultats indiquent que SecuCode permet des mises à jour sécurisées sans compromettre la disponibilité ou la durée de vie de l’appareil.

## Voir aussi

[[Secure coding]], [[Visual Studio]], [[Compass (drawing tool)]], [[Contour drawing]]