# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, spécialement conçu pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés uniquement par l’énergie captée dans leur environnement, doivent rester opérationnels malgré des interruptions fréquentes d’alimentation et des ressources de calcul limitées. Le présent article expose le principe, l’architecture et les résultats expérimentaux de SecuCode, qui intègre une fonction physique non clonable (PUF) basée sur la SRAM dans le protocole de mise à jour.

## Contexte et défis de la mise à jour logicielle sur CRFID
Les CRFID représentent une nouvelle catégorie d’objets connectés sans batterie, capables de traiter, de mesurer et de communiquer via la radio. Leur dépendance à l’énergie captée rend la mise à jour logicielle particulièrement délicate : les cycles d’alimentation sont intermittents, les processeurs sont peu puissants et l’absence d’un système d’exploitation supervisé empêche l’utilisation de mécanismes classiques de sécurité. De plus, les protocoles de communication existants, notamment ISO‑18000‑6C, ne prévoient pas de garanties d’authenticité ou d’intégrité pour le firmware.

## Architecture et fonctionnement de SecuCode
SecuCode relie la PUF SRAM intrinsèque d’un CRFID à un protocole de mise à jour. La PUF, qui génère un identifiant unique à partir de l’état aléatoire de la mémoire SRAM, sert à authentifier le dispositif et à chiffrer le code à mettre à jour. Le mécanisme repose sur une extension du cadre de mise à jour fourni par Texas Instruments, garantissant la compatibilité avec les compilateurs et les outils de mise à jour standards. En outre, SecuCode reste conforme aux exigences du protocole ISO‑18000‑6C, ce qui permet son déploiement sur les infrastructures RFID existantes sans modification matérielle.

## Évaluation, conformité et perspectives
Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai dédié. Les expériences démontrent la conformité aux normes ISO‑18000‑6C, la viabilité des opérations de mise à jour même avec des interruptions d’alimentation fréquentes, ainsi qu’une résistance aux attaques classiques (replay, falsification). Les performances mesurées indiquent un temps d’authentification et de chiffrement de l’ordre de quelques millisecondes, bien adapté aux contraintes de calcul des CRFID. Ces résultats ouvrent la voie à des déploiements sécurisés de firmware sur des réseaux d’objets connectés à faible puissance.

## Voir aussi
[[ArXiv]], [[Supply chain security]], [[Code]], [[Web]], [[Query language]]