# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé spécialement conçu pour les dispositifs RFID à puissance auto‑alimentée (CRFID). Il combine un protocole de mise à jour firmware standard avec une fonction physique unique (PUF) embarquée dans la mémoire SRAM, afin de garantir l’intégrité et l’authenticité des mises à jour malgré l’alimentation intermittente et les ressources limitées de ces appareils.

## Contexte et défis
Les dispositifs CRFID tirent leur énergie de l’environnement radio, ce qui les rend dépourvus de batterie et donc très sensibles aux coupures d’alimentation. Cette intermittence, couplée à une capacité de calcul réduite et à l’absence de système d’exploitation supervisé, rend difficile la mise en œuvre de mécanismes de mise à jour sécurisés. De plus, la plupart des protocoles de communication existants, tels que ISO‑18000‑6C, ne prennent pas en charge les exigences de sécurité supplémentaires nécessaires pour protéger le firmware contre les attaques de falsification ou d’injection de code malveillant.

## Architecture et mécanismes
SecuCode introduit une entanglement entre la PUF SRAM intrinsèque du dispositif et le protocole de mise à jour. À chaque tentative de mise à jour, le firmware est signé numériquement et l’empreinte de la PUF est utilisée pour authentifier l’appareil. Le protocole est entièrement compatible avec ISO‑18000‑6C, permettant ainsi une intégration transparente dans les infrastructures RFID existantes. En outre, SecuCode s’appuie sur un cadre de mise à jour fourni par Texas Instruments, qui étend la compilation et la distribution de firmware standard pour les CRFID.

## Évaluation et conformité
Une implémentation complète de SecuCode a été réalisée et testée sur un banc d’essai comprenant plusieurs dispositifs CRFID. Les résultats montrent une conformité totale aux normes ISO‑18000‑6C, ainsi qu’une faible surcharge de temps et de consommation d’énergie par rapport aux méthodes de mise à jour non sécurisées. Les mesures de sécurité démontrent que la combinaison PUF‑firmware empêche efficacement les attaques de re‑enregistrement et de falsification, même lorsque l’appareil est alimenté de façon intermittente.

## Voir aussi
[[Code]] [[Secure coding]] [[SecuCode Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computat]] [[Web]]