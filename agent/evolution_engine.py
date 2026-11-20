"""Moteur d'évolution testée avec rollback automatique et récompenses.

Ne modifie jamais les modules existants. Snapshot → mutation → tests →
commit + reward OU rollback + pénalité. Protège les contrats critiques.
"""
from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / "state"
CHECKPOINT_DIR = STATE_DIR / "checkpoints"
EVO_STATE_FILE = STATE_DIR / "evolution_state.json"

# Fichiers / dossiers surveillés avant chaque évolution
TRACKED_PATHS = [
    "state",
    "skill_notes",
    "wiki",
    "docs/fly-brain.html",
]

# Contrat STRICT : symboles / endpoints / balises qui ne doivent jamais disparaître
PROTECTED_CONTRACTS = {
    "agent/arxiv_source.py": ["search_domain", "concepts_from_papers"],
    "agent/auto_learn.py": ["run_auto_learn"],
    "agent/graph_rag.py": ["answer", "retrieve"],
    "agent/skill_learn.py": ["run_skill_learn"],
    "agent/skills.py": ["load_skills", "is_hard_junk", "score_relevance"],
    "run_chat_server.py": ["/health", "/api/chat", "/api/retrieve", "/api/arxiv"],
    "docs/fly-brain.html": ["<html", "<script", "fetch("],
}


@dataclass
class EvolutionRecord:
    generation: int
    timestamp: float
    action: str
    skill_used: str
    status: str  # COMMITTED | ROLLED_BACK
    reward: float
    total_reward: float
    metrics_before: Dict[str, float]
    metrics_after: Dict[str, float]
    error: str = ""
    checkpoint_id: str = ""


