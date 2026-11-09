# Beware of Validation by Eye: Visual Validation of Linear Trends in Scatterplots

Visual validation of regression models in scatterplots is a ubiquitous technique for judging model quality, yet its effectiveness has rarely been quantified. This article summarizes an arXiv study that empirically examined how accurately people can assess linear trends visually and how common graphical embellishments influence that assessment.

## Contexte et objectifs

Les chercheurs ont mené deux expériences pour mesurer la capacité des individus à estimer et à valider les pentes de régressions linéaires présentées dans des nuages de points. L’objectif principal était de déterminer si la visualisation d’une ligne de régression permet réellement aux observateurs de juger de la qualité du modèle, et d’évaluer l’impact de dispositifs graphiques fréquents (lignes d’erreur, boîtes de bordure, intervalles de confiance) sur cette capacité.

## Méthodologie et résultats

Dans la première expérience, les participants ont d’abord estimé la pente d’une ligne de régression, puis ont validé la pente affichée. Les résultats montrent que l’estimation visuelle de la pente est plus précise que la validation directe, mais les deux tâches présentent un biais systématique vers des pentes « trop raides ». Cette tendance suggère que les observateurs évaluent implicitement la régression en minimisant les distances orthogonales entre les points et la ligne (ODR) plutôt que les distances verticales classiques (OLS).  
La seconde expérience a introduit des éléments de visualisation courants. Bien que les lignes d’erreur aient réduit le biais de validation, aucune amélioration significative de la précision n’a été observée pour aucune des variantes testées. En conséquence, l’étude conclut qu’il faut faire preuve de prudence lorsqu’on se fie à la validation visuelle pour des tendances linéaires dans les nuages de points.

## Implications et limites

Les résultats indiquent que la perception visuelle des modèles linéaires est sujette à des biais systématiques et que les ajouts graphiques traditionnels ne corrigent pas nécessairement ces biais. Les praticiens de la visualisation de données doivent donc compléter les évaluations visuelles par des mesures quantitatives robustes, surtout lorsqu’une prise de décision critique dépend de la qualité du modèle.

## Voir aussi

* [[Data and information visualization]]
* [[Angular resolution (graph drawing)]]
* [[Area (graph drawing)]]
* [[Technical drawing]]