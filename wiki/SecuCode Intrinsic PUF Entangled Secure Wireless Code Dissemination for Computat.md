# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID à calcul (CRFID). Il combine une fonction physique non clonable (PUF) intégrée à la mémoire SRAM d’un dispositif avec un protocole de mise à jour firmware, afin de surmonter les contraintes d’alimentation intermittente, de capacité de calcul limitée et l’absence de système d’exploitation supervisé. Le système est compatible avec le protocole ISO‑18000‑6C et s’appuie sur un cadre d’actualisation firmware fourni par Texas Instruments.

## Contexte et enjeux

Les dispositifs CRFID représentent une nouvelle catégorie d’appareils IoT sans batterie, qui récupèrent toute leur énergie via l’harvesting radiofréquence. Cette approche offre une simplicité de déploiement et une exploitation continue, mais introduit des défis majeurs en matière de sécurité, notamment la mise à jour logicielle sans fil. Les interruptions d’alimentation, la faible puissance de calcul et l’absence d’un OS de supervision rendent les méthodes classiques de mise à jour vulnérables aux attaques de reprogrammation ou de falsification de firmware.

## Principe de fonctionnement

SecuCode intègre la PUF SRAM, un primitive de sécurité matérielle intrinsèque, dans le processus de mise à jour. La PUF génère un identifiant unique et difficilement clonable à partir de la mémoire volatile du dispositif. Ce défi est utilisé pour authentifier la source du firmware et garantir son intégrité avant l’installation. Le protocole de mise à jour, étendu à partir du cadre TI, utilise des signatures cryptographiques et un mécanisme de vérification basé sur la PUF, assurant que seule une mise à jour signée et authentifiée peut être acceptée, même en présence d’alimentation intermittente.

## Implémentation et résultats

Une implémentation complète de SecuCode a été réalisée et testée sur des dispositifs CRFID réels. Les expérimentations ont confirmé la conformité aux normes ISO‑18000‑6C, démontré la compatibilité avec les compilateurs et les outils de mise à jour existants, et évalué les performances en termes de temps de mise à jour et de consommation d’énergie. Les résultats montrent que SecuCode fournit un niveau de sécurité robuste tout en restant viable pour les ressources limitées des CRFID, ouvrant la voie à des déploiements sûrs d’appareils IoT sans batterie.

## Voir aussi

[[Visual system]] [[Supply chain security]] [[Query language]] [[Network theory of aging]] [[Arxivers sense Fronteres]]