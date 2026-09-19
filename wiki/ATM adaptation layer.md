# ATM adaptation layer

L’**ATM adaptation layer** (AL) est la couche intermédiaire qui permet d’intégrer des protocoles de transfert d’information non‑ATM dans un réseau ATM. Elle découpe les paquets de couches supérieures en cellules ATM de 53 octets, assure leur réassemblage à la destination et gère divers aspects de la transmission propres à ATM, tels que le contrôle de flux, la gestion des erreurs et la qualité de service.

## Fonctionnement de l’adaptation

L’AL se situe entre la couche de transport (ou couche réseau) et la couche ATM. Lorsqu’un paquet arrive, l’AL le fragmentise en cellules, en ajoutant un en‑tête de 5 octets contenant les informations de routage et de contrôle. À l’arrivée, les cellules sont re‑assemblées en un paquet cohérent. Cette opération garantit que les protocoles comme TCP, IP ou même des protocoles propriétaires puissent circuler sur un réseau ATM sans modification majeure de leur structure.

## Rôle dans les réseaux

Dans les réseaux ATM, l’AL est indispensable pour la coexistence de services à haut débit (tels que la vidéo ou le son) et de services à faible débit (tels que la voix ou les données). Elle permet de préserver la qualité de service (QoS) en attribuant des classes de service aux cellules et en appliquant des mécanismes de contrôle de congestion. Sans l’AL, les protocoles non‑ATM ne pourraient pas être encapsulés dans le format cellulaire ATM, ce qui limiterait considérablement la flexibilité du réseau.

## Implémentations et normes

La norme ITU‑T Q.2931 définit l’ATM adaptation layer, tandis que Q.2932 spécifie la couche de gestion de la qualité de service. Ces normes précisent les formats d’en‑tête, les mécanismes de contrôle de flux et les procédures de réassemblage. Les implémentations logicielles et matérielles des routeurs ATM intègrent ces spécifications pour assurer la compatibilité inter‑opérable entre équipements de différents fournisseurs.

## Voir aussi

* [[Asynchronous Transfer Mode]]
* [[ATM cell]]
* [[Adaptation (disambiguation)]]
* [[Network layer]]
* [[Protocol adaptation]]
* [[Quality of Service]]