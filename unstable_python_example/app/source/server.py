import socketserver
from RequestHandler import RequestHandler

# Define the server address and port
HOST, PORT = "0.0.0.0", 80

def server_loop():

    with socketserver.TCPServer((HOST, PORT), 
                                lambda *args, **kwargs: 
                                RequestHandler(*args, **kwargs)) as httpd:
        print(f"Serving on {HOST}:{PORT}...")
        httpd.serve_forever()