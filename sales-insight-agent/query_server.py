import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from database.queries import fetch_sales_data

HOST = "127.0.0.1"
PORT = 8081


class SalesQueryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/health":
            self._send_json(404, {"error": "Not found."})
            return
        self._send_json(200, {"status": "ok"})

    def do_POST(self):
        if self.path != "/sales":
            self._send_json(404, {"error": "Not found."})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length)

        try:
            body = json.loads(raw_body.decode("utf-8"))
            results = fetch_sales_data(
                start_date=body["start_date"],
                end_date=body["end_date"],
                product_name=body.get("product_name", ""),
                region_name=body.get("region_name", ""),
                group_by=body.get("group_by", "month"),
            )
        except KeyError as error:
            self._send_json(400, {"error": f"Missing field: {error.args[0]}"})
            return
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})
            return
        except Exception as error:
            self._send_json(500, {"error": str(error)})
            return

        self._send_json(200, {"results": results})

    def _send_json(self, status, payload):
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), SalesQueryHandler)
    print(f"Sales query endpoint listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
