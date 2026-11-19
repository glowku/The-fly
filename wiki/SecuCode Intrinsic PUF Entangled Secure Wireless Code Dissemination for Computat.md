# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé spécialement conçu pour les dispositifs RFID computationnels (CRFID). Ces appareils, dépourvus de batterie, tirent leur énergie de l’environnement et disposent de capacités de calcul limitées. Le système intègre une fonction physique non clonable (PUF) basée sur la mémoire SRAM pour sécuriser la diffusion de firmware, tout en restant compatible avec les protocoles existants, notamment ISO‑18000‑6C.

## Contexte et problématique

Les CRFID représentent une nouvelle génération d’appareils IoT à faible coût et à faible consommation, capables de fonctionner grâce à l’harvesting énergétique. Cependant, leur mise à jour logicielle reste problématique : l’alimentation intermittente, les ressources de calcul restreintes et l’absence d’un système d’exploitation supervisé rendent difficile l’authentification et la vérification d’intégrité des firmwares. SecuCode répond à ces contraintes en s’appuyant sur la PUF SRAM, un atout matériel intrinsèque qui fournit une identité unique et difficilement clonable.

## Architecture de SecuCode

Le protocole de mise à jour combine la PUF SRAM avec un processus d’authentification basé sur des signatures numériques. Lorsqu’un firmware est proposé, le dispositif génère un challenge‑response à partir de sa PUF, que le serveur vérifie avant d’envoyer le code. La mise à jour est effectuée via le cadre d’actualisation fourni par Texas Instruments, étendu pour inclure la vérification PUF. Cette approche garantit que seul un dispositif authentique peut recevoir et exécuter le firmware, même en l’absence de supervision logicielle.

## Implémentation et résultats expérimentaux

Une implémentation complète de SecuCode a été réalisée et testée sur des plateformes CRFID réelles. Les expériences démontrent la conformité aux normes ISO‑18000‑6C, une faible latence de mise à jour (moins de 2 s pour un firmware de 256 kB) et une robustesse contre les attaques de re‑envoi ou de falsification. Les performances restent acceptables malgré l’alimentation intermittente, grâce à la gestion intelligente de l’énergie et à la réduction des cycles de calcul requis pour la PUF.

## Voir aussi

* [[ArXiv]]
* [[Code]]
* [[Supply chain security]]
* [[Web]]
* [[Visual system]]