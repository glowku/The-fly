Live html:
https://glowku.github.io/The-fly/docs/fly-brain.html

[![GitHub All Releases](https://img.shields.io/github/downloads/glowku/The-fly/total?style=flat-square&logo=github)](https://github.com/glowku/The-fly/releases)
[![GitHub stars](https://img.shields.io/github/stars/glowku/The-fly?style=flat-square&logo=github)](https://github.com/glowku/The-fly/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/glowku/The-fly?style=flat-square&logo=github)](https://github.com/glowku/The-fly/network/members)

# 🪰 The Fly — Autonomous Knowledge Agent

> **Status : BETA** → passage en **ALPHA** prévu quand le graphe tient 50+ articles stables sans dérive hors-sujet.

**Un agent autonome** qui construit un **graphe de connaissance vivant** (wiki Markdown) à partir d’un sujet racine.  
Il perçoit, planifie, agit, évalue, se corrige — et commit le résultat.

Objectif mesurable : **maximiser `coverage × average_quality`**.

---

## Capacités actuelles

| Capacité | Détail |
|----------|--------|
| **Perception** | Wikipedia + recherche multi-mots |
| **arXiv** | `agent/arxiv_source.py` — papiers + concepts filtrés anti-dérive |
| **Mémoire** | coverage / quality / history / skills |
| **Anti-dérive v1** | `is_hard_junk` + score de résonance domaine |
| **Synthèse** | Groq + contexte arXiv optionnel |
| **Graph-RAG** | `agent/graph_rag.py` — réponses ancrées wiki (+ arXiv) |
| **Chat CLI** | `run_chat.py` |
| **Chat UI** | `docs/fly-brain.html` + `run_chat_server.py` |
| **Auto-learn** | voisinage graphe + Groq + **concepts arXiv** |

---

## Architecture

```
PERCEIVE (Wikipedia + arXiv)
   → PLAN (anti-dérive)
   → ACT (Groq synthèse)
   → EVALUATE
   → AUTO_LEARN / REPAIR
   → Graph-RAG chat (wiki noyau + papers)
```

---

## Secrets GitHub Actions

| Secret | Obligatoire |
|--------|-------------|
| `GROQ_API_KEY` | **Oui** |
| `PAT_TOKEN` (scope `repo`) | recommandé pour les push |

---

## Test local — tout le stack

```bash
git clone https://github.com/glowku/The-fly.git
cd The-fly
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export GROQ_API_KEY="gsk_..."                       # https://console.groq.com/keys
```

### 1) arXiv seul

```bash
python run_chat.py --arxiv-only "insect flight haltere"
python -c "from agent.arxiv_source import search_domain, concepts_from_papers as c; p=search_domain('drosophila wing',5); print(len(p), c(p)[:5])"
```

### 2) Graph-RAG (wiki + arXiv + LLM)

```bash
# une question
python run_chat.py "Comment les haltères stabilisent le vol des diptères ?"

# mode interactif
python run_chat.py

# retrieve only (pas de LLM)
python run_chat.py --retrieve-only "haltere" --k 8

# vérifier un claim
python run_chat.py --verify "Les haltères sont des ailes modifiées"

# JSON brut
python run_chat.py --json "pollination by hoverflies"
```

Sans `GROQ_API_KEY` → mode **extractif** (citations wiki uniquement).

### 3) Chat HTML (graphe + panneau)

Terminal A — API :

```bash
export GROQ_API_KEY="gsk_..."
python run_chat_server.py
# → http://127.0.0.1:8765
```

Terminal B — page :

```bash
# depuis la racine du repo
python -m http.server 8080
# ouvre http://127.0.0.1:8080/docs/fly-brain.html
```

Le panneau Chat utilise l’API locale si dispo, sinon mode extractif (GitHub Pages).

Pages live (extractif) : https://glowku.github.io/The-fly/docs/fly-brain.html

### 4) Agent (ne casse rien — dry-run d’abord)

```bash
python run.py --dry-run
python run.py
python -c "from agent.auto_learn import run_auto_learn; run_auto_learn()"
python -m agent.evaluate_dashboard
```

### 5) Endpoints API chat server

| Méthode | Path | Body / query |
|---------|------|----------------|
| GET | `/health` | — |
| POST | `/api/chat` | `{"question":"...","use_arxiv":true,"k":6}` |
| POST | `/api/verify` | `{"claim":"..."}` |
| GET | `/api/retrieve?q=...&k=6` | — |
| GET | `/api/arxiv?q=insect+flight` | — |

Exemple curl :

```bash
curl -s http://127.0.0.1:8765/api/chat \
  -H 'Content-Type: application/json' \
  -d '{"question":"rôle des haltères","use_arxiv":true}'
```

---

## Structure clé

```
agent/
  arxiv_source.py   # API arXiv Atom, concepts filtrés
  graph_rag.py      # retrieve + answer + verify_claim
  skills.py         # anti-dérive v1
  auto_learn.py     # pool + arXiv concepts
  synthesis.py      # Groq + contexte arXiv
docs/fly-brain.html # graphe + chatbot
run_chat.py
run_chat_server.py
run.py
```

---

## Licence

MIT.
