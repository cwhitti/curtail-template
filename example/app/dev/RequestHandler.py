import http.server
import socketserver

# Define the request handler
class RequestHandler( http.server.SimpleHTTPRequestHandler ):

    # PRIVATE FUNCTIONS 

    # Handles bad response
    def _handle_404(self):
        response = 400
        title = (b"<html><head><title>404 Not Found</title></head>")
        body  = (b"<body><h1>404 Not Found</h1><p>The page you requested does not exist.</p></body></html>")
        self._serve_html( response, title, body )
        return response
        
    # Handles the test endpoint
    def _handle_test(self):
        response = 200
        title = (b"<html><head><title>Test Endpoint</title></head>")
        body  = (b"<body><h1>Test Page</h1><p>This is the /test endpoint.</p></body></html>")
        self._serve_html( response, title, body )
        return response

    # Handles the root endpoint
    def _handle_root(self):
        response = 200
        title = (b"<html><head><title>Root Endpoint</title></head>")
        body  = (b"<body><h1>Welcome to the Root!</h1><p>This is the main page.</p></body></html>")
        self._serve_html( response, title, body )
        return response

    def _serve_html( self, resp, title, body, extra_headers=None ): 

        self.send_response( resp )
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write( title)
        self.wfile.write( body )

    # PUBLIC FUNCTIONS

    def do_GET(self):
        if self.path == "/":
            self._handle_root()
        elif self.path == "/test":
            self._handle_test()
        else:
            self._handle_404()
