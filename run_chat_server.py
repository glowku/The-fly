#!/usr/bin/env python3
"""Serveur local Graph-RAG pour le chat de fly-brain.html (stdlib only)."""
from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from agent.graph_rag import answer, retrieve, verify_claim
from agent.arxiv_source import search_domain

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
            return self._json(200, {"ok": True, "service": "the-fly-chat", "port": PORT})
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

        q = (data.get("question") or data.get("q") or data.get("claim") or "").strip()
        if not q:
            return self._json(400, {"error": "question required"})
        k = int(data.get("k") or 6)
        use_arxiv = data.get("use_arxiv", True)

        if path == "/api/chat":
            res = answer(q, k=k, use_arxiv=bool(use_arxiv))
            return self._json(200, res)
        if path == "/api/verify":
            res = verify_claim(q, k=k)
            return self._json(200, res)
        return self._json(404, {"error": "not found"})

    def log_message(self, fmt, *args):
        print(f"[chat-server] {args[0]}", flush=True)


def main():
    host = "127.0.0.1"
    httpd = ThreadingHTTPServer((host, PORT), Handler)
    print(f"The-fly chat API → http://{host}:{PORT}", flush=True)
    print("  POST /api/chat   {\"question\": \"...\"}", flush=True)
    print("  POST /api/verify {\"claim\": \"...\"}", flush=True)
    print("  GET  /api/retrieve?q=...&k=6", flush=True)
    print("  GET  /api/arxiv?q=insect+flight", flush=True)
    print("Ouvre docs/fly-brain.html (file:// ou python -m http.server)", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstop", flush=True)


if __name__ == "__main__":
    main()
