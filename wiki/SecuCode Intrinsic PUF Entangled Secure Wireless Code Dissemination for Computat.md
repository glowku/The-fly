# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés exclusivement par l’énergie électromagnétique, sont dépourvus de batterie et d’un système d’exploitation supervisé, ce qui rend la distribution de firmware à distance particulièrement délicate. SecuCode résout ce problème en associant une fonction physique non clonable (PUF) intégrée à la mémoire SRAM aux protocoles de mise à jour existants, notamment ISO‑18000‑6C.

## Contexte et problématique
Les CRFID représentent une nouvelle catégorie d’appareils IoT « edge » grâce à leur simplicité de déploiement et à leur fonctionnement perpétuel grâce à l’auto‑alimentation. Cependant, leur nature intermittente, leurs ressources computationnelles limitées et l’absence d’un OS de supervision compliquent la sécurisation des mises à jour logicielles. Les solutions traditionnelles, qui reposent sur des clés pré‑partagées ou des mécanismes de chiffrement lourds, ne sont pas adaptées à ces contraintes.

## Principe et architecture de SecuCode
SecuCode introduit une entanglement entre la PUF SRAM intrinsèque du dispositif et le protocole de mise à jour. La PUF génère un identifiant unique à chaque démarrage, qui sert à authentifier le firmware reçu. Le mécanisme s’appuie sur un cadre de mise à jour fourni par Texas Instruments, étendu pour intégrer la vérification PUF. Ainsi, la mise à jour est effectuée uniquement si le firmware est signé et correspond à l’empreinte PUF du dispositif, garantissant l’intégrité et l’authenticité sans nécessiter de stockage supplémentaire ou de puissance supplémentaire.

## Évaluation et conformité
Une implémentation complète de SecuCode a été réalisée et testée sur des plateformes CRFID réelles. Les expérimentations montrent que le protocole respecte les normes ISO‑18000‑6C, que la latence introduite par la vérification PUF reste négligeable par rapport aux délais de communication radio, et que la sécurité est renforcée contre les attaques par réutilisation de firmware ou par falsification de mise à jour. Les performances sont compatibles avec les contraintes énergétiques, car la PUF est activée uniquement lors de la réception d’un paquet de mise à jour, minimisant ainsi la consommation.

## Voir aussi
[[Diagrammatic reasoning]], [[Graph theory]], [[Diagrams.net]], [[Automated reasoning]], [[EVOR Evolving Retrieval for Code Generation]]