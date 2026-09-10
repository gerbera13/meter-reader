#!/usr/bin/env python3
import http.server
import urllib.request
import json
import sys

LM_HOST = "http://127.0.0.1:1234"

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/proxy/"):
            url = LM_HOST + "/" + self.path[7:]
            self._proxy("GET", url)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/proxy/"):
            url = LM_HOST + "/" + self.path[7:]
            self._proxy("POST", url)
        else:
            super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def _proxy(self, method, url):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else None

        req = urllib.request.Request(url, data=body, method=method)
        req.add_header("Content-Type", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(data)

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    http.server.HTTPServer(("", port), Proxy).serve_forever()
