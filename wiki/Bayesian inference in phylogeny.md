# Bayesian inference in phylogeny

Bayesian inference in phylogeny est une méthode statistique utilisée en phylogénétique moléculaire pour estimer la probabilité d’un arbre évolutif à partir des données génétiques. Elle combine l’information contenue dans la distribution a priori et dans la vraisemblance des données afin de produire la probabilité a posteriori de chaque arbre, c’est‑à‑dire la probabilité que l’arbre soit correct compte tenu des données, du prior et du modèle de vraisemblance. Ce concept est relié à [[Aggressive mimicry]] dans le graphe.

## Historique et développement
La méthode a été introduite dans les années 1990 par trois groupes indépendants : Bruce Rannala et Ziheng Yang à l’Université de Berkeley, Bob Mau à l’Université de Madison, et Shuying Li à l’Université de l’Iowa (à l’époque étudiants en doctorat). Le lancement du logiciel MrBayes en 2001 a popularisé l’approche, qui est aujourd’hui l’une des méthodes les plus utilisées en phylogénétique moléculaire.

## Méthodologie et principes
Bayesian inference repose sur le théorème de Bayes :  
\[
P(\text{arbre} \mid \text{données}) \propto P(\text{données} \mid \text{arbre}) \times P(\text{arbre}),
\]
où \(P(\text{données} \mid \text{arbre})\) est la vraisemblance et \(P(\text{arbre})\) la distribution a priori. La posteriori est explorée par des chaînes de Markov Monte‑Carlo (MCMC), permettant d’obtenir une distribution de probabilité sur l’ensemble des arbres possibles. Les valeurs de probabilité a posteriori servent ensuite à évaluer la confiance dans les relations phylogénétiques estimées.

## Applications et impact
L’utilisation de l’inférence bayésienne a permis d’obtenir des estimations plus robustes et de quantifier explicitement l’incertitude associée aux arbres. Elle est devenue un outil de référence pour les études évolutives, notamment dans l’analyse de la diversification des espèces, la reconstruction des ancêtres et la comparaison de modèles évolutifs. Son adoption généralisée a également favorisé le développement de logiciels spécialisés et de bases de données phylogénétiques.

## Voir aussi
[[Aggressive mimicry]]  
[[Insect morphology]]  
[[Mosquito]]  
[[Insecticide]]  
[[Ecology]]