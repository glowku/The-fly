# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés uniquement par l’énergie captée dans l’environnement, doivent rester opérationnels malgré des alimentations intermittentes et des ressources de calcul limitées. Le système intègre une fonction physique non clonable (PUF) basée sur la mémoire SRAM pour sécuriser la distribution de firmware, tout en restant compatible avec les protocoles existants, notamment ISO‑18000‑6C.

## Contexte et défis
Les CRFID représentent une nouvelle génération d’objets connectés sans batterie, capables de réaliser des calculs et de collecter des données sensorielles. Leur dépendance à l’énergie captée rend la mise à jour logicielle particulièrement délicate : l’alimentation peut être interrompue à tout moment, et les dispositifs ne disposent pas d’un système d’exploitation supervisé. De plus, les contraintes de puissance et de capacité de calcul limitent les approches de sécurité classiques. Il est donc essentiel de développer une méthode qui fonctionne dans ces conditions extrêmes tout en garantissant l’intégrité et l’authenticité du firmware.

## Architecture et mécanismes
SecuCode relie la PUF SRAM intrinsèque du dispositif à un protocole de mise à jour. La PUF génère un identifiant unique et non reproductible à chaque démarrage, ce qui permet de lier de façon univoque chaque firmware à l’appareil concerné. Le protocole de mise à jour, basé sur le cadre de Texas Instruments, est étendu pour inclure la vérification de la signature cryptographique du firmware et l’authentification de la source via la PUF. Cette approche élimine le besoin d’un stockage permanent de clés et assure que même en cas de coupure d’alimentation, le processus peut reprendre sans compromettre la sécurité.

## Évaluation et conformité
Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai. Les résultats démontrent la conformité aux normes ISO‑18000‑6C, la compatibilité avec les compilateurs et outils de mise à jour existants, ainsi qu’une faible surcharge en termes de consommation énergétique et de temps de mise à jour. Les mesures de sécurité montrent que les tentatives d’usurpation d’appareil ou de modification non autorisée du firmware sont efficacement détectées grâce à la combinaison de la PUF et des signatures cryptographiques.

## Voir aussi
[[Web]] [[Code]] [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]] [[Secure coding]] [[Autonomous agent]] [[Technical drawing tool]]