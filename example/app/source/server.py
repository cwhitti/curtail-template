import socketserver
from RequestHandler import RequestHandler

# Define the server address and port
HOST, PORT = "127.0.0.1", 80

def server_loop():

    # Create and start the server
    with socketserver.TCPServer((HOST, PORT), RequestHandler) as httpd:
        #print(f"Serving on port {PORT}...")
        httpd.serve_forever()