# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID à calcul (CRFID). Il associe une fonction physique unique (PUF) intégrée à la mémoire SRAM du dispositif à un protocole de mise à jour firmware, afin de surmonter les contraintes d’alimentation intermittente, de ressources limitées et l’absence de système d’exploitation supervisé. La solution est entièrement compatible avec les protocoles de communication existants, notamment ISO‑18000‑6C, et s’appuie sur un cadre de mise à jour firmware standardisé fourni par Texas Instruments.

## Contexte et défis
Les dispositifs CRFID tirent leur énergie de l’environnement radio, ce qui les rend dépourvus de batterie et sujets à des interruptions d’alimentation fréquentes. Leur faible puissance de calcul et l’absence de système d’exploitation robuste compliquent la mise en œuvre de mécanismes de sécurité traditionnels. De plus, la mise à jour sans fil du firmware doit garantir l’authenticité, l’intégrité et la confidentialité du code tout en restant viable sur des ressources très limitées.

## Architecture et mécanismes de SecuCode
SecuCode intègre une PUF SRAM intrinsèque au dispositif, générant un identifiant matériel unique à chaque fois que le dispositif est alimenté. Ce PUF est utilisé pour dériver des clés cryptographiques temporaires qui chiffrent et authentifient les paquets de mise à jour. Le protocole de mise à jour repose sur l’extension d’un cadre existant de Texas Instruments, permettant une compilation et une distribution de firmware conformes aux normes industrielles. Le processus se déroule en plusieurs étapes : (1) génération d’un challenge PUF, (2) réponse PUF calculée par le dispositif, (3) établissement d’une session sécurisée, et (4) transmission et vérification du firmware. Cette approche élimine le besoin d’un stockage persistant de clés ou d’un module de sécurité dédié, tout en assurant une résistance aux attaques par copie ou par falsification.

## Évaluation et conformité
Une mise en œuvre complète de SecuCode a été réalisée et testée sur des plateformes CRFID réelles. Les expérimentations ont confirmé la conformité aux spécifications ISO‑18000‑6C, démontré une faible consommation énergétique supplémentaire et évalué la robustesse contre des attaques classiques (replay, injection de firmware malveillant). Les performances de mise à jour, mesurées en temps de transmission et en consommation d’énergie, restent dans les limites acceptables pour les applications IoT industrielles.

## Voir aussi
[[Web]], [[Code]], [[Secure coding]], [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]]