import http.server
from urllib.parse import urlparse, parse_qs
import random

# Define the request handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("(!) Established connection on localhost")

        if self.path == "/":
            self._handle_root()
        elif self.path == "/test":
            self._handle_test()
        elif self.path.startswith("/multiply"):
            self._handle_multiply()
        else:
            self._handle_404()

    def _handle_404(self):
        response = 404
        title = "404 Not Found"
        body = "<h1>404 Not Found</h1><p>The page you requested does not exist.</p>"
        self._serve_html(response, title, body)

    def _handle_empty_query(self):
        response = 400
        title = "Bad Request"
        body = "<h1>400 Bad Request</h1><p>Must specify type_1, type_2, or both.</p>"
        self._serve_html(response, title, body)

    def _handle_multiply(self):

        response = 200
        length = random.randint(70, 10000000)
        title = "Str Multiplier"

        mystr = int( '2' + '0' * length ) 
        body = f"<h1>Result</h1><p>Generated Length: {length}\nString:{mystr}.</p>"
        self._serve_html(response, title, body)

    def _handle_test(self):
        response = 200
        title = "Test Endpoint"
        body = "<h1>Test Page</h1><p>This endpoint is different!.</p>"
        self._serve_html(response, title, body)

    def _handle_root(self):
        response = 200
        title = "Root Endpoint"
        body = "<h1>Welcome to the Root!</h1><p>This is the main page.</p>"
        self._serve_html(response, title, body)

    def _serve_html(self, response, title, body):
        self.send_response(response)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = f"<html><head><title>{title}</title></head><body>{body}</body></html>"
        self.wfile.write(html.encode('utf-8'))
