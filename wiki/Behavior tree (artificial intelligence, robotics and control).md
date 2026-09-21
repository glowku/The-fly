# Behavior tree (artificial intelligence, robotics and control)

Un **arbre de comportement** (behavior tree) est un modèle mathématique de l’exécution de plans utilisé en informatique, en robotique, en systèmes de contrôle et dans les jeux vidéo. Il décrit les basculements entre un nombre fini de tâches de façon modulaire. Sa force réside dans la possibilité de composer des tâches très complexes à partir de tâches simples, sans se soucier de la mise en œuvre de ces dernières. Les arbres de comportement présentent des similitudes avec les machines à états hiérarchiques, la différence majeure étant que le bloc de construction principal est une tâche plutôt qu’un état. Leur lisibilité humaine les rend moins sujets aux erreurs et très populaires dans la communauté des développeurs de jeux. Les arbres de comportement ont également démontré leur capacité à se généraliser à plusieurs autres architectures de contrôle.

## Modèle mathématique et architecture

Un arbre de comportement est constitué d’un ensemble fini de nœuds, chacun représentant une tâche ou un compositeur (séquence, sélection, parallèle, etc.). Le flux d’exécution se fait en parcourant l’arbre, en évaluant les nœuds enfants selon des règles prédéfinies. Les compositeurs orchestrent la logique de contrôle, tandis que les tâches terminales exécutent des actions concrètes ou évaluent des conditions. Cette séparation claire entre logique de contrôle et actions permet d’ajouter, de modifier ou de réutiliser des tâches sans impacter l’architecture globale. Le modèle mathématique se base sur la théorie des graphes orientés, où chaque nœud possède un état d’exécution (succeed, fail, running) qui guide le flux de contrôle.

## Applications et avantages

Les arbres