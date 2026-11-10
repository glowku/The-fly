# Information retrieval

L’information retrieval (IR) désigne la recherche et la récupération d’informations pertinentes dans un système d’information. Elle se base sur une *information need*, souvent exprimée sous forme de requête. L’IR englobe la recherche de documents, de métadonnées et de contenus multimédias (textes, images, sons), ainsi que la recherche de données structurées dans des bases de données.

## Principes fondamentaux

La première étape consiste à *indexer* les ressources. L’indexation peut être textuelle (full‑text) ou basée sur d’autres caractéristiques du contenu, comme les métadonnées ou les signatures multimodales. Lorsqu’une requête est soumise, le moteur d’IR parcourt l’index pour identifier les éléments les plus proches de la demande. Les modèles de pertinence, tels que le modèle vectoriel ou le modèle probabiliste, évaluent la similarité entre la requête et les documents. Les résultats sont ensuite triés et présentés à l’utilisateur.

## Applications et extensions

L’IR est employé dans de nombreux domaines : moteurs de recherche Web, systèmes de recommandation, bases de données de recherche scientifique, et services de gestion de documents d’entreprise. Le *cross‑modal retrieval* étend la recherche à travers différentes modalités (texte, image, audio), permettant, par exemple, de retrouver une image à partir d’une description textuelle. Les graphes de connaissances, souvent stockés dans des [[Graph database]], facilitent la représentation des relations entre entités, tandis que les théories de [[Network theory]] aident à analyser la structure des liens entre documents. Les techniques d’[[Automated reasoning]] sont parfois intégrées pour inférer des relations implicites ou pour reformuler les requêtes. Enfin, la sécurité de l’information, notamment via des mécanismes d’[[Application security]], garantit l’intégrité et la confidentialité des données récupérées.

## Voir aussi

- [[Graph database]]
- [[Network theory]]
- [[Automated reasoning]]
- [[Application security]]
- [[Cross-origin resource sharing]]