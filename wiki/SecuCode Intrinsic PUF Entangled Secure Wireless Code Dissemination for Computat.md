# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé spécialement conçu pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés uniquement par l’énergie captée dans leur environnement, offrent une simplicité de déploiement et une autonomie permanente, mais présentent des contraintes majeures en matière de sécurité des mises à jour. SecuCode résout ces problèmes en intégrant une fonction physique non clonable (PUF) basée sur la mémoire SRAM dans le protocole de mise à jour.

## Contexte et défis

Les CRFID sont des dispositifs sans batterie, capables de réaliser des calculs et de mesurer des capteurs, tout en se rechargant par l’intermédiaire de l’énergie électromagnétique. Leur alimentation intermittente, leurs ressources de calcul limitées et l’absence d’un système d’exploitation supervisé rendent difficile la mise à jour sécurisée de leur firmware. De plus, la plupart des protocoles de communication existants, notamment ISO‑18000‑6C, ne prennent pas en charge les mécanismes de sécurité avancés requis pour protéger l’intégrité et l’authenticité du code.

## Architecture de SecuCode

SecuCode entangle la PUF SRAM intrinsèque du dispositif avec le protocole de mise à jour. La PUF fournit une identité unique et difficile à cloner, ce qui permet d’authentifier le dispositif sans stocker de secrets persistants. Le protocole de mise à jour, étendu à partir d’un cadre récent de Texas Instruments, utilise cette identité pour chiffrer et signer le firmware, garantissant que seul le dispositif légitime peut le déchiffrer et l’exécuter. Cette approche est entièrement compatible avec ISO‑18000‑6C, ce qui facilite l’intégration dans les systèmes existants.

## Implémentation et résultats

Une implémentation complète de SecuCode a été réalisée, incluant le firmware, le protocole de mise à jour et les tests de conformité aux normes. Des expériences approfondies ont démontré que le système respecte les exigences de l’ISO‑18000‑6C, tout en offrant des performances acceptables malgré les contraintes de puissance et de calcul. Les mesures de sécurité montrent que la combinaison de la PUF et du protocole de mise à jour résiste aux attaques par clonage et aux tentatives d’injection de firmware malveillant.

## Voir aussi

[[ArXiv]], [[Supply chain security]], [[ISO-18000-6C protocol]], [[Texas Instruments firmware update framework]], [[SRAM PUF]], [[Wireless firmware updates]]