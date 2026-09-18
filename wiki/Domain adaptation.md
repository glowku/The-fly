# Domain adaptation

Domain adaptation est une branche du machine learning et de l’apprentissage par transfert qui se concentre sur la problématique de former un modèle sur une distribution de données source, puis de l’appliquer à une distribution cible différente mais liée. Cette approche vise à surmonter les disparités entre les ensembles de données d’entraînement et de test, afin d’améliorer la robustesse et la généralisation des modèles dans des environnements réels.

## Définition

Dans le cadre de l’apprentissage supervisé, un modèle est généralement entraîné sur un jeu de données étiqueté provenant d’une source particulière (par exemple, des images capturées dans un laboratoire). Lorsque ce modèle est déployé sur un nouveau domaine – comme des images prises dans des conditions de lumière différentes ou à partir d’un appareil photo distinct – ses performances peuvent chuter drastiquement. La domain adaptation propose des techniques pour aligner les représentations des deux domaines, en réduisant la divergence statistique entre eux.

## Principes fondamentaux

Les méthodes de domain adaptation se répartissent en deux grandes familles :  
1. **Adaptation sans supervision** : aucune donnée étiquetée n’est disponible dans le domaine cible. Les algorithmes cherchent alors à minimiser la distance entre les distributions source et cible en utilisant des mesures telles que la divergence de Jensen‑Shannon ou l’entropie croisée.  
2. **Adaptation semi‑supervisée** : quelques étiquettes sont disponibles dans le domaine cible. Le modèle exploite ces informations pour affiner ses paramètres, souvent via des techniques de co‑étiquetage ou de rééchantillonnage.

Les approches les plus courantes incluent l’alignement de caractéristiques, l’apprentissage de représentations invariantes et la régularisation basée sur la divergence de distribution. Le choix de la méthode dépend de la disponibilité des données, de la similarité entre les domaines et des contraintes computationnelles.

## Applications et défis

La domain adaptation trouve des applications dans la vision par ordinateur (reconnaissance d’objets entre différents environnements), le traitement du langage naturel (adaptation de modèles de traduction à des registres spécifiques) et la santé (transfert de modèles d’imagerie médicale entre hôpitaux). Les principaux défis résident dans la quantification de la disparité entre domaines, la préservation de la discrétion des caractéristiques pertinentes et la gestion de la complexité computationnelle.

## Voir aussi
[[Evolution (journal)]], [[Gene-centered view of evolution]], [[Foraging]], [[Desert ecology]], [[Arctic ecology]]