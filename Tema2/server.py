import urllib
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import methods


class handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        parameters = urllib.parse.parse_qs(parsed_url.query)
        methods.GET(self, self.path.removesuffix(parsed_url.query)[:-1], parameters)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def main():
    server = ThreadingSimpleServer(("", 8088), handler)
    print("Server started at port 8088.")
    server.serve_forever()
    server.server_close()
    print("Server stopped.")


main()
