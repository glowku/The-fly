# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID à puissance auto-générée (CRFID). En associant une fonction physique unique (PUF) intégrée à la mémoire SRAM à un protocole de mise à jour, SecuCode permet aux appareils dépourvus de batterie et de système d’exploitation de recevoir des firmwares fiables malgré leur alimentation intermittente et leurs ressources limitées.

## Contexte et défis
Les dispositifs CRFID représentent une nouvelle catégorie d’objets connectés à l’Internet des objets, capables de fonctionner uniquement grâce à l’énergie captée dans leur environnement. Leur architecture sans batterie et sans OS entraîne des contraintes majeures : interruptions fréquentes d’alimentation, capacité de calcul réduite et absence de mécanismes de sécurité traditionnels. La mise à jour sans fil de firmware reste donc un problème non résolu, car les méthodes classiques requièrent une puissance stable et des ressources de traitement suffisantes.

## Architecture et mécanismes
SecuCode introduit une entanglement entre la PUF SRAM intrinsèque du dispositif et le protocole de mise à jour. La PUF, en tant que primitive de sécurité matérielle, fournit une identité unique et difficilement clonable pour chaque appareil. Le protocole, compatible avec le standard ISO‑18000‑6C, étend un cadre de mise à jour existant de Texas Instruments, garantissant ainsi l’interopérabilité avec les équipements industriels. Le processus de mise à jour se déroule en plusieurs étapes : génération d’un challenge‑response à partir de la PUF, signature cryptographique du firmware, et transmission sécurisée via le protocole ISO‑18000‑6C. Cette approche permet de vérifier l’authenticité du firmware et l’intégrité de la transmission tout en respectant les contraintes énergétiques des CRFID.

## Évaluation et conformité
Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai dédié. Les expérimentations démontrent la conformité aux normes ISO‑18000‑6C, la robustesse contre les attaques par rejeu et par falsification de firmware, ainsi que les performances acceptables en termes de temps de mise à jour et de consommation énergétique. Les résultats indiquent que SecuCode offre une solution viable pour la gestion sécurisée des dispositifs RFID sans batterie, ouvrant la voie à des déploiements massifs dans des environnements industriels et domestiques.

## Voir aussi
[[Query expansion]] [[Visual system]] [[Andy Diagram]] [[ArXiv]] [[Supply chain security]] [[Code]]