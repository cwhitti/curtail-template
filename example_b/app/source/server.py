import socketserver
from RequestHandler import RequestHandler
from dbClass import DataBase

# Define the server address and port
HOST, PORT = "0.0.0.0", 80
DB_FILE = "data/pokemon.db"
CSV_FILE = "data/pokemon.csv"

db = DataBase( DB_FILE, CSV_FILE )

def server_loop():

    with socketserver.TCPServer((HOST, PORT), 
                                lambda *args, **kwargs: 
                                RequestHandler(*args, db=db, **kwargs)) as httpd:
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()