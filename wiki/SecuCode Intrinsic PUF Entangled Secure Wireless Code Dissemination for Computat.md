# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé spécialement conçu pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés exclusivement par l’énergie captée sur le champ électromagnétique, sont dépourvus de batterie et de système d’exploitation supervisé, ce qui rend la distribution de firmware difficile. En associant une fonction physique non clonable (PUF) basée sur la mémoire SRAM aux protocoles de mise à jour, SecuCode offre une solution robuste aux contraintes d’alimentation intermittente et de ressources limitées.

## Contexte et motivation

Les CRFID représentent une nouvelle catégorie d’objets connectés à l’Internet des objets, grâce à leur simplicité de déploiement et à leur fonctionnement continu grâce à l’auto‑alimentation. Cependant, la mise à jour sécurisée de leur firmware reste un problème majeur, notamment en raison de l’absence de supervision logicielle et de la fragilité des connexions sans fil. SecuCode répond à ces défis en s’appuyant sur le standard ISO‑18000‑6C, largement utilisé dans l’industrie RFID, et en intégrant un protocole de mise à jour fourni par Texas Instruments, étendu pour inclure la PUF.

## Architecture et fonctionnement

Le cœur de SecuCode est l’entrelacement d’une PUF SRAM intrinsèque à la procédure de mise à jour. À chaque tentative de téléchargement de firmware, le dispositif génère un identifiant unique à partir de la PUF, qui est ensuite utilisé pour chiffrer et authentifier le code. Cette approche garantit que seul le dispositif cible peut déchiffrer et exécuter le firmware, même en présence d’interférences ou d’attaques de type « man‑in‑the‑middle ». Les tests effectués montrent une conformité complète aux normes industrielles, ainsi qu’une performance acceptable malgré les contraintes énergétiques.

## Évaluation expérimentale

Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai composé de plusieurs tags CRFID. Les résultats démontrent la viabilité de la méthode : le temps de mise à jour reste dans la plage acceptable pour les applications IoT, et la sécurité est renforcée grâce à la non‑clonabilité de la PUF. De plus, la solution s’intègre sans modification aux outils de compilation et de mise à jour existants, facilitant son adoption par les fabricants.

## Voir aussi

[[ArXiv]] [[Supply chain security]] [[Code]] [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]] [[Technical drawing tool]] [[Compass (drawing tool)]].