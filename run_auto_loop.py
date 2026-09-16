#!/usr/bin/env python3
"""Lance auto_learn toutes les 15 secondes, indéfiniment."""
import time
import traceback
from agent.auto_learn import run_auto_learn

INTERVAL = 15  # secondes

if __name__ == "__main__":
    print(f"[loop] démarrage – cycle toutes les {INTERVAL}s")
    while True:
        try:
            run_auto_learn()
        except Exception as e:
            print(f"[loop] ERREUR: {e}")
            traceback.print_exc()
        print(f"[loop] sleep {INTERVAL}s …")
        time.sleep(INTERVAL)
