# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés uniquement par l’énergie captée via leurs antennes, doivent fonctionner sans batterie ni système d’exploitation supervisé, ce qui rend les procédures de mise à jour traditionnelles inefficaces. En liant la fonction physique unique de la mémoire SRAM (SRAM PUF) à un protocole de mise à jour, SecuCode assure l’authenticité et l’intégrité du firmware tout en respectant les contraintes de puissance et de calcul propres aux CRFID.

## Contexte et défis
Les CRFID représentent une nouvelle catégorie d’objets connectés, capables de collecter, traiter et transmettre des données sans source d’énergie externe. Leur intermittence de puissance, leur faible capacité de calcul et l’absence de système d’exploitation supervisé compliquent la sécurisation des mises à jour logicielles. De plus, ils utilisent des protocoles de communication standardisés, notamment ISO‑18000‑6C, ce qui impose une compatibilité stricte avec les équipements existants.

## Architecture et mécanismes
SecuCode introduit une entanglement entre la SRAM PUF et le protocole de mise à jour. La PUF, intrinsèque à chaque puce, génère un identifiant matériel unique et non clonable. Lors d’une mise à jour, le firmware est signé par le fabricant et enveloppé dans un paquet cryptographique qui inclut un challenge‑response basé sur la PUF. Le dispositif CRFID, lorsqu’il reçoit le paquet, utilise sa PUF pour répondre au challenge, prouvant ainsi son identité avant d’accepter et d’installer le firmware. Ce processus élimine la nécessité d’une clé pré‑installée ou d’un stockage de secrets, tout en restant compatible avec ISO‑18000‑6C.

## Implémentation et résultats
Une implémentation complète de SecuCode a été réalisée en étendant un cadre de mise à jour firmware fourni par Texas Instruments. Des expériences sur des plateformes CRFID réelles ont démontré la conformité aux normes, la fiabilité des mises à jour malgré l’alimentation intermittente, et une empreinte de performance acceptable pour les contraintes de ces dispositifs. Les mesures de sécurité montrent que l’attaque par clonage matériel est rendue pratiquement impossible grâce à la nature non clonable de la SRAM PUF.

## Voir aussi
[[Insect Festival]]  
[[Bonefish fly patterns]]  
[[Insects in ethics]]  
[[Behavioral ecology (disambiguation)]]