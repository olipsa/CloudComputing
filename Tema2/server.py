import urllib
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import methods
import database


class handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        parameters = urllib.parse.parse_qs(parsed_url.query)
        path = self.path.removesuffix(parsed_url.query)
        methods.GET(self, path, parameters)

    def do_POST(self):
        parsed_url = urlparse(self.path)
        parameters = urllib.parse.parse_qs(parsed_url.query)
        path = self.path.removesuffix(parsed_url.query)
        methods.POST(self, path, parameters)

    def do_PUT(self):
        parsed_url = urlparse(self.path)
        parameters = urllib.parse.parse_qs(parsed_url.query)
        path = self.path.removesuffix(parsed_url.query)
        methods.PUT(self, path, parameters)

    def do_DELETE(self):
        parsed_url = urlparse(self.path)
        parameters = urllib.parse.parse_qs(parsed_url.query)
        path = self.path.removesuffix(parsed_url.query)
        methods.DELETE(self, path, parameters)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def main():
    server = ThreadingSimpleServer(("", 8088), handler)
    print("Server started at port 8088.")
    database.connect()
    server.serve_forever()
    server.server_close()
    database.close()
    print("Server stopped.")


main()
