# Principle of least privilege

Le principe de moindre privilège (PoLP), principe de privilège minimal (PoMP) ou principe de moindre autorité (PoLA) est un concept fondamental en sécurité de l'information et en informatique. Il stipule que, dans chaque couche d’abstraction d’un environnement de calcul, chaque module ne doit disposer que des droits d’accès strictement nécessaires à son objectif légitime. Ce principe vise à limiter la surface d’attaque et à réduire les conséquences d’une compromission.

## Historique et fondements théoriques

Le PoLP trouve ses racines dans les bonnes pratiques de gestion des accès et dans la théorie de la défense en profondeur. Il s’appuie sur l’idée que la restriction d’autorisations minimise les risques d’erreur humaine ou d’exploitation malveillante. En pratique, il se traduit par la mise en place de rôles, de groupes et de politiques d’accès granulaires. Les systèmes d’exploitation modernes, les bases de données et les services cloud intègrent ce principe via des mécanismes tels que les ACL, les listes de contrôle d’accès (ACL) et les politiques IAM.

## Application dans les environnements distribués

Dans les architectures distribuées, le PoLP est crucial pour éviter les fuites de données entre services. Chaque micro‑service ne possède que les permissions nécessaires pour communiquer avec les services voisins. Ce principe est également lié au Cross‑origin resource sharing (CORS) dans le contexte des graphes, où les requêtes entre domaines sont strictement contrôlées pour empêcher l’accès non autorisé aux ressources graph. En appliquant le PoLP, les développeurs peuvent définir des règles CORS précises, garantissant que seules les requêtes provenant de domaines approuvés sont autorisées.

## Impact sur la conception et la maintenance

En adoptant le PoLP, les organisations réduisent la complexité de la gestion des droits d’accès et améliorent la traçabilité des actions. Les audits de sécurité deviennent plus simples, car chaque privilège est documenté et justifié. De plus, la maintenance est facilitée : lorsqu’un module est mis à jour ou retiré, il suffit de réviser ses permissions sans affecter l’ensemble du système. Le PoLP est ainsi un levier essentiel pour la conformité aux normes de sécurité telles que ISO 27001 ou PCI‑DSS.

## Voir aussi

[[Graph database]] [[Data and information visualization]] [[Technical drawing]] [[Angular resolution (graph drawing)]] [[Area (graph drawing)]]