# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés exclusivement par l’énergie captée dans leur environnement, offrent une autonomie permanente mais présentent des contraintes uniques : alimentation intermittente, capacités de calcul limitées et absence d’un système d’exploitation supervisé. SecuCode répond à ces défis en liant la fonction physique non clonable (PUF) intégrée dans la mémoire SRAM aux protocoles de mise à jour firmware.

## Contexte et motivation
Les CRFID représentent une nouvelle génération d’objets connectés sans batterie, capables de réaliser des tâches de calcul et de capteur tout en récupérant l’énergie électromagnétique. Leur déploiement à grande échelle dépend de la possibilité de mettre à jour leur firmware de façon fiable et sécurisée. Les approches traditionnelles échouent en raison de l’alimentation intermittente et de l’absence de mécanismes de protection classiques. SecuCode introduit une solution qui exploite la PUF SRAM, un atout matériel intrinsèque, pour authentifier et sécuriser chaque transmission de code.

## Architecture et mécanismes
Le protocole SecuCode s’appuie sur le standard de communication ISO‑18000‑6C, largement utilisé par les dispositifs CRFID, garantissant ainsi une compatibilité immédiate avec les infrastructures existantes. La PUF SRAM produit un identifiant unique et non reproductible à chaque démarrage, qui est intégré dans le processus de signature du firmware. En étendant le cadre de mise à jour fourni par Texas Instruments, SecuCode conserve les méthodes de compilation et de distribution standard tout en ajoutant une couche de sécurité basée sur le matériel. Cette approche élimine le besoin d’un système d’exploitation supervisé et permet une authentification robuste même lors d’alimentations intermittentes.

## Évaluation et conformité
Une implémentation complète de SecuCode a été réalisée et testée sur plusieurs plateformes CRFID. Les expérimentations démontrent la conformité aux exigences du protocole ISO‑18000‑6C, ainsi qu’une performance acceptable en termes de temps de mise à jour et de consommation énergétique. Les analyses de sécurité montrent que la combinaison de la PUF SRAM et du protocole de mise à jour empêche efficacement les attaques de falsification et de relecture. Les résultats indiquent que SecuCode constitue une solution viable pour la gestion sécurisée des dispositifs IoT sans batterie.

## Voir aussi
[[Application security]] [[Automated reasoning]] [[Diagrams.net]] [[Image]] [[Searching Scientific Literature for Answers on COVID-19 Questions]]