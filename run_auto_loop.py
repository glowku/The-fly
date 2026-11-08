#!/usr/bin/env python3
"""Boucle auto_learn + triage (durée limitée pour GHA)."""
import time
import traceback
from agent.auto_learn import run_auto_learn
from agent.triage import run_triage
from agent.tools import git_commit_push

INTERVAL = 90
MAX_RUNTIME = 45 * 60


def main():
    start = time.time()
    print(f"[loop] start interval={INTERVAL}s max={MAX_RUNTIME // 60}min", flush=True)

    # Triage initial — trie, n'efface pas
    try:
        rep = run_triage(max_move=120)
        print(f"[loop] triage initial: {rep}", flush=True)
        try:
            git_commit_push(
                ["state/"],
                f"triage: q={rep.get('moved_to_quarantine')} active={rep.get('active_nodes')} dedup={rep.get('deduped')}",
            )
        except Exception as e:
            print(f"[loop] triage push skip: {e}", flush=True)
    except Exception as e:
        print(f"[loop] triage error: {e}", flush=True)
        traceback.print_exc()

    cycle = 0
    while True:
        if time.time() - start > MAX_RUNTIME:
            print("[loop] max runtime → stop", flush=True)
            break
        cycle += 1
        print(f"\n[loop] ===== cycle {cycle} =====", flush=True)
        try:
            # None = rotation skill/wiki/triage dans auto_learn
            run_auto_learn(mode=None)
        except Exception as e:
            print(f"[loop] ERREUR cycle {cycle}: {e}", flush=True)
            traceback.print_exc()
        print(f"[loop] sleep {INTERVAL}s", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
