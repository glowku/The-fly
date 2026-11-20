"""Tests d'invariants non-régression — exécutés à chaque évolution."""
from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_coverage_json_valid():
    p = ROOT / "state" / "coverage.json"
    assert p.exists(), "coverage.json manquant"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "nodes" in data and isinstance(data["nodes"], dict)
    assert "edges" in data and isinstance(data["edges"], list)
    # aucun nœud vide
    for title in data["nodes"]:
        assert title and title.strip(), "nœud vide dans coverage"


def test_quality_json_valid():
    p = ROOT / "state" / "quality.json"
    assert p.exists(), "quality.json manquant"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_skills_json_valid():
    p = ROOT / "state" / "skills.json"
    assert p.exists(), "skills.json manquant"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    assert len(data) >= 1


def test_fly_brain_html_intact():
    p = ROOT / "docs" / "fly-brain.html"
    assert p.exists()
    html = p.read_text(encoding="utf-8")
    assert "<html" in html.lower()
    assert "<script" in html.lower()
    assert "fetch(" in html
    # balises non cassées grossièrement
    assert html.count("<div") >= html.count("</div") - 2


def test_protected_python_symbols():
    checks = {
        "agent/arxiv_source.py": ["search_domain", "concepts_from_papers"],
        "agent/auto_learn.py": ["run_auto_learn"],
        "agent/graph_rag.py": ["answer", "retrieve"],
        "agent/skill_learn.py": ["run_skill_learn"],
        "agent/skills.py": ["load_skills", "is_hard_junk"],
    }
    for rel, symbols in checks.items():
        content = (ROOT / rel).read_text(encoding="utf-8")
        tree = ast.parse(content)
        defined = {
            n.name
            for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        }
        for sym in symbols:
            assert sym in defined or sym in content, f"{sym} manquant dans {rel}"


def test_chat_server_endpoints_present():
    content = (ROOT / "run_chat_server.py").read_text(encoding="utf-8")
    for ep in ("/health", "/api/chat", "/api/retrieve", "/api/arxiv"):
        assert ep in content, f"endpoint {ep} manquant"


def test_import_core_modules():
    from agent.arxiv_source import search_domain  # noqa: F401
    from agent.graph_rag import retrieve  # noqa: F401
    from agent.skills import load_skills  # noqa: F401
    from agent.auto_learn import run_auto_learn  # noqa: F401
