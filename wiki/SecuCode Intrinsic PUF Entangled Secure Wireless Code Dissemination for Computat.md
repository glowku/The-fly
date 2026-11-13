# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Il exploite une fonction physique unique (PUF) embarquée dans la mémoire SRAM pour authentifier les mises à jour de firmware, tout en restant compatible avec les protocoles de communication existants. Le système est adapté aux contraintes d’énergie intermittente et de ressources limitées propres aux CRFID, et s’appuie sur un cadre de mise à jour fourni par Texas Instruments.  

## Contexte et enjeux des dispositifs CRFID  
Les CRFID représentent une nouvelle catégorie d’appareils IoT sans batterie, qui tirent leur énergie de l’environnement radio. Leur fonctionnement intermittent, leurs capacités de calcul restreintes et l’absence d’un système d’exploitation supervisé compliquent la distribution sécurisée de firmware. Les mises à jour sans fil doivent donc être légères, fiables et résilientes aux coupures d’alimentation.  

## Architecture et mécanismes de SecuCode  
SecuCode intègre la PUF SRAM intrinsèque du dispositif dans le protocole de mise à jour. Lorsqu’une mise à jour est initiée, le firmware est signé par le serveur, puis le dispositif génère un défi‑réponse à partir de sa PUF. Cette réponse, combinée à la signature, constitue une preuve d’authenticité que le firmware n’a pas été altéré et que le dispositif est bien celui prévu. Le protocole est entièrement compatible avec ISO‑18000‑6C, le standard de communication des RFID, et repose sur une compilation et une mise à jour de firmware conformes aux pratiques industrielles.  

## Évaluation et conformité aux standards  
Une implémentation complète a été réalisée et testée sur plusieurs plateformes CRFID. Les expérimentations démontrent la conformité aux normes ISO‑18000‑6C, l’efficacité du protocole même en cas d’alimentation intermittente, et la robustesse contre les attaques par falsification de firmware. Les performances mesurées montrent un temps de mise à jour raisonnable, compatible avec les contraintes énergétiques des dispositifs.  

## Voir aussi  
- [[ArXiv]]  
- [[Image]]  
- [[Diagrams