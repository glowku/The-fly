# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé conçu spécifiquement pour les dispositifs RFID computationnels (CRFID). Ces appareils, alimentés par l’énergie ambiante, fonctionnent sans batterie et disposent de capacités de calcul limitées. La mise à jour de leur firmware via le réseau pose des défis uniques liés à l’alimentation intermittente, aux ressources restreintes et à l’absence de système d’exploitation supervisé. SecuCode propose une solution intégrée en liant une fonction physique non clonable (PUF) basée sur la mémoire SRAM aux protocoles de mise à jour existants, notamment ISO‑18000‑6C.

## Contexte et problématique

Les CRFID représentent une nouvelle catégorie d’appareils IoT de bord, capables de récolter toute leur énergie pour fonctionner. Leur nature sans batterie les rend particulièrement vulnérables aux attaques de mise à jour logicielle, car les adversaires peuvent intercepter ou altérer le code transmis sans que l’appareil ne dispose d’un mécanisme de vérification robuste. De plus, la puissance intermittente limite la capacité de traitement et empêche l’utilisation de solutions de sécurité classiques, qui exigent souvent un système d’exploitation ou des ressources mémoire importantes.

## Architecture et mécanisme de SecuCode

SecuCode s’appuie sur une PUF SRAM intrinsèque, un élément matériel unique à chaque dispositif, pour authentifier et chiffrer les mises à jour. Le protocole fonctionne en trois étapes : (1) génération d’un challenge‑response pair à partir de la PUF, (2) utilisation de la réponse comme clé de chiffrement symétrique pour le firmware, et (3) transmission sécurisée via ISO‑18000‑6C. Cette approche élimine le besoin d’un stockage de clé externe ou d’une infrastructure de gestion de clés, tout en restant compatible avec les normes industrielles. Le mécanisme est intégré dans un cadre de mise à jour fourni par Texas Instruments, étendu pour supporter la PUF et les contraintes énergétiques des CRFID.

## Évaluation et conformité

Une implémentation complète de SecuCode a été réalisée et testée sur des dispositifs CRFID réels. Les expérimentations ont démontré la conformité aux protocoles ISO‑18000‑6C, la robustesse contre les attaques par rejeu et la résilience face aux coupures d’alimentation. Les performances montrent que la génération de la PUF et le chiffrement peuvent être effectués en quelques millisecondes, ce qui est compatible avec les cycles d’alimentation intermittents. En outre, la solution ne nécessite aucune modification du firmware existant, ce qui facilite son adoption dans les chaînes d’approvisionnement actuelles.

## Voir aussi

[[Secure coding]] [[Visual Studio]] [[Compass (drawing tool)]] [[Contour drawing]] [[Insect flight]]