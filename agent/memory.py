"""Mémoire persistante : coverage, quality, history, goal tracking."""
import json
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path("state")
STATE_DIR.mkdir(exist_ok=True)

COVERAGE = STATE_DIR / "coverage.json"
QUALITY = STATE_DIR / "quality.json"
HISTORY = STATE_DIR / "history.jsonl"
GOAL = STATE_DIR / "goal.json"


def _now():
    return datetime.now(timezone.utc).isoformat()


def _read_root_file():
    root_file = Path("ROOT.txt")
    if root_file.exists():
        return root_file.read_text(encoding="utf-8").strip() or "Fly"
    return "Fly"


def load_coverage():
    if COVERAGE.exists():
        try:
            data = json.loads(COVERAGE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[memory] coverage.json corrompu → backup + reset minimal: {e}", flush=True)
            COVERAGE.rename(COVERAGE.with_suffix(".json.bak"))
            data = {"root": _read_root_file(), "nodes": {}, "edges": [], "frontier": [], "max_depth": 0}
        data.setdefault("root", "Fly")
        data.setdefault("nodes", {})
        data.setdefault("edges", [])
        data.setdefault("frontier", [])
        data.setdefault("max_depth", 0)
        return data
    return {
        "root": _read_root_file(),
        "nodes": {},
        "edges": [],
        "frontier": [],
        "max_depth": 0,
    }


def save_coverage(cov):
    COVERAGE.write_text(json.dumps(cov, indent=2, ensure_ascii=False), encoding="utf-8")


def load_quality():
    if QUALITY.exists():
        return json.loads(QUALITY.read_text(encoding="utf-8"))
    return {}


def save_quality(q):
    QUALITY.write_text(json.dumps(q, indent=2, ensure_ascii=False), encoding="utf-8")


def load_goal():
    if GOAL.exists():
        return json.loads(GOAL.read_text(encoding="utf-8"))
    return {
        "objective": "maximize coverage × average_quality",
        "target_nodes": 200,
        "target_avg_quality": 7.5,
        "started_at": _now(),
    }


def save_goal(g):
    GOAL.write_text(json.dumps(g, indent=2, ensure_ascii=False), encoding="utf-8")


def log_event(event_type, payload):
    entry = {"ts": _now(), "type": event_type, **payload}
    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_history(limit=None):
    if not HISTORY.exists():
        return []
    lines = HISTORY.read_text(encoding="utf-8").strip().splitlines()
    if limit:
        lines = lines[-limit:]
    return [json.loads(l) for l in lines if l.strip()]


def compute_objective_score():
    cov = load_coverage()
    qual = load_quality()
    n_nodes = len(cov.get("nodes", {}))
    avg_q = sum(q.get("score", 0) for q in qual.values()) / max(len(qual), 1)
    coverage_factor = min(n_nodes / 50.0, 4.0)
    return round(coverage_factor * avg_q, 3), n_nodes, round(avg_q, 2)


def reset_for_new_root(root: str):
    """Réinitialise le graphe pour un nouveau sujet racine."""
    cov = {
        "root": root,
        "nodes": {},
        "edges": [],
        "frontier": [],
        "max_depth": 0,
    }
    save_coverage(cov)
    save_quality({})
    Path("ROOT.txt").write_text(root + "\n", encoding="utf-8")
    log_event("reset_root", {"root": root})
    return cov
