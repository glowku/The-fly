# Query expansion

La **query expansion** (QE) désigne la reformulation d’une requête initiale afin d’améliorer la performance des opérations de recherche d’information, notamment dans le cadre de la compréhension de requête. Elle consiste à enrichir la requête utilisateur en y ajoutant des termes pertinents, ce qui permet de rapprocher la requête des documents disponibles dans l’index.

## Techniques de l’expansion de requête

Les méthodes classiques de QE comprennent :
- **Recherche de synonymes** : l’ajout de mots ayant la même signification que ceux de la requête originale.
- **Mots sémantiquement liés** : l’inclusion de termes proches sur le plan sémantique, souvent obtenus via des modèles de langage ou des graphes de connaissances.
- **Morphologie** : le stemming ou la lemmatisation qui génèrent toutes les formes morphologiques d’un mot.
- **Correction orthographique** : la détection et la correction automatique des fautes d’orthographe, avec suggestion de la forme corrigée dans les résultats.
- **Réévaluation des poids** : l’ajustement des poids des termes de la requête pour refléter leur importance relative dans le contexte de la recherche.

Ces techniques peuvent être combinées ou appliquées séquentiellement selon les besoins du système de recherche.

## Applications et bénéfices

L’expansion de requête est particulièrement utile lorsque la requête est courte ou vague, ou lorsqu’elle contient des termes peu fréquents. En élargissant le champ lexical, la QE augmente la couverture des documents pertinents et réduit le risque de résultats hors sujet. Elle est également un composant clé des systèmes de recherche adaptatifs, où les requêtes sont continuellement réévaluées en fonction des retours utilisateurs et des interactions de recherche.

## Relation avec l’indexation des moteurs de recherche

La QE s’appuie sur l’indexation des moteurs de recherche, qui stocke les termes et leurs occurrences dans les documents. En exploitant les index, le système peut rapidement identifier les documents contenant les termes supplémentaires générés par l’expansion, tout en maintenant des temps de réponse acceptables. De plus, les techniques d’indexation inversée facilitent la mise à jour et la gestion des termes supplémentaires introduits par la QE.

## Voir aussi

- [[A Case-Driven Multi-Agent Framework for E-Commerce Search Relevance]]
- [[Multi-Turn Agentic Scientific Literature Search via Workflow Induction]]
- [[Automated reasoning]]
- [[Diagrammatic reasoning]]