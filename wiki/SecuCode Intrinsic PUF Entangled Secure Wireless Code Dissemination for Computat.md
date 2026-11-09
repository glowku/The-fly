# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, dépourvus de batterie, tirent toute leur énergie de l’environnement grâce à l’harvesting d’énergie. La mise à jour de leur firmware reste cependant problématique en raison de l’alimentation intermittente, des ressources limitées et de l’absence de système d’exploitation supervisé.

## Contexte et défis des CRFID

Les CRFID représentent une nouvelle catégorie d’appareils IoT de bord, combinant sensibilité, calcul et communication sans fil. Leur fonctionnement dépend d’une alimentation intermittente, ce qui rend les protocoles classiques de mise à jour inefficaces. De plus, leur faible puissance de calcul empêche l’utilisation de mécanismes cryptographiques lourds, et l’absence d’un OS superviseur complique la gestion de la sécurité.

## Architecture et mécanismes de SecuCode

SecuCode intègre de façon intrinsèque une fonction physique non clonable (PUF) basée sur la mémoire SRAM du dispositif. Cette PUF sert de clé unique à chaque appareil, permettant d’authentifier les mises à jour sans nécessiter de stockage supplémentaire. Le protocole de mise à jour est étendu à partir d’un cadre récent de Texas Instruments, garantissant la compatibilité avec les compilateurs et méthodes d’update standards de l’industrie. De plus, SecuCode reste entièrement compatible avec le protocole ISO‑18000‑6C, largement utilisé par les CRFID pour la communication sans fil.

## Évaluation, conformité et performances

Une implémentation complète de SecuCode a été réalisée et testée sur des dispositifs CRFID réels. Les expériences démontrent la conformité aux normes ISO, la robustesse du mécanisme d’authentification PUF et la capacité à fonctionner de façon continue malgré l’alimentation intermittente. Les performances mesurées montrent que la surcharge introduite par la PUF reste négligeable par rapport aux contraintes de puissance des CRFID, tout en assurant un niveau de sécurité suffisant pour prévenir les attaques de mise à jour malveillantes.

## Voir aussi

* [[Palaeoptera]]
* [[Tachinidae]]
* [[Angular resolution (graph drawing)]]
* [[Area (graph drawing)]]
* [[Technical drawing]]
* [[Data and information visualization]]