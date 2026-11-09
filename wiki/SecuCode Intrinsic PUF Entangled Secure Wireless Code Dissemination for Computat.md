# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID à puissance auto‑alimentée (CRFID). Il associe de façon intrinsèque une fonction physique non clonable (PUF) basée sur la mémoire SRAM aux protocoles de mise à jour firmware, afin de surmonter les contraintes d’alimentation intermittente, de capacité de calcul limitée et l’absence de système d’exploitation supervisé.

## Fonctionnement et architecture

Le cœur de SecuCode repose sur l’entrelacement d’une PUF SRAM avec le protocole de mise à jour. Lorsqu’un dispositif CRFID reçoit une nouvelle image firmware, la PUF génère un identifiant unique et difficilement reproductible, qui sert à authentifier la source et à chiffrer le flux de mise à jour. Cette approche élimine le besoin d’une clé pré‑installée ou d’un module cryptographique supplémentaire, tout en garantissant que chaque mise à jour est liée de façon irréversible au matériel spécifique du lecteur.

## Compatibilité et mise en œuvre

SecuCode a été conçu pour être entièrement compatible avec les protocoles de communication existants, notamment ISO‑18000‑6C, couramment utilisés par les lecteurs RFID. Il s’intègre également dans le cadre de mise à jour firmware standardisé de Texas Instruments, en étendant le framework récent proposé par l’entreprise. Cette intégration permet aux développeurs de compiler et de déployer des firmwares en suivant les pratiques industrielles, sans modifier l’architecture logicielle de base du dispositif.

## Évaluation et performances

Une implémentation complète de SecuCode a été réalisée et soumise à une batterie d’expériences. Les résultats démontrent la conformité aux normes ISO, la robustesse contre les attaques par rejeu et par falsification, ainsi que des temps de mise à jour raisonnables malgré les contraintes énergétiques. Les mesures de performance indiquent que la génération de la PUF et le chiffrement se font en quelques millisecondes, ce qui est compatible avec les cycles d’alimentation intermittents des CRFID.

## Voir aussi

* [[Physical Unclonable Function]]
* [[RFID]]
* [[ISO‑18000‑6C]]
* [[Firmware update]]
* [[Texas Instruments]]
* [[Energy harvesting]]