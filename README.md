Live html:
https://glowku.github.io/The-fly/docs/fly-brain.html

[![GitHub All Releases](https://img.shields.io/github/downloads/glowku/The-fly/total?style=flat-square&logo=github)](https://github.com/glowku/The-fly/releases)
[![GitHub stars](https://img.shields.io/github/stars/glowku/The-fly?style=flat-square&logo=github)](https://github.com/glowku/The-fly/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/glowku/The-fly?style=flat-square&logo=github)](https://github.com/glowku/The-fly/network/members)[![GitHub forks](https://img.shields.io/github/forks/glowku/The-fly?style=flat-square&logo=github)](https://github.com/glowku/The-fly/network/members)

# 🪰 The Fly — Autonomous Knowledge Agent

> **Status : BETA** → passage en **ALPHA** prévu quand le graphe tient 50+ articles stables sans dérive hors-sujet.

**Un agent autonome** qui construit un **graphe de connaissance vivant** (wiki Markdown) à partir d’un sujet racine.  
Ce n’est pas un bot de stats : il perçoit, planifie, agit, évalue, se corrige — et commit le résultat.

Objectif mesurable : **maximiser `coverage × average_quality`**.

---

## Nom du projet

Le dépôt s’appelle encore *The-fly*. Quelques pistes pour l’identité « produit » :

| Nom | Idée |
|-----|------|
| **FlyBrain** | cerveau de mouche + réseau de neurones du wiki |
| **Diptera** | ordre scientifique des mouches — sérieux, mémorable |
| **SwarmWiki** | essaim d’articles qui s’auto-organise |
| **GrokFly** | clin d’œil agentique (indépendant de xAI) |
| **Neural Fly** | nœuds = neurones, edges = synapses |
| **Haltere** | organe d’équilibre des diptères — l’agent « stabilise » le graphe |
| **MaggotMind** | un peu trash, très mème |
| **GraphLarva** | le graphe grandit par stades (larve → imago) |

**Recommandation :** **FlyBrain** (clair) ou **Haltere** (unique, scientifique).

---

## Ce qu’il sait faire (beta)

| Capacité | Détail |
|----------|--------|
| **Perception** | Wikipedia (summary + links + related) + **recherche multi-mots** (`resolve_title`, bigrams/trigrams) |
| **Mémoire** | `coverage.json`, `quality.json`, `history.jsonl`, `skills.json` |
| **Skills / « neurones »** | compétences (`entomologie`, `anatomie_insecte`, `vol_et_aerodynamique`…) renforcées à chaque article |
| **Planification** | priorité : repair → **feuilles sans enfants** → frontier → peu d’enfants |
| **Action** | synthèse Groq (modèle gratuit) + écriture `wiki/*.md` + commit |
| **Évaluation** | score 0–10 (longueur, structure, liens, diversité…) |
| **Auto-learn** | Groq propose des concepts par skill → **écrit 1 vrai article** + seed frontier |
| **Anti-doublon** | skip si déjà dans nodes/quality/frontier ou similarité ≥ 88 % |
| **Anti-dérive** | `score_relevance` + ban hors-sujet (ex. cybersecurity pure) |
| **Branch** | nœud solide sans enfants → découverte de sous-concepts **sans** réécriture |
| **Visualisation** | `docs/fly-brain.html` — graphe neural live, frontier grisée, lecture d’articles |

---

## Architecture

```
                    GOAL: max coverage × quality
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    PERCEIVE              PLAN                  ACT
    Wikipedia          value / leaf           Groq + git
    multi-search       frontier / skill       wiki/*.md
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                          EVALUATE
                         score 0–10
                              │
                              ▼
                    REFLECT / AUTO_LEARN
              repair · branch · skill seed · dedupe
                              │
                              ▼
                    DASHBOARD + fly-brain.html
```

---

## Démarrage rapide

### 1. Clé Groq (gratuit)

1. [console.groq.com/keys](https://console.groq.com/keys)  
2. **Create API Key** → `gsk_...`

### 2. Secrets GitHub

**Settings → Secrets and variables → Actions**

| Secret | Obligatoire |
|--------|-------------|
| `GROQ_API_KEY` | **Oui** |
| `PAT_TOKEN` (scope `repo`) | Fortement recommandé pour les push |

### 3. Premier cycle

1. **Actions → bootstrap → Run workflow**  
2. Sujet racine : idéalement un **vrai titre Wikipedia** (`Fly`, `Diptera`, `Ecology`)  
3. Puis **expand** / **auto_learn**

### 4. Workflows

| Workflow | Quand | Rôle |
|----------|--------|------|
| `bootstrap` | manuel | reset root + 1er article |
| `expand` | ~30 min | cycle Perceive→Plan→Act→Evaluate |
| `auto_learn` | ~3 h | skill faible → article réel + frontier |
| `repair` | ~6 h | corrige les scores faibles |
| `evaluate` | optionnel | rafraîchit `DASHBOARD.md` |

---

## Structure

```
The-fly/
├── .github/workflows/
│   ├── bootstrap.yml
│   ├── expand.yml
│   ├── auto_learn.yml
│   ├── repair.yml
│   └── evaluate.yml
├── agent/
│   ├── perception.py      # Wikipedia + multi_search + resolve
│   ├── planning.py        # leaf / frontier / repair
│   ├── synthesis.py       # Groq
│   ├── evaluation.py      # score 0–10
│   ├── skills.py          # neurones de compétence
│   ├── auto_learn.py      # apprentissage par skill
│   ├── repair.py
│   ├── memory.py
│   └── tools.py           # git add -A / rebase / push robuste
├── docs/
│   └── fly-brain.html     # UI graphe neural
├── wiki/                  # articles Markdown
├── state/
│   ├── coverage.json
│   ├── quality.json
│   ├── skills.json
│   ├── history.jsonl
│   └── goal.json
├── DASHBOARD.md
├── ROOT.txt
└── run.py
```

---

## Objectif & roadmap

**Objectif courant (beta)**  
Maximiser `coverage_factor × avg_quality` sans dérive thématique, avec des **sous-branches** sous chaque nœud feuille.

**Critères pour passer en ALPHA**

- [ ] ≥ 50 articles cohérents sur le sujet racine  
- [ ] auto_learn crée des articles utiles **sans** junk (Wing Chun, albums…)  
- [ ] push Actions stable (plus de non-fast-forward)  
- [ ] graphe HTML lisible (pas de labels empilés)  
- [ ] zéro hors-sujet récurrent dans `wiki/`

**Ensuite**

- source arXiv / actualité  
- multi-langue  
- chat via GitHub Issues  
- force-layout plus avancé dans fly-brain  

---

## Test local

```bash
export GROQ_API_KEY="gsk_..."
python run.py --dry-run
python run.py
python -c "from agent.auto_learn import run_auto_learn; run_auto_learn()"
python -m agent.evaluate_dashboard
```

Ouvre `docs/fly-brain.html` (ou GitHub Pages) pour le graphe live.

---

## Licence

MIT.

---

*Beta — agent autonome de connaissance, pas un bot de stats.*  
*Prochaine étape : **alpha**.*
