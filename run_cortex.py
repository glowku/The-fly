#!/usr/bin/env python3
"""Point d'entrée unique pour GitHub Actions / local.

Modes:
  triage  — trie le graphe (quarantine, pas delete)
  skill   — skill_learn une note
  wiki    — auto_learn wiki insecte
  full    — triage + skill + wiki
  loop    — plusieurs cycles (comme run_auto_loop)
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import traceback


def main():
    p = argparse.ArgumentParser(description="The-fly cortex runner")
    p.add_argument(
        "--mode",
        choices=["triage", "skill", "wiki", "full", "loop"],
        default=os.environ.get("CORTEX_MODE", "full"),
    )
    p.add_argument("--cycles", type=int, default=int(os.environ.get("CORTEX_CYCLES", "8")))
    p.add_argument("--interval", type=int, default=int(os.environ.get("CORTEX_INTERVAL", "60")))
    p.add_argument("--max-minutes", type=int, default=int(os.environ.get("CORTEX_MAX_MIN", "40")))
    args = p.parse_args()

    from agent.auto_learn import run_auto_learn
    from agent.skill_learn import run_skill_learn
    from agent.triage import run_triage
    from agent.tools import git_commit_push

    print(f"[cortex] mode={args.mode} cycles={args.cycles}", flush=True)

    def push(msg: str, paths=None):
        try:
            git_commit_push(paths or ["state/", "skill_notes/", "wiki/", "DASHBOARD.md"], msg)
        except Exception as e:
            print(f"[cortex] push skip: {e}", flush=True)

    if args.mode == "triage":
        rep = run_triage(max_move=150)
        print(rep, flush=True)
        push(f"cortex triage: moved={rep.get('moved_to_quarantine')} active={rep.get('active_nodes')}")
        return 0

    if args.mode == "skill":
        sk = run_skill_learn()
        print(sk, flush=True)
        push(f"cortex skill: {sk.get('skill')} — {sk.get('topic')}")
        return 0

    if args.mode == "wiki":
        ok = run_auto_learn(mode="wiki")
        print(ok, flush=True)
        push("cortex wiki learn")
        return 0

    if args.mode == "full":
        rep = run_triage(max_move=120)
        print("[cortex] triage", rep, flush=True)
        sk = run_skill_learn()
        print("[cortex] skill", sk, flush=True)
        w = run_auto_learn(mode="wiki")
        print("[cortex] wiki", w, flush=True)
        push(
            f"cortex full: q={rep.get('moved_to_quarantine')} skill={sk.get('skill')} wiki={bool(w)}"
        )
        return 0

    # loop
    start = time.time()
    max_s = args.max_minutes * 60
    try:
        rep = run_triage(max_move=120)
        push(f"cortex loop triage: {rep.get('moved_to_quarantine')}")
    except Exception:
        traceback.print_exc()

    for i in range(1, args.cycles + 1):
        if time.time() - start > max_s:
            print("[cortex] max time", flush=True)
            break
        print(f"[cortex] cycle {i}/{args.cycles}", flush=True)
        try:
            run_auto_learn(mode=None)  # rotation skill/wiki/triage
        except Exception:
            traceback.print_exc()
        time.sleep(max(15, args.interval))

    push("cortex loop done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
