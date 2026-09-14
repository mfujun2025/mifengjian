# -*- coding: utf-8 -*-
"""模拟飞书群机器人 webhook，用于本地端到端验证询单表单。
请求体里带 FAILTEST 字段则返回飞书错误码，否则返回成功。"""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "_form_requests.jsonl")


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n).decode("utf-8")
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({"path": self.path, "body": raw}, ensure_ascii=False) + "\n")

        if "FAILTEST" in raw:
            payload = {"code": 19001, "msg": "param invalid: incoming webhook access token invalid"}
        else:
            payload = {"code": 0, "msg": "success", "data": {}}
        b = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    open(LOG, "w", encoding="utf-8").close()
    print("mock feishu webhook on http://127.0.0.1:8792/hook")
    HTTPServer(("127.0.0.1", 8792), H).serve_forever()
