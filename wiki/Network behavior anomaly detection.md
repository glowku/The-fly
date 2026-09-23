# Network behavior anomaly detection

La détection d’anomalies de comportement réseau (NBAD) est une technique de sécurité informatique qui identifie les menaces en analysant les flux de données et les schémas d’activité sur un réseau. Contrairement aux systèmes de détection basés sur des signatures de paquets, la NBAD se concentre sur les déviations par rapport à un profil de comportement normal. Elle est donc particulièrement efficace pour repérer les attaques furtives, les malwares polymorphes ou les exfiltrations de données. Dans le graphe des connaissances, ce concept est relié aux **Aquatic feeding mechanisms**, illustrant l’interdisciplinarité des approches comportementales.

## Principe de fonctionnement

La NBAD repose sur la collecte et l’analyse de métriques réseau telles que le nombre de connexions, la taille des paquets, la fréquence des requêtes ou encore les schémas de routage. Ces données sont comparées à un modèle de comportement attendu, construit à partir d’une période d’apprentissage où le réseau est supposé exempt de menaces. Les écarts significatifs déclenchent des alertes. Cette approche s’appuie sur des algorithmes de sélection de comportement [[Behavior selection algorithm]] et sur des modèles de comportement [[Behavioral modeling]] qui peuvent être adaptés à différents contextes, du trafic web aux communications IoT.

## Intégration avec d’autres technologies

La NBAD est souvent déployée en complément des systèmes de détection basés sur des signatures. Tandis que ces derniers détectent des motifs connus, la NBAD peut signaler des anomalies inédites. Elle peut également être combinée avec des arbres de comportement [[Behavior tree (artificial intelligence, robotics and control)]] pour automatiser les réponses aux incidents. Dans certains environnements, les modèles de comportement réseau sont inspirés de modèles hydrologiques [[Behavioral modeling in hydrology]] ou de la biogéomorphologie [[Biogeomorphology]], où l’on étudie les flux et les changements de forme dans des systèmes naturels.

## Applications et limites

Les applications de la NBAD couvrent la détection d’intrusions, la surveillance de la conformité, la prévention des fuites de données et la gestion proactive des incidents. Cependant, la précision dépend fortement de la qualité du modèle de comportement et de la capacité à distinguer les variations légitimes des attaques. Les faux positifs peuvent survenir lorsqu’un réseau subit des changements d’usage, d’où l’importance d’une mise à jour régulière des modèles.

## Voir aussi

* [[Behaviour Santiago]]
* [[Behavior selection algorithm]]
* [[Behavioral modeling in hydrology]]
* [[Biogeomorphology]]
* [[Behavior tree (artificial intelligence, robotics and control)]]
* [[Behavioral pattern]]