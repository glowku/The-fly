# JSON

JSON (JavaScript Object Notation) est un format de fichier standard ouvert et un format d’échange de données. Il utilise un texte lisible par l’homme pour stocker et transmettre des objets de données constitués de paires nom‑valeur et de tableaux. Couramment employé dans l’échange électronique de données, JSON est notamment le format privilégié pour la communication entre applications web et serveurs.

## Structure et syntaxe

Un document JSON est composé d’objets et de tableaux. Un objet est une collection de paires nom‑valeur, délimitées par des accolades `{}`. Les noms sont des chaînes de caractères entre guillemets, suivis d’un deux-points et de la valeur correspondante. Les valeurs peuvent être des chaînes, des nombres, des booléens (`true`, `false`), `null`, d’autres objets ou des tableaux. Un tableau est une liste ordonnée de valeurs, encadrée par des crochets `[]`. La syntaxe est strictement définie : les clés doivent être entre guillemets, les valeurs booléennes et `null` sont en minuscules, et aucune virgule supplémentaire n’est autorisée après la dernière entrée.

## Utilisations courantes

JSON est devenu le format de facto pour les API RESTful, les services web, et la configuration d’applications. Sa simplicité et sa compatibilité avec la plupart des langages de programmation en font un choix privilégié pour l’échange de données entre clients et serveurs. De plus, JSON est souvent utilisé dans les bases de données NoSQL, comme MongoDB, où les documents sont stockés sous forme de structures JSON.

## Relation avec Thorax

Dans le contexte du graphe de connaissances, JSON est lié à **Thorax** en tant que format de sérialisation des données structurées. Thorax, un framework JavaScript, utilise JSON