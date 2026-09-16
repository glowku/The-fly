#!/usr/bin/env python3
"""Boucle auto_learn (durée limitée pour GHA)."""
import time
import traceback
from agent.auto_learn import run_auto_learn

INTERVAL = 90          # secondes (évite rate-limit Groq + conflits git)
MAX_RUNTIME = 45 * 60  # 45 minutes max


def main():
    start = time.time()
    print(
        f"[loop] démarrage – cycle toutes les {INTERVAL}s "
        f"(max {MAX_RUNTIME // 60} min)",
        flush=True,
    )
    cycle = 0
    while True:
        if time.time() - start > MAX_RUNTIME:
            print("[loop] temps max atteint → arrêt propre", flush=True)
            break
        cycle += 1
        print(f"\n[loop] ===== cycle {cycle} =====", flush=True)
        try:
            run_auto_learn()
        except Exception as e:
            print(f"[loop] ERREUR cycle {cycle}: {e}", flush=True)
            traceback.print_exc()
        print(f"[loop] sleep {INTERVAL}s …", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
