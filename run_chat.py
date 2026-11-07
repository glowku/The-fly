#!/usr/bin/env python3
"""CLI Graph-RAG The-fly — interroge le noyau wiki (+ arXiv) via Groq."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agent.graph_rag import answer, retrieve, verify_claim
from agent.arxiv_source import search_domain


def main():
    p = argparse.ArgumentParser(description="The-fly Graph-RAG chat")
    p.add_argument("question", nargs="*", help="Question (sinon mode interactif)")
    p.add_argument("--no-arxiv", action="store_true")
    p.add_argument("--k", type=int, default=6)
    p.add_argument("--verify", action="store_true", help="Mode vérification de claim")
    p.add_argument("--json", action="store_true")
    p.add_argument("--retrieve-only", action="store_true")
    p.add_argument("--arxiv-only", action="store_true")
    args = p.parse_args()

    q = " ".join(args.question).strip()
    if args.arxiv_only:
        topic = q or "insect flight diptera"
        papers = search_domain(topic, max_results=8)
        print(json.dumps(papers, ensure_ascii=False, indent=2) if args.json else "\n".join(
            f"- {p['title']} [{p.get('published')}] {p.get('url')}" for p in papers
        ))
        return

    if not q:
        print("The-fly Graph-RAG — tape une question (Ctrl+C pour quitter)")
        while True:
            try:
                q = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not q:
                continue
            _run(q, args)
        return

    _run(q, args)


def _run(q, args):
    if args.retrieve_only:
        docs = retrieve(q, k=args.k)
        if args.json:
            print(json.dumps(docs, ensure_ascii=False, indent=2))
        else:
            for d in docs:
                print(f"[{d['score']}] {d['title']} (q={d.get('quality')})")
        return

    if args.verify:
        res = verify_claim(q, k=args.k)
    else:
        res = answer(q, k=args.k, use_arxiv=not args.no_arxiv)

    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    print("\n" + res.get("answer", ""))
    print("\n--- sources wiki ---")
    for s in res.get("sources") or []:
        print(f"  · {s}")
    if res.get("arxiv"):
        print("--- arXiv ---")
        for a in res["arxiv"][:4]:
            print(f"  · {a.get('title')} — {a.get('url')}")
    print(f"mode={res.get('mode')} model={res.get('model')}")


if __name__ == "__main__":
    main()
