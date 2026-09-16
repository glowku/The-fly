#!/usr/bin/env python3
"""Boucle auto_learn toutes les 15 secondes (durée limitée pour GHA)."""
import os
import time
import traceback
from agent.auto_learn import run_auto_learn

INTERVAL = 15          # secondes
MAX_RUNTIME = 45 * 60  # 45 minutes max (pour GHA)

def main():
    start = time.time()
    print(f"[loop] démarrage – cycle toutes les {INTERVAL}s (max {MAX_RUNTIME//60} min)")
    cycle = 0
    while True:
        if time.time() - start > MAX_RUNTIME:
            print("[loop] temps max atteint → arrêt propre")
            break
        cycle += 1
        print(f"\n[loop] ===== cycle {cycle} =====")
        try:
            run_auto_learn()
        except Exception as e:
            print(f"[loop] ERREUR cycle {cycle}: {e}")
            traceback.print_exc()
        print(f"[loop] sleep {INTERVAL}s …")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
