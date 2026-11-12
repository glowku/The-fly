# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Il exploite la fonction physique unique d’un SRAM PUF (Physical Unclonable Function) afin de l’entrelacer avec un protocole de mise à jour firmware, répondant ainsi aux contraintes d’alimentation intermittente, de ressources limitées et à l’absence de système d’exploitation supervisé.

## Contexte et défis
Les CRFID sont des appareils sans batterie qui récupèrent toute leur énergie en provenance du champ radio. Cette architecture simplifie le déploiement et assure une opération continue, mais elle rend la mise à jour sécurisée du firmware particulièrement délicate. Les contraintes d’alimentation intermittente, la puissance de calcul réduite et l’absence de supervision OS rendent les méthodes classiques de distribution de code inadaptées. De plus, les dispositifs communiquent via le protocole ISO‑18000‑6C, ce qui impose une compatibilité stricte avec les normes industrielles existantes.

## Architecture et mécanismes de SecuCode
SecuCode intègre la PUF SRAM du dispositif comme clé d’authentification intrinsèque. Lors d’une mise à jour, le serveur génère un défi qui est traité par la PUF pour produire une réponse unique au dispositif. Cette réponse sert à chiffrer et signer le firmware, garantissant que seul le matériel cible peut le déchiffrer et l’exécuter. Le protocole repose sur une extension du cadre de mise à jour firmware fourni par Texas Instruments, assurant ainsi une compatibilité complète avec les compilateurs et les outils de mise à jour standard. La communication reste conforme au protocole ISO‑18000‑6C, ce qui permet une intégration transparente dans les systèmes existants.

## Évaluation et conformité
Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai dédié. Les expérimentations démontrent la conformité aux normes ISO‑18000‑6C, évaluent les performances en termes de latence et de consommation d’énergie, et attestent de la robustesse du mécanisme contre les attaques par rejeu et par falsification. Les résultats indiquent que SecuCode peut être déployé sans modification majeure du firmware existant, tout en offrant une couche de sécurité supplémentaire indispensable aux applications IoT critiques.

## Voir aussi
[[ArXiv]], [[Diagrams.net]], [[Multi-Turn Agentic Scientific Literature Search via Workflow Induction]], [[Graph theory]], [[Image]]