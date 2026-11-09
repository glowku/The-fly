# Template-Based Graph Clustering

Template-Based Graph Clustering (TBC) est une méthode de partitionnement de graphes qui intègre des connaissances supplémentaires sur la structure des communautés à découvrir. Contrairement aux approches classiques, TBC ne se contente pas de la topologie brute ; elle compare le graphe observé à un modèle de référence (template) de dimension réduite. Le résultat est un embedding de dimension \(k\) qui respecte à la fois les connexions du graphe et les contraintes imposées par le template. Cette approche permet de surmonter les difficultés rencontrées par les méthodes de clustering traditionnelles, notamment dans les cas de communautés très denses ou fortement imbriquées.

## Méthodologie

Le problème est formulé comme une correspondance entre le graphe observé \(G=(V,E)\) et un template \(T=(U,F)\) où \(|V|=n\) et \(|U|=k\) avec \(k \ll n\). Chaque sommet de \(G\) est associé à un sommet de \(T\) via une matrice d’affectation \(X \in \mathbb{R}^{n \times k}\). Les arêtes du template servent de support pour guider l’alignement : deux sommets de \(G\) sont plus susceptibles d’être placés dans la même cluster si l’arête correspondante existe dans \(T\). Pour rendre le problème tractable, la contrainte d’orthogonalité sur \(X\) est relâchée, ce qui conduit à une optimisation sur l’ensemble des matrices orthonormées. Les priorités pertinentes, telles que la densité attendue des clusters et les relations entre eux, sont intégrées dans la fonction de coût. Le résultat final est un embedding de dimension \(k\) qui peut être interprété comme une représentation latente des communautés.

## Avantages et performances

Les expérimentations montrent que TBC dépasse les méthodes classiques (k-moyennes, spectral clustering, Louvain) surtout dans les scénarios où les clusters présentent des densités très inégales ou des interconnexions complexes. La capacité à injecter des priors sur la structure des clusters permet d’éviter les pièges d’over‑clustering ou de fragmentation. De plus, la relaxation sur les matrices orthonormées assure une convergence plus stable et une meilleure interprétabilité du résultat. Les évaluations sur des graphes synthetiques et réels démontrent une amélioration significative de la précision de clustering, mesurée par des indices tels que l’indice de Rand ajusté ou la silhouette.

## Voir aussi

- [[Angular resolution (graph drawing)]]
- [[Area (graph drawing)]]
- [[Insects in ethics]]
- [[Behavioral ecology (disambiguation