# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé spécialement conçu pour les dispositifs RFID computationnels (CRFID). Il exploite la fonction physique non clonable (PUF) intégrée à la mémoire SRAM du dispositif afin de garantir l’authenticité et l’intégrité du firmware. Cette approche permet de surmonter les contraintes de puissance intermittente et de ressources limitées propres aux CRFID, tout en restant compatible avec les protocoles de communication existants, notamment ISO‑18000‑6C.

## Contexte et motivation
Les dispositifs CRFID tirent leur énergie de l’environnement, ce qui les rend autonomes mais aussi vulnérables aux attaques de mise à jour logicielle. L’absence d’un système d’exploitation supervisé et la puissance limitée rendent les méthodes classiques de mise à jour peu adaptées. SecuCode propose une solution qui s’appuie sur un élément matériel intrinsèque, la SRAM PUF, pour créer un lien unique et non reproductible entre le dispositif et le firmware qu’il reçoit.

## Architecture et principe de fonctionnement
Le protocole SecuCode intègre la PUF SRAM dans la chaîne de mise à jour. Lors de la réception d’un paquet de firmware, le dispositif génère un challenge‑response à partir de sa PUF, qui est vérifié par le serveur d’authentification. Seuls les firmwares signés avec la clé dérivée de la PUF sont acceptés. Le mécanisme est entièrement compatible avec le cadre de mise à jour fourni par Texas Instruments, étendu pour fonctionner sans supervision et avec des cycles d’alimentation intermittents. La communication se fait via ISO‑18000‑6C, assurant ainsi une intégration transparente dans les infrastructures RFID existantes.

## Évaluation et conformité
Une implémentation complète a été réalisée et testée sur des plateformes CRFID réelles. Les expérimentations ont confirmé la conformité aux normes ISO‑18000‑6C, la robustesse contre les attaques par rejeu et la résilience face aux coupures d’alimentation fréquentes. Les performances montrent un temps de mise à jour acceptable pour les applications IoT, tout en conservant un faible coût énergétique grâce à l’utilisation de la PUF comme mécanisme d’authentification sans calcul supplémentaire.

## Voir aussi
[[Supply chain security]] [[Code]] [[Arxivers sense Fronteres]] [[Web]] [[Technical drawing tool]] [[Compass (drawing tool)]]