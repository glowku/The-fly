# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Il associe la fonction physique unique d’une mémoire SRAM (SRAM PUF) à un protocole de mise à jour firmware, afin de surmonter les contraintes d’alimentation intermittente, de puissance de calcul limitée et l’absence de système d’exploitation supervisé. Le système est entièrement compatible avec le protocole ISO‑18000‑6C et s’appuie sur une extension du cadre de mise à jour firmware fourni par Texas Instruments.

## Contexte et problématique

Les dispositifs CRFID représentent une nouvelle catégorie d’appareils IoT sans batterie, qui tirent toute leur énergie de la récupération d’énergie électromagnétique. Cette architecture offre une simplicité de déploiement et une opération perpétuelle, mais elle rend les mises à jour logicielles sans fil particulièrement délicates. Les interruptions d’alimentation fréquentes et les ressources computationnelles restreintes empêchent l’usage de mécanismes de sécurité traditionnels, tandis que l’absence d’un système d’exploitation supervisé limite les options de protection.

## Principe de SecuCode

SecuCode intègre la SRAM PUF, un primitive de sécurité matérielle intrinsèque, dans le processus de mise à jour firmware. La PUF génère un identifiant unique et non clonable à partir de la mémoire SRAM du dispositif, qui est utilisé pour authentifier et chiffrer les paquets de mise à jour. Le protocole de mise à jour, étendu à partir du cadre Texas Instruments, garantit que seules les firmwares signées et vérifiées par le propriétaire du dispositif peuvent être installées, même en présence d’alimentation intermittente. Cette approche élimine le besoin de stockage de clés privées ou de mécanismes de gestion de session complexes, tout en restant conforme aux normes industrielles.

## Implémentation et résultats

Une implémentation complète de SecuCode a été réalisée et testée sur un écosystème CRFID standard. Les expérimentations ont confirmé la conformité aux spécifications ISO‑18000‑6C, démontré la robustesse du mécanisme contre les attaques par rejeu et par falsification, et évalué les performances en termes de latence et de consommation d’énergie. Les résultats montrent que SecuCode permet une mise à jour sécurisée sans fil tout en respectant les contraintes de ressources propres aux dispositifs CRFID.

## Voir aussi

[[ArXiv]] [[ISO‑18000‑6C]] [[Texas Instruments firmware update framework]] [[Physical Unclonable Function (PUF)]] [[Internet of Things (IoT)]] [[Energy harvesting]]