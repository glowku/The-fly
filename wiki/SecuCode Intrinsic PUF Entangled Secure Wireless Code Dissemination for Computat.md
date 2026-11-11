# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé spécialement conçu pour les dispositifs RFID computationnels (CRFID). Il exploite une fonction physique unique (PUF) intégrée dans la mémoire SRAM afin de lier la signature du firmware à l'identité matérielle du dispositif. Cette approche permet de surmonter les contraintes d’alimentation intermittente, de puissance de calcul limitée et l’absence d’un système d’exploitation supervisé, tout en restant compatible avec les protocoles de communication existants, notamment ISO‑18000‑6C.

## Contexte et défis des dispositifs CRFID
Les CRFID sont des capteurs sans batterie qui tirent toute leur énergie de la radiofréquence. Leur fonctionnement intermittent et leurs ressources restreintes rendent les mises à jour logicielles traditionnelles inefficaces. De plus, l’absence d’un système d’exploitation dédié complique la mise en œuvre de mécanismes de sécurité classiques, tels que les signatures numériques ou les certificats. Il est donc crucial de développer une solution qui s’intègre naturellement dans l’architecture matérielle et logicielle de ces dispositifs.

## Architecture et mécanismes de SecuCode
SecuCode entangle la PUF SRAM du dispositif avec le protocole de mise à jour du firmware. Lorsqu’une nouvelle image est transmise, le dispositif génère un challenge‑response à partir de sa PUF, qui est utilisé pour authentifier la source et garantir l’intégrité du code. Le mécanisme est entièrement compatible avec le protocole ISO‑18000‑6C et s’appuie sur une extension du cadre de mise à jour de firmware fourni par Texas Instruments. L’implémentation complète intègre la compilation standard, la signature et la vérification, tout en respectant les contraintes énergétiques et temporelles des CRFID.

## Évaluation expérimentale et résultats
Une série d’expériences a été menée pour valider la conformité aux normes, mesurer les performances et évaluer la robustesse contre les attaques. Les résultats montrent que SecuCode maintient un cycle de mise à jour raisonnable même avec des alimentations intermittentes, tout en offrant une protection cryptographique solide grâce à la PUF. Les tests de conformité ISO‑18000‑6C ont confirmé l’interopérabilité avec les lecteurs RFID existants, et les mesures de sécurité ont démontré la résistance aux tentatives de falsification de firmware.

## Voir aussi
[[Automated reasoning]]  
[[Diagrams.net]]  
[[Image]]  
[[Graph theory]]  
[[Searching Scientific Literature for Answers on COVID-19 Questions]]