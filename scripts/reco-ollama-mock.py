#!/usr/bin/env python3
# Reco の Ollama 検出 + Gemma3:27b モデル DL を満たすモックサーバ。
# 文字起こし機能を解放しつつ Ollama 本体を起動せず 17GB DL も実行しない。
# - GET  /api/tags      : llama3.2 + gemma3:27b を「DL 済み」として返す
# - GET  /api/version   : ダミー version
# - GET  /api/ps        : 空 (running models)
# - POST /api/show      : gemma3:27b の詳細を返す
# - POST /api/pull      : ストリームで進捗 + success を返して即終了 (実 DL なし)
# - POST /api/generate, /api/chat : 503 で蹴る (要約は使えない)
# Listen: 127.0.0.1:11434
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import json, sys, datetime, time

PORT = 11434

MODELS = [
    {
        "name": "gemma4:26b",
        "model": "gemma4:26b",
        "modified_at": "2026-05-12T12:00:00Z",
        "size": 17_000_000_000,
        "digest": "g" * 64,
        "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "gemma4",
            "families": ["gemma4"],
            "parameter_size": "26B",
            "quantization_level": "Q4_K_M",
        },
    },
    {
        "name": "llama3.2:3b",
        "model": "llama3.2:3b",
        "modified_at": "2026-05-12T12:00:00Z",
        "size": 2_019_393_189,
        "digest": "l" * 64,
        "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "llama",
            "families": ["llama"],
            "parameter_size": "3.2B",
            "quantization_level": "Q4_K_M",
        },
    },
]

PULL_STATUSES = [
    {"status": "pulling manifest"},
    {"status": "pulling g00000000000000000000000000000000000000000000000000000000000000g", "digest": "sha256:" + "g" * 64, "total": 17_000_000_000, "completed": 0},
    {"status": "pulling g00000000000000000000000000000000000000000000000000000000000000g", "digest": "sha256:" + "g" * 64, "total": 17_000_000_000, "completed": 4_250_000_000},
    {"status": "pulling g00000000000000000000000000000000000000000000000000000000000000g", "digest": "sha256:" + "g" * 64, "total": 17_000_000_000, "completed": 8_500_000_000},
    {"status": "pulling g00000000000000000000000000000000000000000000000000000000000000g", "digest": "sha256:" + "g" * 64, "total": 17_000_000_000, "completed": 12_750_000_000},
    {"status": "pulling g00000000000000000000000000000000000000000000000000000000000000g", "digest": "sha256:" + "g" * 64, "total": 17_000_000_000, "completed": 17_000_000_000},
    {"status": "verifying sha256 digest"},
    {"status": "writing manifest"},
    {"status": "removing any unused layers"},
    {"status": "success"},
]


class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        sys.stderr.write(
            f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {self.address_string()} - {fmt % args}\n"
        )
        sys.stderr.flush()

    def _json(self, code, payload, keepalive=False):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if not keepalive:
            self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def _stream_ndjson(self, items, delay=0.5):
        self.send_response(200)
        self.send_header("Content-Type", "application/x-ndjson")
        self.send_header("Transfer-Encoding", "chunked")
        self.send_header("Connection", "close")
        self.end_headers()
        for it in items:
            line = (json.dumps(it) + "\n").encode("utf-8")
            chunk = f"{len(line):x}\r\n".encode("ascii") + line + b"\r\n"
            try:
                self.wfile.write(chunk)
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                return
            time.sleep(delay)
        try:
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        if self.path in ("/", "/api/version"):
            self._json(200, {"version": "0.5.0-reco-mock"})
        elif self.path == "/api/tags":
            self._json(200, {"models": MODELS})
        elif self.path == "/api/ps":
            self._json(200, {"models": []})
        else:
            self._json(404, {"error": f"mock: GET {self.path} not implemented"})

    def do_POST(self):
        cl = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(cl) if cl > 0 else b""
        try:
            req = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            req = {}
        sys.stderr.write(f"  POST body: {req}\n"); sys.stderr.flush()

        if self.path == "/api/pull":
            self._stream_ndjson(PULL_STATUSES, delay=0.4)
        elif self.path == "/api/show":
            self._json(200, {
                "modelfile": "FROM gemma4:26b",
                "parameters": "",
                "template": "{{ .Prompt }}",
                "details": MODELS[0]["details"],
                "model_info": {"general.architecture": "gemma4"},
            })
        elif self.path in ("/api/generate", "/api/chat", "/api/embeddings", "/api/embed"):
            self._json(503, {"error": "Reco-Ollama mock: summarization disabled"})
        else:
            self._json(404, {"error": f"mock: POST {self.path} not implemented"})


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


if __name__ == "__main__":
    s = ThreadedHTTPServer(("127.0.0.1", PORT), H)
    sys.stderr.write(f"Reco Ollama mock v2 on 127.0.0.1:{PORT} (gemma4:26b advertised)\n")
    sys.stderr.flush()
    s.serve_forever()
