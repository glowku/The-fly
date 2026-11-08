---
skill: securite_defensive
topic: secure coding basics input validation
created: 2026-11-08T09:54:23.420847+00:00
---

## Contexte  
Les applications modernes reçoivent des données de sources variées : formulaires web, API, fichiers, services tiers.  
Sans validation stricte, ces entrées peuvent introduire des attaques : injection SQL, XSS, path traversal, etc.  
Le principe de la sécurité défensive consiste à *défendre* l’application dès le premier point d’entrée, en supposant que toute donnée est potentiellement malveillante.  

## Méthode  
1. **Définir un schéma d’entrée**  
   - Liste des champs attendus, types, longueurs, formats (regex).  
   - Utiliser des bibliothèques de validation (ex. `express-validator`, `Joi`, `pydantic`).  

2. **Appliquer la validation en amont**  
   - Middleware ou interceptor avant toute logique métier.  
   - Refuser immédiatement toute requête qui ne correspond pas au schéma.  

3. **Sanitiser les données**  
   - Échapper les caractères spéciaux dans les champs destinés à la base de données ou au rendu HTML.  
   - Utiliser des fonctions natives (`htmlspecialchars`, `mysqli_real_escape_string`, `PreparedStatement`).  

4. **Limiter les privilèges**  
   - Ne pas stocker les données non nécessaires.  
   - Restreindre les champs autorisés à la mise à jour (whitelisting).  

5. **Surveiller et logger**  
   - Enregistrer les tentatives de validation échouées avec IP, timestamp, champ concerné.  
   - Aligner les logs avec un SIEM pour détection d’anomalies.  

## Pièges  
- **Validation côté client uniquement** : les utilisateurs peuvent désactiver JavaScript ou envoyer des requêtes directes.  
- **Schémas trop permissifs** : accepter des longueurs excessives ou des formats trop généraux ouvre la porte aux attaques de buffer overflow ou de DoS.  
- **Échappement double** : appliquer l’échappement à la fois côté serveur et côté client peut masquer des vulnérabilités.  
- **Mise à jour manuelle des schémas** : oublier de synchroniser les schémas entre services expose des failles.  
- **Ignorer les métadonnées** : les en-têtes HTTP, les cookies, les paramètres de requête doivent aussi être validés.  

## Checklist  
| Étape | Action | Outil / Exemple | Vérification |
|-------|--------|-----------------|--------------|
| 1 | Définir schéma | `Joi.object({email: Joi.string().email().required(), age: Joi.number().integer().min(0)})` | Schéma complet, sans champs optionnels inutiles |
| 2 | Middleware de validation | `app.use(validateInput)` | Refus immédiat des requêtes non conformes |
| 3 | Sanitisation | `htmlspecialchars($input)` | Aucun caractère spécial non échappé |
| 4 | Prepared statements | `$stmt = $pdo->prepare('INSERT INTO users (email) VALUES (?)')` | Pas de concaténation SQL |
| 5 | Logging | `log('validation_failed', ['ip'=>$_SERVER['REMOTE_ADDR'], 'field'=>$field])` | Logs stockés dans un fichier sécurisé |
| 6 | Tests | `curl -X POST -d 'email=bad' http://app` | Réponse 400, pas de fuite d’erreur détaillée |
| 7 | Surveillance | SIEM alert sur 10 échecs en 5 min | Alertes configurées, escalades définies |

**Lien agents autonomes / graphes**  
- Un *agent de validation* peut être modélisé comme un nœud dans un graphe de services.  
- Chaque nœud possède un *profil de schéma* (graph node) et un *policy graph* décrivant les dépendances.  
- L’agent interroge le *policy graph* pour récupérer le schéma actuel, applique la validation, puis transmet le résultat au nœud suivant.  
- En cas d’échec, l’agent déclenche un *workflow de mitigation* (bloquer IP, notifier l’équipe).  

En appliquant systématiquement ces étapes, vous transform
