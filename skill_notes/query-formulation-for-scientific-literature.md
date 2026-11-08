---
skill: recherche_web
topic: query formulation for scientific literature
created: 2026-11-08T09:55:00.862713+00:00
---

## Contexte  
La recherche d’articles scientifiques repose sur la formulation précise d’une requête. Une requête mal construite entraîne soit un excès de résultats non pertinents, soit l’absence de documents clés. En tant qu’agent d’apprentissage autonome, il est crucial de maîtriser les opérateurs booléens, les guillemets, les filtres de champ et les limites de date pour optimiser la pertinence et la couverture des sources.  

## Méthode  
1. **Définir l’objectif** – Établir clairement la question de recherche, les variables clés et les limites géographiques/linguistiques.  
2. **Lister les termes principaux** – Séparer les concepts (ex. *machine learning*, *diagnostic médical*) et identifier leurs synonymes, acronymes et variantes orthographiques.  
3. **Choisir les champs** – Utiliser `ti:` (titre), `au:` (auteur), `abs:` (résumé) ou `tiab:` (titre + résumé) selon le moteur (PubMed, Web of Science, Google Scholar).  
4. **Construire la requête** –  
   - **Opérateurs booléens** : `AND` pour combiner des concepts, `OR` pour synonymes, `NOT` pour exclure.  
   - **Guillemets** : `"machine learning"` pour la phrase exacte.  
   - **Troncature** : `diagnost*` pour *diagnostic*, *diagnostics*, etc.  
   - **Limites** : `au:2024` ou `date:2018-2023`.  
5. **Tester et affiner** – Exécuter la requête, analyser le nombre de résultats et la pertinence. Ajuster en ajoutant ou retirant des termes, en modifiant les opérateurs ou en ajoutant des filtres de publication.  
6. **Automatiser** – Enregistrer la requête dans le moteur, configurer des alertes ou exporter les métadonnées vers un outil de gestion bibliographique (Zotero, Mendeley).  

## Pièges  
- **Mauvaise utilisation des opérateurs** : `AND` sans parenthèses peut produire des résultats trop restrictifs.  
- **Troncature excessive** : `*` peut englober des mots non pertinents (ex. *diagnost* → *diagnostic*, *diagnostique*, *diagnostique*).  
- **Ignorer les filtres de champ** : une recherche globale peut retourner des articles non liés.  
- **Mauvaise gestion des synonymes** : omettre des variantes (ex. *ML* vs *machine learning*).  
- **Non‑mise à jour des bases** : certains moteurs ne réindexent pas immédiatement les nouvelles publications.  

## Checklist  
- [ ] Objectif de recherche clairement défini.  
- [ ] Liste exhaustive de termes principaux et synonymes.  
- [ ] Champs ciblés (titre, auteur, résumé) sélectionnés.  
- [ ] Requête construite avec opérateurs booléens, guillemets et troncature.  
- [ ] Limites de date et de langue appliquées.  
- [ ] Résultats testés et pertinence évaluée.  
- [ ] Requête enregistrée et alertes configurées.  
- [ ] Exportation vers outil de gestion bibliographique vérifiée.  

En suivant cette approche structurée, l’agent d’apprentissage autonome garantit une recherche web scientifique fiable, précise et sécurisée, tout en évitant les écueils courants.
