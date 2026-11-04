"""Serve the demo: python web/serve.py [host] [port]   then open http://localhost:8000/web/
Also answers GET /lan with this laptop's current LAN IP, so the page knows which subnet to scan for the camera."""
import http.server, json, pathlib, socket, sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"  # use 0.0.0.0 to open it from another device
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
ROOT = pathlib.Path(__file__).resolve().parent.parent


def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))  # no packet is sent; just picks the interface of the default route
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def do_GET(self):
        if self.path != "/lan":
            return super().do_GET()
        body = json.dumps({"ip": lan_ip()}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"CLEARWAVE demo: http://{'localhost' if HOST == '127.0.0.1' else HOST}:{PORT}/web/")
    http.server.ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