class EvolutionEngine:
    def __init__(self) -> None:
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if EVO_STATE_FILE.exists():
            try:
                return json.loads(EVO_STATE_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        return {
            "generation": 0,
            "total_reward": 0.0,
            "last_good_checkpoint": None,
            "skills": {},
            "history": [],
            "forbidden_mutations": [],
        }

    def save_state(self) -> None:
        EVO_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        EVO_STATE_FILE.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    # ------------------------------------------------------------------
    # 1. SNAPSHOT ATOMIQUE
    # ------------------------------------------------------------------
    def create_checkpoint(self, label: str = "auto") -> str:
        ckpt_id = f"gen_{self.state['generation']:04d}_{int(time.time())}_{label}"
        dest = CHECKPOINT_DIR / ckpt_id
        dest.mkdir(parents=True, exist_ok=True)

        for rel in TRACKED_PATHS:
            src = ROOT / rel
            if not src.exists():
                continue
            target = dest / rel
            if src.is_dir():
                ignore = shutil.ignore_patterns("checkpoints", "__pycache__", "*.pyc")
                shutil.copytree(src, target, dirs_exist_ok=True, ignore=ignore)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
        return ckpt_id

    # ------------------------------------------------------------------
    # 2. ROLLBACK
    # ------------------------------------------------------------------
    def rollback(self, ckpt_id: str | None = None) -> bool:
        ckpt_id = ckpt_id or self.state.get("last_good_checkpoint")
        if not ckpt_id:
            return False
        src_root = CHECKPOINT_DIR / ckpt_id
        if not src_root.exists():
            return False

        for rel in TRACKED_PATHS:
            backup = src_root / rel
            live = ROOT / rel
            if not backup.exists():
                continue
            if backup.is_dir():
                for item in backup.rglob("*"):
                    if item.is_file():
                        rel_item = item.relative_to(backup)
                        dst = live / rel_item
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dst)
            else:
                live.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup, live)
        return True

    # ------------------------------------------------------------------
    # 3. GARDE-FOU CONTRATS
    # ------------------------------------------------------------------
    def verify_protected_contracts(self) -> List[str]:
        errors: List[str] = []
        for rel_path, required_tokens in PROTECTED_CONTRACTS.items():
            p = ROOT / rel_path
            if not p.exists():
                errors.append(f"Fichier critique manquant: {rel_path}")
                continue
            content = p.read_text(encoding="utf-8", errors="ignore")

            if rel_path.endswith(".py"):
                try:
                    tree = ast.parse(content)
                    defined = {
                        node.name
                        for node in ast.walk(tree)
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                    }
                    for tok in required_tokens:
                        if not tok.startswith("/") and tok not in defined and tok not in content:
                            errors.append(f"Fonction/symbole supprimé dans {rel_path}: {tok}")
                except SyntaxError as exc:
                    errors.append(f"Erreur de syntaxe Python dans {rel_path}: {exc}")

            for tok in required_tokens:
                if tok not in content:
                    errors.append(f"Élément protégé effacé dans {rel_path}: {tok}")

        return errors

    # ------------------------------------------------------------------
    # 4. SUITE DE TESTS
    # ------------------------------------------------------------------
    def run_evolution_tests(self) -> tuple[bool, str]:
        contract_errors = self.verify_protected_contracts()
        if contract_errors:
            return False, " | ".join(contract_errors)

        tests_dir = ROOT / "tests"
        if tests_dir.exists():
            try:
                proc = subprocess.run(
                    ["python", "-m", "pytest", "-q", "tests/"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=90,
                )
                if proc.returncode != 0:
                    return False, f"Tests échoués:\n{proc.stdout}\n{proc.stderr}"
            except FileNotFoundError:
                # pytest non installé → smoke seulement
                pass
            except subprocess.TimeoutExpired:
                return False, "Timeout pytest"

        smoke = subprocess.run(
            [
                "python",
                "-c",
                (
                    "from agent.arxiv_source import search_domain; "
                    "from agent.graph_rag import retrieve; "
                    "from agent.auto_learn import run_auto_learn; "
                    "from agent.skills import load_skills; "
                    "print('OK')"
                ),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=45,
        )
        if smoke.returncode != 0:
            return False, f"Smoke import échoué: {smoke.stderr}"

        return True, "ALL_TESTS_PASSED"

    # ------------------------------------------------------------------
    # 5. MÉTRIQUES & RÉCOMPENSE
    # ------------------------------------------------------------------
    @staticmethod
    def measure_metrics() -> Dict[str, float]:
        """Mesure coverage × quality + connexité du graphe."""
        from agent.memory import load_coverage, load_quality, compute_objective_score

        cov = load_coverage()
        qual = load_quality()
        nodes = cov.get("nodes") or {}
        edges = cov.get("edges") or []

        obj, n_nodes, avg_q = compute_objective_score()

        # Composantes connexes (BFS non-orienté)
        adj: Dict[str, set] = {n: set() for n in nodes}
        for e in edges:
            a, b = e.get("from"), e.get("to")
            if a in adj and b in adj:
                adj[a].add(b)
                adj[b].add(a)

        visited: set = set()
        components = 0
        orphans = 0
        for n in nodes:
            deg = len(adj.get(n, ()))
            if deg == 0:
                orphans += 1
            if n in visited:
                continue
            components += 1
            stack = [n]
            visited.add(n)
            while stack:
                cur = stack.pop()
                for nxt in adj.get(cur, ()):
                    if nxt not in visited:
                        visited.add(nxt)
                        stack.append(nxt)

        # Ponts inter-skills approximés via densify keywords
        bridges = 0
        try:
            from agent.densify import _skill_of

            for e in edges:
                a, b = e.get("from"), e.get("to")
                if a in nodes and b in nodes:
                    if _skill_of(a) != _skill_of(b):
                        bridges += 1
        except Exception:
            pass

        return {
            "coverage": float(n_nodes),
            "average_quality": float(avg_q),
            "objective": float(obj),
            "nodes_count": float(n_nodes),
            "edges_count": float(len(edges)),
            "connected_components": float(max(components, 1)),
            "orphans": float(orphans),
            "bridges": float(bridges),
        }

    @staticmethod
    def compute_reward(
        before: Dict[str, float], after: Dict[str, float], passed: bool
    ) -> float:
        if not passed:
            return -5.0

        score_before = before.get("coverage", 0.0) * before.get("average_quality", 0.0)
        score_after = after.get("coverage", 0.0) * after.get("average_quality", 0.0)
        delta_quality = (score_after - score_before) * 0.01  # scale down (scores already large)

        comp_before = before.get("connected_components", 1)
        comp_after = after.get("connected_components", 1)
        connectivity_bonus = max(0.0, (comp_before - comp_after) * 1.5)

        orphans_delta = max(0.0, before.get("orphans", 0) - after.get("orphans", 0)) * 0.3
        new_nodes = max(0.0, after.get("nodes_count", 0) - before.get("nodes_count", 0)) * 0.4
        new_edges = max(0.0, after.get("edges_count", 0) - before.get("edges_count", 0)) * 0.05

        return round(1.0 + delta_quality + connectivity_bonus + orphans_delta + new_nodes + new_edges, 3)

    # ------------------------------------------------------------------
    # 6. BOUCLE SNAPSHOT → MUTATE → TEST → COMMIT / ROLLBACK
    # ------------------------------------------------------------------
    def evolve_step(
        self,
        action_name: str,
        skill_used: str,
        mutate_fn: Callable[[], None],
        measure_fn: Callable[[], Dict[str, float]] | None = None,
    ) -> EvolutionRecord:
        measure = measure_fn or self.measure_metrics
        metrics_before = measure()
        ckpt_id = self.create_checkpoint(label=skill_used.replace(" ", "_")[:32])

        error_msg = ""
        passed = False
        metrics_after = metrics_before

        try:
            mutate_fn()
            metrics_after = measure()
            passed, test_msg = self.run_evolution_tests()
            if not passed:
                error_msg = test_msg
        except Exception as exc:
            passed = False
            error_msg = f"Exception durant l'évolution: {exc}"

        if not passed:
            self.rollback(ckpt_id)
            metrics_after = measure()
            reward = self.compute_reward(metrics_before, metrics_after, passed=False)
            status = "ROLLED_BACK"
            self.state["forbidden_mutations"].append(
                {"action": action_name, "error": error_msg[:240], "ts": time.time()}
            )
            self.state["forbidden_mutations"] = self.state["forbidden_mutations"][-50:]
        else:
            reward = self.compute_reward(metrics_before, metrics_after, passed=True)
            status = "COMMITTED"
            self.state["generation"] += 1
            self.state["last_good_checkpoint"] = ckpt_id

        sk = self.state["skills"].setdefault(
            skill_used,
            {
                "level": 1,
                "reward": 0.0,
                "successes": 0,
                "failures": 0,
                "linked_nodes": [],
            },
        )
        sk["reward"] = round(sk["reward"] + reward, 3)
        if status == "COMMITTED":
            sk["successes"] += 1
            sk["level"] = 1 + sk["successes"] // 3
        else:
            sk["failures"] += 1

        self.state["total_reward"] = round(self.state["total_reward"] + reward, 3)

        rec = EvolutionRecord(
            generation=self.state["generation"],
            timestamp=time.time(),
            action=action_name,
            skill_used=skill_used,
            status=status,
            reward=reward,
            total_reward=self.state["total_reward"],
            metrics_before=metrics_before,
            metrics_after=metrics_after,
            error=error_msg[:300],
            checkpoint_id=ckpt_id,
        )
        self.state["history"].append(asdict(rec))
        self.state["history"] = self.state["history"][-100:]
        self.save_state()
        return rec

    def status(self) -> Dict[str, Any]:
        metrics = self.measure_metrics()
        return {
            "generation": self.state.get("generation", 0),
            "total_reward": self.state.get("total_reward", 0.0),
            "last_good_checkpoint": self.state.get("last_good_checkpoint"),
            "skills": self.state.get("skills", {}),
            "history": self.state.get("history", [])[-20:],
            "forbidden_mutations": self.state.get("forbidden_mutations", [])[-10:],
            "metrics": metrics,
        }

    def run_safe_cycle(self, mode: str | None = None) -> EvolutionRecord:
        """Cycle d'évolution sûr : densify + auto_learn/skill sous protection."""

        def mutate():
            from agent.densify import densify_edges
            from agent.auto_learn import run_auto_learn
            from agent.skill_learn import run_skill_learn

            densify_edges(max_new=25)
            if mode == "skill":
                run_skill_learn()
            elif mode == "wiki":
                run_auto_learn(mode="wiki")
            else:
                run_auto_learn(mode=mode)

        skill = mode or "cortex_cycle"
        return self.evolve_step(
            action_name=f"safe_cycle:{mode or 'auto'}",
            skill_used=skill,
            mutate_fn=mutate,
        )
