#!/usr/bin/env python3
"""Serveur local The-fly : chat + act (learn / triage / skill)."""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from agent.graph_rag import answer, retrieve
from agent.arxiv_source import search_domain
from agent.auto_learn import run_auto_learn
from agent.skill_learn import run_skill_learn
from agent.triage import run_triage
from agent.identity import skill_boost_answer
from agent.skills import get_skills_summary, load_skills

PORT = 8765


class Handler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        qs = parse_qs(urlparse(self.path).query)
        if path in ("/", "/health"):
            return self._json(200, {
                "ok": True,
                "service": "the-fly-cortex",
                "port": PORT,
                "actions": ["chat", "learn", "skill", "triage", "act"],
            })
        if path == "/api/skills":
            return self._json(200, {"skills": get_skills_summary(), "raw": {k: {"level": v.get("level"), "n": len(v.get("articles") or [])} for k, v in load_skills().items()}})
        if path == "/api/retrieve":
            q = (qs.get("q") or [""])[0]
            k = int((qs.get("k") or ["6"])[0])
            return self._json(200, {"docs": retrieve(q, k=k)})
        if path == "/api/arxiv":
            q = (qs.get("q") or ["insect flight"])[0]
            return self._json(200, {"papers": search_domain(q, max_results=6)})
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return self._json(400, {"error": "invalid json"})

        if path == "/api/chat":
            q = (data.get("question") or data.get("q") or "").strip()
            if not q:
                return self._json(400, {"error": "question required"})
            # intent act depuis le chat
            low = q.lower()
            if any(x in low for x in ("triage", "purge", "nettoie le graphe", "trie les nœuds", "trie les noeuds")):
                rep = run_triage(max_move=int(data.get("max_move") or 80))
                return self._json(200, {
                    "answer": (
                        f"Triage fait (tri, pas suppression). "
                        f"Déplacés quarantaine: {rep.get('moved_to_quarantine')}, "
                        f"actifs: {rep.get('active_nodes')}, dédup: {rep.get('deduped')}. "
                        f"Wiki files intacts."
                    ),
                    "sources": [],
                    "mode": "act_triage",
                    "report": rep,
                })
            if any(x in low for x in ("skill_learn", "apprend skill", "learn skill", "booster skill")) and "comment" not in low:
                if "comment" in low or "comment" in low:
                    pass
            if low.strip() in ("skill_learn", "run skill_learn", "lance skill_learn") or low.startswith("skill_learn "):
                sk = run_skill_learn()
                return self._json(200, {
                    "answer": f"skill_learn OK — {sk.get('skill')} ← {sk.get('topic')} (new={sk.get('new')})",
                    "sources": [],
                    "mode": "act_skill",
                    "report": sk,
                })
            if any(x in low for x in ("auto_learn", "apprend", "lance learn", "run learn")) and "comment" not in low and "booster" not in low:
                mode = "full" if "full" in low else ("wiki" if "wiki" in low else None)
                rep = run_auto_learn(mode=mode)
                return self._json(200, {
                    "answer": f"auto_learn cycle exécuté: {json.dumps(rep, ensure_ascii=False)[:500]}",
                    "sources": [],
                    "mode": "act_learn",
                    "report": rep,
                })
            if any(x in low for x in ("booster skill", "améliorer skill", "ameliorer skill", "comment booster")):
                return self._json(200, {
                    "answer": skill_boost_answer(),
                    "sources": [],
                    "mode": "skill_arch",
                })
            res = answer(q, k=int(data.get("k") or 6), use_arxiv=bool(data.get("use_arxiv", True)))
            return self._json(200, res)

        if path == "/api/learn":
            mode = data.get("mode")  # skill|wiki|triage|full|None
            rep = run_auto_learn(mode=mode)
            return self._json(200, {"ok": True, "report": rep})

        if path == "/api/skill":
            sk = run_skill_learn(
                force_skill=data.get("skill"),
                force_topic=data.get("topic"),
            )
            return self._json(200, {"ok": True, "report": sk})

        if path == "/api/triage":
            rep = run_triage(max_move=int(data.get("max_move") or 100))
            return self._json(200, {"ok": True, "report": rep, "note": "tri not delete"})

        if path == "/api/act":
            action = (data.get("action") or "").strip().lower()
            if action == "triage":
                return self._json(200, {"ok": True, "report": run_triage(max_move=int(data.get("max_move") or 100))})
            if action == "skill":
                return self._json(200, {"ok": True, "report": run_skill_learn()})
            if action in ("learn", "auto_learn", "full"):
                return self._json(200, {"ok": True, "report": run_auto_learn(mode=data.get("mode") or ("full" if action == "full" else None))})
            return self._json(400, {"error": "action must be triage|skill|learn|full"})

        return self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        print(f"[chat-server] {args[0]}", flush=True)


def main():
    host = "127.0.0.1"
    httpd = ThreadingHTTPServer((host, PORT), Handler)
    print(f"The-fly cortex → http://{host}:{PORT}", flush=True)
    print("  POST /api/chat | /api/learn | /api/skill | /api/triage | /api/act", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstop", flush=True)


if __name__ == "__main__":
    main()
