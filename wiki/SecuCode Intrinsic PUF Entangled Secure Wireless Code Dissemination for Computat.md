# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Il combine une fonction physique non clonable (PUF) basée sur la mémoire SRAM du dispositif avec un protocole de mise à jour firmware. Cette approche vise à surmonter les contraintes d’alimentation intermittente, de puissance de calcul limitée et l’absence de système d’exploitation supervisé propres aux CRFID. Le système est entièrement compatible avec le protocole ISO‑18000‑6C et s’appuie sur un cadre d’actualisation firmware fourni par Texas Instruments.

## Contexte et défis
Les dispositifs CRFID représentent une nouvelle catégorie d’objets connectés sans batterie, reposant sur l’énergie captée par leurs antennes. Leur connectivité sans fil et leur autonomie énergétique les rendent attractifs pour l’Internet des objets, mais la mise à jour sécurisée de leur firmware reste problématique. Les interruptions d’alimentation fréquentes et les ressources restreintes rendent inefficaces les solutions de mise à jour classiques, qui supposent une disponibilité continue de l’appareil et un système d’exploitation capable de gérer les transactions cryptographiques.

## Principe de fonctionnement
SecuCode entangle la PUF SRAM intrinsèque du dispositif avec le protocole de mise à jour. À chaque tentative de mise à jour, le firmware est signé par un serveur central et le dispositif génère un challenge‑response à partir de sa PUF. La réponse unique, impossible à reproduire sur un autre appareil, sert à authentifier le firmware avant son installation. Ainsi, même si un attaquant intercepte les paquets, il ne peut pas falsifier la signature sans connaître la réponse PUF propre à l’appareil.

## Implémentation et résultats
Une implémentation complète de SecuCode a été réalisée, intégrant le protocole ISO‑18000‑6C et étendant le cadre de mise à jour firmware de Texas Instruments. Des expériences approfondies ont confirmé la conformité aux normes industrielles, évalué les performances en termes de latence et de consommation d’énergie, et démontré la robustesse du système face à des attaques classiques. Les résultats indiquent que SecuCode offre une solution viable pour la maintenance sécurisée des CRFID dans des environnements à ressources limitées.

## Voir aussi
[[Application security]], [[ISO-18000-6C]], [[Physical Unclonable Function (PUF)]], [[Computational RFID]], [[Firmware update]], [[Energy harvesting devices]]