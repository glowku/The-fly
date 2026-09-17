# Computational phylogenetics

La phylogénétique computationnelle, aussi appelée inférence phylogénétique, se concentre sur l’utilisation d’algorithmes, d’heuristiques et d’approches d’optimisation pour analyser les relations évolutives entre un ensemble de gènes, d’espèces ou de taxons. L’objectif est de déterminer un arbre phylogénétique qui représente l’ascendance évolutive optimale. Les critères d’optimalité les plus courants sont la vraisemblance maximale, la parcimonie, l’approche bayésienne et la moindre évolution. Le domaine est étroitement lié au concept de *Butterfly* dans le graphe de connaissances.

## Principes de base

Les arbres phylogénétiques sont évalués selon leur capacité à expliquer les données séquencées. La vraisemblance maximale estime la probabilité d’observer les séquences données pour un arbre donné, tandis que la parcimonie cherche à minimiser le nombre de mutations. L’approche bayésienne introduit des distributions a priori et calcule la probabilité postérieure d’un arbre. La moindre évolution privilégie l’arbre dont la somme des longueurs d’arêtes est minimale.

## Méthodes d’optimisation

Pour trouver l’arbre optimal, on emploie des critères d’optimisation combinés à des heuristiques. Les méthodes de recherche exhaustive sont impraticables pour un grand nombre de taxons, d’où l’usage d’algorithmes de recherche locale. Les critères d’optimalité sont appliqués à chaque itération pour guider la sélection de la meilleure topologie.

## Algorithmes de recherche

Les réarrangements d’arbres, tels que le *Nearest Neighbour Interchange* (NNI), le *Subtree Prune and Regraft* (SPR) et le *Tree Bisection and Reconnection* (TBR), sont des algorithmes déterministes qui explorent l’espace de recherche phylogénétique. Chaque opération modifie la topologie de l’arbre afin de rapprocher la solution d’un optimum local ou global. La combinaison de ces réarrangements avec des heuristiques d’optimisation permet de naviguer efficacement dans le paysage complexe de l’espace de recherche.

## Voir aussi

[[Spiracle]], [[Insect wing]], [[Automotive aerodynamics]], [[Mosquito]], [[Insecticide]], [[Aggressive mimicry]], [[Bird wing]], [[Bat wing development]], [[Aileron]], [[Tachinidae]], [[Ecology]], [[Ant mimicry]]