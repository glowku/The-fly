# SecuCode: Intrinsic PUF Entangled Secure Wireless Code Dissemination for Computational RFID Devices

SecuCode est un mécanisme de mise à jour logicielle sans fil sécurisé, conçu spécifiquement pour les dispositifs RFID à puissance auto‑alimentée (CRFID). En exploitant la fonction physique unique (PUF) intégrée dans la mémoire SRAM, SecuCode lie la signature de firmware à l’identité matérielle du dispositif, garantissant l’authenticité et l’intégrité des mises à jour malgré l’alimentation intermittente et les ressources limitées des CRFID.

## Contexte et problématique
Les dispositifs CRFID représentent une nouvelle génération d’appareils IoT sans batterie, reposant sur la récupération d’énergie électromagnétique pour fonctionner. Leur connectivité sans fil, couplée à l’absence d’un système d’exploitation supervisé, rend la distribution sécurisée de firmware particulièrement délicate. Les contraintes d’alimentation intermittente, de puissance de calcul réduite et de mémoire restreinte empêchent l’utilisation de protocoles de mise à jour classiques, créant un vide en matière de sécurité.

## Architecture et mécanismes
SecuCode intègre la PUF SRAM comme primitive de sécurité intrinsèque. Lorsqu’un dispositif reçoit une mise à jour, il génère un challenge‑response pair unique à partir de son état SRAM, puis le combine avec le firmware via un protocole d’authentification cryptographique. Cette entanglement garantit que seule la copie physique du dispositif peut valider la mise à jour, empêchant les attaques par duplication ou par injection de firmware malveillant. Le protocole est conçu pour être compatible avec ISO‑18000‑6C, le standard de communication utilisé par la majorité des CRFID, et s’appuie sur un cadre de mise à jour fourni par Texas Instruments, assurant ainsi une intégration transparente dans les chaînes de production existantes.

## Implémentation et résultats
Une implémentation complète de SecuCode a été réalisée et testée sur des dispositifs CRFID réels. Les expérimentations ont montré la conformité aux normes ISO‑18000‑6C, une latence de mise à jour acceptable pour les applications IoT, et une robustesse contre les attaques de falsification de firmware. Les performances de la PUF SRAM ont été évaluées en termes de stabilité et de reproductibilité, confirmant la fiabilité du mécanisme d’authentification même sous des conditions d’alimentation fluctuantes.

## Voir aussi
[[ArXiv]], [[Supply chain security]], [[Code]], [[Web]], [[Query expansion]]