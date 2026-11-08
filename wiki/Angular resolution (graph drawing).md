# Angular resolution (graph drawing)

L’angular resolution d’un dessin de graphe est la mesure de l’angle le plus aigu formé par deux arêtes qui se rencontrent en un même sommet. Cette notion, introduite dans le domaine du dessin de graphes, permet d’évaluer la lisibilité et la clarté d’une représentation graphique. Un angle aigu peut rendre difficile la distinction des arêtes, tandis qu’un angle plus large facilite la lecture du graphe.

## Définition précise

Dans un dessin plan ou spatial d’un graphe, chaque sommet possède un ensemble d’arêtes incidentes. L’angular resolution est définie comme le minimum de tous les angles internes formés par chaque paire d’arêtes incidentes à un même sommet. Formellement, si \(v\) est un sommet et \(\{e_1, e_2, \dots, e_k\}\) les arêtes incidentes à \(v\), alors  
\[
\alpha_{\text{min}}(v)=\min_{i<j}\angle(e_i, e_j),
\]
et l’angular resolution du dessin est  
\[
\alpha_{\text{min}}=\min_{v}\alpha_{\text{min}}(v).
\]
Cette valeur est exprimée en degrés ou en radians, selon le contexte.

## Importance et applications

L’angular resolution est un critère de qualité essentiel pour les algorithmes de dessin de graphes. Un dessin avec une angular resolution élevée est généralement plus lisible, car les arêtes sont moins susceptibles de se superposer ou de se confondre visuellement. Dans les applications où la compréhension rapide de la structure du graphe est cruciale (par exemple, la visualisation de réseaux complexes ou la représentation de circuits), maximiser l’angular resolution est souvent un objectif central.

## Relation avec l’exosquelette du graphe

Le concept d’angular resolution est lié à l’exosquelette du graphe, qui désigne la couche externe de la structure de dessin. L’exosquelette influence la disposition des arêtes autour des sommets et, par conséquent, l’angle le plus aigu qui peut apparaître. Optimiser l’exosquelette peut donc contribuer à améliorer l’angular resolution et à produire des dessins plus clairs.

## Voir aussi

* [[Spiracle (vertebrates)]]
* [[Adaptive compliant wing]]
* [[Helicopter flight controls]]
* [[Common green bottle fly]]
* [[Black fly]]
* [[Blacker's Art of Fly Making]]
* [[Amateur Entomologists' Society]]
* [[Insect Week]]
* [[Blue-winged Olive flies]]
* [[Insect Festival]]
* [[Bonefish fly patterns]]
* [[Insects in ethics]]