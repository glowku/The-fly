# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID à puissance autonome (CRFID). Il exploite la fonction physique non clonable (PUF) intégrée dans la mémoire SRAM des appareils afin de lier la sécurité du firmware à une caractéristique matérielle unique. Cette approche permet de surmonter les contraintes de puissance intermittente, de capacité de calcul limitée et l’absence de système d’exploitation supervisé qui rendent les mises à jour sans fil difficiles pour les CRFID.

## Conception et principe de fonctionnement

Le cœur de SecuCode repose sur l’entrelacement d’une PUF SRAM avec un protocole de mise à jour firmware. À chaque cycle d’alimentation, le dispositif génère un identifiant matériel à partir de la PUF, qui sert à authentifier l’origine du firmware et à établir une clé cryptographique temporaire. Le protocole est entièrement compatible avec le standard ISO‑18000‑6C, le protocole de communication le plus répandu pour les dispositifs RFID. En outre, SecuCode s’appuie sur un cadre d’actualisation de firmware fourni par Texas Instruments, étendu pour intégrer la génération de clés et la vérification d’intégrité du code.

## Implémentation et évaluation

Une implémentation complète de SecuCode a été réalisée et testée sur des plateformes CRFID réelles. Les expérimentations ont démontré la conformité aux normes ISO‑18000‑6C, la viabilité de l’opération continue grâce à l’énergie captée et la robustesse du mécanisme face aux tentatives d’usurpation. Les performances mesurées indiquent que la génération de la PUF et la négociation de la clé se font en quelques millisecondes, ce qui est compatible avec les contraintes de temps de vie de l’alimentation.

## Sécurité et perspectives

La sécurité de SecuCode repose sur la non-clonabilité de la PUF SRAM et sur l’utilisation de protocoles cryptographiques éprouvés. Le système garantit l’authenticité, l’intégrité et la confidentialité du firmware, tout en restant léger pour les dispositifs sans batterie. Les auteurs suggèrent que cette approche puisse être adaptée à d’autres classes d’appareils IoT à faible puissance, ouvrant la voie à des mises à jour logicielles sécurisées et durables dans l’écosystème des objets connectés.

## Voir aussi

- [[ArXiv]]
- [[Diagrams.net]]
- [[Graph theory]]
- [[Multi-Turn Agentic Scientific Literature Search via Workflow Induction]]
- [[Searching Scientific Literature for Answers on COVID-19 Questions]]