"""Local web app for asking questions against the provided Solstice docs."""

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from retrieval import answer_question, load_docs


DATA_DIR = Path(__file__).parent / "data"
WEB_PAGE = Path(__file__).with_name("index.html")
DOCS = load_docs(DATA_DIR / "docs.json")


class RequestHandler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, status, payload):
        self._send(status, json.dumps(payload), "application/json; charset=utf-8")

    def do_GET(self):
        if self.path == "/":
            self._send(200, WEB_PAGE.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        elif self.path == "/health":
            self._send_json(200, {"status": "ok", "documents": len(DOCS)})
        else:
            self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if self.path != "/ask":
            self._send_json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 10_000:
                self._send_json(413, {"error": "Question is too long"})
                return
            payload = json.loads(self.rfile.read(length))
            question = payload.get("question", "")
            if not isinstance(question, str):
                raise ValueError("Question must be text")
        except (json.JSONDecodeError, AttributeError, ValueError):
            self._send_json(400, {"error": "Send a JSON object with a text question"})
            return
        self._send_json(200, answer_question(question, DOCS))

    def log_message(self, format_string, *args):
        print("%s - %s" % (self.address_string(), format_string % args))


def main():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), RequestHandler)
    print("Solstice Docs Q&A is available at http://%s:%s" % (host, port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()