# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID à puissance auto-générée (CRFID). En exploitant la fonction physique non clonable (PUF) intégrée aux mémoires SRAM, SecuCode lie de façon intrinsèque l’authenticité du firmware à l’identité matérielle du lecteur, tout en restant compatible avec les protocoles de communication existants, notamment ISO‑18000‑6C.

## Fonctionnement et principe de sécurité

Les CRFID, dépourvus de batterie et de système d’exploitation supervisé, doivent fonctionner avec des alimentations intermittentes et des ressources computationnelles limitées. SecuCode surmonte ces contraintes en s’appuyant sur la PUF SRAM, qui génère un identifiant unique à partir des fluctuations de tension de chaque cellule mémoire. Ce « signature matérielle » est calculée à chaque démarrage et sert de clé d’authentification pour le protocole de mise à jour. Ainsi, le firmware ne peut être installé que si la signature correspond à celle attendue par le serveur, empêchant les attaques par injection de code malveillant.

## Compatibilité et mise en œuvre

Le système est entièrement compatible avec l’ISO‑18000‑6C, le standard industriel pour les lecteurs RFID. Il s’intègre également à un cadre de mise à jour logicielle fourni par Texas Instruments, qui étend la compilation et la distribution de firmware standard. L’implémentation complète de SecuCode a été réalisée sur un prototype CRFID, démontrant la conformité aux normes et la faisabilité pratique de la mise à jour sans fil dans un environnement à faible puissance.

## Évaluation expérimentale

Des expériences approfondies ont été menées pour mesurer la performance et la robustesse de SecuCode. Les résultats montrent que la génération de la signature PUF et la vérification d’authenticité ajoutent un délai minimal, compatible avec les contraintes de cycle de vie des CRFID. De plus, l’architecture a été testée contre des attaques de relecture et de falsification, confirmant la résistance du mécanisme grâce à l’entrelacement matériel du firmware et de la PUF.

## Voir aussi

* [[ArXiv]]
* [[Supply chain security]]
* [[Code]]
* [[ISO‑18000‑6C]]
* [[Texas Instruments]]
* [[Network theory of aging]]