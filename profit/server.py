import http.server
import socketserver
import urllib.parse

PORT = 8008


def start(path):
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)
    print(
        f"Open visualization at http://localhost:{PORT}/{urllib.parse.quote(str(path))}/visualization.html"
    )
    httpd.serve_forever()
