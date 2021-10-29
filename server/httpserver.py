from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from serverfunc import get_volumes, list_folders


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == "/":
            result = get_volumes()
        else:
            result = list_folders(self.path[1:].replace("%20", " "))

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_string = json.dumps(result)
        self.wfile.write(bytes(json_string, 'utf8'))

def run_http_server():
    with HTTPServer(('', 8080), handler) as server:
        print(123)
        server.serve_forever()
