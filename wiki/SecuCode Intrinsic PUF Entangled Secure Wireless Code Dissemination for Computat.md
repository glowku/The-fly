# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID à calcul (CRFID). Ces appareils, alimentés uniquement par l’énergie électromagnétique, sont dépourvus de batterie et d’un système d’exploitation supervisé, ce qui rend les mises à jour logicielles particulièrement délicates. En associant une fonction physique non clonable (PUF) intégrée à la mémoire SRAM à un protocole de mise à jour, SecuCode surmonte les contraintes de puissance intermittente et de capacité de calcul limitée.

## Contexte et défis des dispositifs CRFID
Les CRFID représentent une nouvelle classe d’objets connectés à faible consommation, capables de collecter, traiter et transmettre des données sans source d’énergie externe. Leur architecture sans batterie les expose à des interruptions fréquentes de l’alimentation, rendant les opérations de mise à jour fragiles. De plus, l’absence d’un système d’exploitation robuste empêche l’utilisation de mécanismes de sécurité classiques, tandis que les ressources matérielles restreintes limitent les options de chiffrement et d’authentification.

## Architecture et mécanismes de SecuCode
SecuCode intègre la PUF SRAM, un primitive de sécurité matérielle intrinsèque, dans le flux de mise à jour du firmware. La PUF génère un identifiant unique et difficilement reproductible à partir de la mémoire volatile, qui sert à authentifier le dispositif et à chiffrer les paquets de mise à jour. Le protocole est entièrement compatible avec le standard ISO‑18000‑6C, utilisé couramment par les CRFID, et s’appuie sur une extension du cadre de mise à jour de firmware fourni par Texas Instruments. Cette approche permet une mise à jour sécurisée sans nécessiter de ressources supplémentaires ou de modification du firmware existant.

## Évaluation et résultats expérimentaux
Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai comprenant plusieurs dispositifs CRFID. Les expérimentations ont démontré la conformité aux normes ISO, une latence de mise à jour acceptable pour les applications IoT, et une robustesse contre les attaques par rejeu et par falsification de firmware. Les mesures de consommation d’énergie indiquent que l’utilisation de la PUF n’ajoute pas de surcharge significative, préservant ainsi l’autonomie énergétique des dispositifs.

## Voir aussi
[[Application security]], [[Network theory]], [[Cross-origin resource sharing]], [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]], [[What Would a Graph Look Like in This Layout A Machine Learning Approach to Large]]