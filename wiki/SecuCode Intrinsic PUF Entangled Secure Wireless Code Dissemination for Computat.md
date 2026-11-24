# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID à puissance auto‑alimentée (CRFID). Il combine une fonction physique non clonable (PUF) basée sur la mémoire SRAM du dispositif avec un protocole d’actualisation de firmware, afin de garantir l’intégrité et l’authenticité du code distribué tout en respectant les contraintes de puissance intermittente et de ressources limitées propres aux CRFID.

## Fonctionnement et architecture

Le cœur de SecuCode repose sur l’entrelacement d’une PUF SRAM intrinsèque avec le processus de mise à jour. Lorsqu’un dispositif CRFID reçoit une mise à jour, la PUF génère un identifiant unique à partir de l’état aléatoire de la SRAM, qui est ensuite utilisé pour chiffrer et signer le firmware. Cette approche élimine le besoin d’un système d’exploitation supervisé, car la PUF fournit une source d’authentification matérielle fiable même en l’absence de courant continu. Le protocole est entièrement compatible avec ISO‑18000‑6C, le standard de communication couramment employé par les CRFID, et s’intègre dans le cadre d’actualisation de firmware fourni par Texas Instruments, un standard industriel largement adopté.

## Implémentation et résultats expérimentaux

Une implémentation complète de SecuCode a été réalisée et testée sur un échantillon de dispositifs CRFID. Les expériences ont montré que le mécanisme respecte les exigences de conformité aux standards, tout en maintenant un temps de mise à jour raisonnable malgré l’alimentation intermittente. Les mesures de performance indiquent que l’empreinte mémoire supplémentaire est négligeable, et que la latence introduite par la génération de la PUF et le chiffrement reste bien en dessous des limites acceptables pour les applications IoT. Sur le plan de la sécurité, SecuCode offre une protection robuste contre les attaques de falsification de firmware et les tentatives d’injection de code malveillant, grâce à l’unicité et à l’imprévisibilité de la PUF.

## Voir aussi

* [[Secure coding]]
* [[ISO-18000-6C protocol]]
* [[Texas Instruments]]
* [[Physical Unclonable Function]]
* [[Computational RFID]]
* [[Energy harvesting]]