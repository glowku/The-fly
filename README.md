# 🪰 The Fly — Autonomous Knowledge Agent

**Un vrai agent autonome** qui construit progressivement un **graphe de connaissance vivant** (wiki Markdown) à partir d'un sujet racine.

Il possède :
- **Perception** (Wikipedia REST API)
- **Mémoire persistante** (coverage + quality + history)
- **Planification par valeur** (trous dans le graphe + qualité faible + centralité)
- **Action** (synthèse via Groq LLM gratuit + commit git)
- **Évaluation multi-critères** de son propre output (score 0-10)
- **Réflexion / auto-correction** (repair, liens cassés, orphelins)

Objectif mesurable : **maximiser `coverage_factor × average_quality`**.

---

## Architecture

```
┌──────────────────────────────────────┐
│ GOAL                                 │
│ maximize coverage × quality          │
└──────────────┬───────────────────────┘
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
┌─────────┐ ┌──────────┐ ┌──────────┐
│PERCEIVE │─▶│ PLAN    │─▶│ ACT     │
│Wikipedia│ │value gap │ │ LLM+git │
└─────────┘ └──────────┘ └────┬─────┘
                              │
                              ▼
                        ┌──────────┐
                        │ EVALUATE │
                        │score 0-10│
                        └────┬─────┘
                             │
                             ▼
                      ┌───────────────┐
                      │ REFLECT       │
                      │repair / delete│
                      │update dash    │
                      └───────────────┘
```

---

## Démarrage rapide (5 minutes)

### 1. Créer la clé Groq (gratuit)

1. Va sur [https://console.groq.com/keys](https://console.groq.com/keys)
2. Crée un compte (Google / GitHub)
3. **Create API Key** → copie la clé `gsk_...`

### 2. Créer le dépôt GitHub

```bash
# Depuis le dossier parent
cd the-fly-autonomous-worker
git init
git add -A
git commit -m "🪰 init: the-fly autonomous knowledge agent"
gh repo create the-fly-autonomous-worker --public --source=. --remote=origin --push
```

Ou pousse manuellement vers ton repo existant.

### 3. Secrets GitHub

Dans ton repo → **Settings → Secrets and variables → Actions** :

| Secret          | Valeur                          | Obligatoire |
|-----------------|---------------------------------|-------------|
| `GROQ_API_KEY`  | ta clé `gsk_...`                | **Oui**     |
| `PAT_TOKEN`     | Personal Access Token (repo)    | Recommandé* |

\* `PAT_TOKEN` (scope `repo`) est recommandé pour que les workflows puissent push correctement. Sinon `GITHUB_TOKEN` est utilisé en fallback.

```bash
gh secret set GROQ_API_KEY
# colle ta clé
```

### 4. Lancer le premier cycle

1. Onglet **Actions**
2. Workflow **bootstrap**
3. **Run workflow** → choisis le sujet racine (ex: `Fly`, `Artificial intelligence`, `Cybersecurity`)
4. Attends 1-2 minutes

Tu verras apparaître :
- le premier article dans `wiki/`
- la mise à jour de `DASHBOARD.md`
- les premiers événements dans `state/history.jsonl`

### 5. Laisser tourner

Les workflows planifiés prennent le relais :

| Workflow   | Fréquence     | Rôle                          |
|------------|---------------|-------------------------------|
| `expand`   | toutes les 30 min | Ajoute / enrichit un article |
| `repair`   | toutes les 6 h    | Corrige les articles faibles |
| `evaluate` | toutes les 2 h    | Rafraîchit le dashboard      |

---

## Structure du projet

```
the-fly-autonomous-worker/
├── .github/workflows/
│   ├── expand.yml      # cycle principal
│   ├── repair.yml      # auto-correction
│   ├── evaluate.yml    # dashboard
│   └── bootstrap.yml   # premier lancement
├── agent/
│   ├── memory.py       # état persistant + score objectif
│   ├── perception.py   # Wikipedia (summary, links, related, categories)
│   ├── planning.py     # sélection par valeur attendue
│   ├── synthesis.py    # génération via Groq (llama-3.3-70b)
│   ├── evaluation.py   # score multi-critères 0-10
│   ├── repair.py       # repair + orphelins + liens cassés
│   ├── tools.py        # git + écriture
│   └── evaluate_dashboard.py
├── wiki/               # articles Markdown générés
├── state/
│   ├── coverage.json   # nœuds + arêtes + frontière
│   ├── quality.json    # scores par article
│   ├── history.jsonl   # log append-only de toutes les actions
│   └── goal.json       # cibles de l'objectif
├── DASHBOARD.md        # métriques publiques (auto-généré)
├── ROOT.txt            # sujet racine
├── run.py              # point d'entrée du cycle
├── requirements.txt
└── README.md
```

---

## Ce qui rend l'agent intelligent (v1.1)

| Capacité              | Implémentation |
|-----------------------|----------------|
| Perception            | Wikipedia REST (summary + links + related + categories) |
| Mémoire               | coverage / quality / history / goal persistants |
| Planification         | Score de priorité = qualité faible + trou frontière + centralité estimée + profondeur |
| Action                | Synthèse structurée + découverte de liens + commit |
| Évaluation            | 6 critères (longueur, structure, liens, diversité, propreté, H1) → score 0-10 |
| Réflexion             | Repair des scores < seuil, promotion des liens cassés en frontière, suppression orphelins |
| Objectif mesurable    | `coverage_factor × avg_quality` visible dans le dashboard |
| Auto-correction       | Boucle repair toutes les 6 h |

Le commit n'est **pas** l'objectif : c'est la conséquence de l'activité de l'agent.

---

## Tester en local

```bash
export GROQ_API_KEY="gsk_..."
python run.py --dry-run     # un cycle sans commit
python run.py               # un cycle réel (si git configuré)
python -m agent.evaluate_dashboard
```

---

## Après 24 h / 1 semaine

- ~40-50 articles (selon rate limits Groq)
- Frontière de plusieurs centaines de concepts
- Dashboard public avec top articles, répartition qualité, historique
- Historique git lisible avec messages significatifs (`wiki: Title (score X.XX)`)

---

## Améliorations possibles (prochaines versions)

- Source arXiv pour les sujets scientifiques
- Veille Hacker News / actualité
- Mode multilingue (EN / ES)
- Interaction via GitHub Issues (« pose une question à l'agent »)
- Visualisation du graphe (Mermaid / D3)

---

## Licence

MIT — fais-en ce que tu veux.

---

*Construit pour être un agent, pas un bot de stats.*
