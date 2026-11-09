---
skill: recherche_web
title: Multi-Turn Agentic Scientific Literature Search via Workflow Induction
source: arxiv
url: https://arxiv.org/abs/2607.00597v2
created: 2026-11-09T20:35:45.216964+00:00
---

# Multi-Turn Agentic Scientific Literature Search via Workflow Induction

## Source
arXiv — https://arxiv.org/abs/2607.00597v2

## Abstract
Scientific literature search often requires more than retrieving papers from a single query: users' intents are underspecified, preference-dependent, and evolve through interaction. Existing search agents typically rely on fixed pipelines or implicit language-only reasoning, making their search strategies difficult to control, inspect, and refine. We introduce PaperPilot, a multi-turn literature search agent that frames scientific search as workflow induction. Given an anchor paper and a user query, PaperPilot constructs an executable DAG of paper-search operators, including keyword search, citation expansion, filtering, scoring, reranking, and evidence extraction. User feedback is then used to refine both the query and the workflow itself. We train PaperPilot with supervised workflow imitation and preference optimization over controlled workflow corruptions. Experiments show that PaperPilot-9B improves over the base Qwen3.5-9B toolset agent under multi-turn interaction, increasing Hit@5 from 58.0 to 77.0, MRR from 47.5 to 59.4, and nDCG@10 from 26.8 to 32.5, while reducing workflow execution errors from 9.5% to 0%. These results show that explicit, editable search workflows provide an effective and controllable interface for aligning literature search agents with complex scientific intent.

## Extraction pour skill `recherche_web`
- Concepts à retenir pour l'agent The-fly (architecture, sécu, retrieval, graphe).
- Ne pas traiter l'abstract comme un tutoriel offensif.
