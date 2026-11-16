# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID à puissance auto-générée (CRFID). Il combine une fonction physique unique (PUF) basée sur la mémoire SRAM avec un protocole d’actualisation de firmware, afin de surmonter les contraintes d’alimentation intermittente, de ressources limitées et l’absence de système d’exploitation supervisé.

## Contexte et problématique

Les dispositifs CRFID représentent une nouvelle catégorie d’appareils IoT sans batterie, qui récupèrent toute leur énergie via l’auto-génération électromagnétique. Bien que ces systèmes offrent connectivité et alimentation sans fil, la mise à jour sécurisée de leur firmware demeure un défi majeur. Les contraintes d’alimentation intermittente, la puissance de calcul restreinte et l’absence d’un système d’exploitation dédié compliquent la vérification d’intégrité et la protection contre les attaques de mise à jour malveillantes.

## Principe de fonctionnement

SecuCode introduit l’entrelacement d’une PUF SRAM intrinsèque au protocole de mise à jour. La PUF, caractéristique non clonable de la mémoire SRAM, génère un identifiant unique à chaque démarrage, même en l’absence d’alimentation stable. Ce mécanisme sert de clé d’authentification pour le firmware, assurant que seules les mises à jour signées par le fabricant peuvent être acceptées. Le protocole est entièrement compatible avec le standard ISO‑18000‑6C, le protocole de communication couramment utilisé par les CRFID, et s’appuie sur un cadre d’actualisation de firmware fourni par Texas Instruments, étendu pour intégrer la PUF.

## Implémentation et résultats

Une implémentation complète de SecuCode a été réalisée et testée sur des dispositifs CRFID réels. Les expérimentations démontrent la conformité aux normes ISO, la robustesse contre les attaques de falsification et l’efficacité énergétique. Les performances mesurées montrent que le processus d’authentification via la PUF impose un surcoût minimal, tout en garantissant la sécurité du firmware. Les résultats indiquent également que la mise à jour reste fiable malgré les interruptions fréquentes d’alimentation, grâce à la capacité de la PUF à réinitialiser l’état de l’appareil sans perte d’information.

## Voir aussi

[[ArXiv]], [[Supply chain security]], [[Code]], [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]], [[Technical drawing tool]]