"""Small JSON API using only the Python standard library.

Run with: python api.py
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from errors import ParcelSystemError
from system import ParcelSystem


class ParcelAPIHandler(BaseHTTPRequestHandler):
    """HTTP endpoints over the same ParcelSystem business logic."""

    system = None

    def _send(self, status: int, payload: dict | list) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            raise ValueError("Request body must be JSON.")
        data = json.loads(self.rfile.read(length).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("JSON body must be an object.")
        return data

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        try:
            if path == "/api/parcels":
                self._send(200, [parcel.to_dict() for parcel in self.system])
            elif path == "/api/desk":
                self._send(200, self.system.desk.desk)
            elif path == "/api/collected":
                self._send(200, self.system.pickup.collected)
            elif path.startswith("/api/overdue/"):
                pid = path.rsplit("/", 1)[-1]
                self._send(200, self.system.overdue_summary(pid))
            else:
                self._send(404, {"error": "Endpoint not found"})
        except ParcelSystemError as error:
            self._send(400, {"error": str(error)})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            data = self._read_json()
            if path == "/api/parcels":
                parcel = self.system.add_parcel(
                    data["date"], data["receiver"], data["item"]
                )
                self._send(201, parcel.to_dict())
            elif path == "/api/tenants":
                tenant = self.system.register_tenant(data["name"], int(data["room"]))
                self._send(201, tenant.to_dict())
            elif path == "/api/assign":
                self._send(200, self.system.assign_parcel(data["pid"]))
            elif path == "/api/collect":
                record = self.system.collect_parcel(data["tenant"], data["pid"])
                self._send(200, record)
            elif path == "/api/payments":
                record = self.system.make_payment(
                    data["tenant"], data["pid"], int(data["amount"])
                )
                self._send(201, record)
            else:
                self._send(404, {"error": "Endpoint not found"})
        except (ParcelSystemError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
            self._send(400, {"error": str(error)})

    def log_message(self, format_string: str, *args) -> None:
        # Keep standard HTTP logs concise.
        print(f"[API] {self.address_string()} - {format_string % args}")


def main() -> None:
    ParcelAPIHandler.system = ParcelSystem()
    server = HTTPServer(("127.0.0.1", 8000), ParcelAPIHandler)
    print("Parcel API running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        ParcelAPIHandler.system.save_all()
        server.server_close()


if __name__ == "__main__":
    main()
