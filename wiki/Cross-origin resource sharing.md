# Cross-origin resource sharing

Cross‑origin resource sharing (CORS) est un mécanisme de sécurité qui permet à une page web d’accéder à des ressources protégées situées sur un serveur appartenant à un domaine différent de celui qui a servi la page. Alors que le même‑origine (same‑origin policy) interdit par défaut les requêtes HTTP « cross‑domain » telles que les appels Ajax, CORS offre une méthode standardisée pour que le navigateur et le serveur négocient l’autorisation d’accès. Ce protocole est plus permissif que le blocage complet, mais plus sûr que l’ouverture totale aux requêtes inter‑domaine.

## Principe de base

Les ressources pouvant être partagées sans restriction incluent les images, feuilles de style, scripts, iframes et vidéos. Pour les requêtes plus sensibles, comme celles effectuées par `XMLHttpRequest` ou `fetch`, le navigateur ajoute un en‑tête `Origin` indiquant le domaine d’origine. Le serveur répond avec des en‑têtes `Access‑Control‑Allow‑Origin` (et éventuellement d’autres) qui précisent les domaines autorisés, les méthodes HTTP acceptées et les en‑têtes personnalisés. Si la réponse du serveur ne contient pas les en‑têtes requis, le navigateur bloque la réponse côté client.

## Mécanisme de négociation

CORS repose sur un échange d’en‑têtes HTTP. Lorsqu’une requête simple (GET, HEAD, POST sans en‑têtes personnalisées) est envoyée, le navigateur vérifie immédiatement l’en‑tête `Access‑Control‑Allow‑Origin`. Pour les requêtes « complexes » (méthodes autres que GET/HEAD/POST, en‑têtes non standards, ou requêtes avec credentials), le navigateur effectue d’abord une requête préliminaire (preflight) en méthode `OPTIONS`. Le serveur doit alors répondre avec les en‑têtes `Access‑Control‑Allow‑Methods` et `Access‑Control‑Allow-Headers`. Ce processus garantit que le serveur a explicitement approuvé la requête avant que les données ne soient transférées.

## Sécurité et bonnes pratiques

CORS ne remplace pas l’authentification ou l’autorisation. Il ne suffit pas de déclarer un domaine autorisé ; le serveur doit également vérifier l’identité de l’utilisateur et les droits d’accès. Les développeurs doivent limiter les domaines autorisés à ceux réellement nécessaires, éviter d’utiliser le joker `*` lorsqu’ils souhaitent envoyer des cookies ou des informations d’authentification, et s’assurer que les réponses ne contiennent pas d’informations sensibles exposées à des tiers. La spécification actuelle est intégrée dans le Fetch Living Standard du WHATWG, tandis qu’une version antérieure a été publiée comme recommandation W3C.

## Voir aussi
[[Angular resolution (graph drawing)]], [[Chemical ecology]], [[Human behavioral ecology]], [[Cultural ecology]], [[Evolutionary developmental psychology]], [[Insects in ethics]]