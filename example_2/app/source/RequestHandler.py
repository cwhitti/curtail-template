import http.server
from dbClass import DataBase
from urllib.parse import urlparse, parse_qs
import os

# define global constants
DB_FILE = "data/pokemon.db"
CSV_FILE = "data/pokemon.csv"


# Define the request handler
class RequestHandler( http.server.SimpleHTTPRequestHandler ):

    def __init__(self, *args, db=None, **kwargs, ):
        self.db = db
        super().__init__(*args, **kwargs)

    '''
    PUBLIC FUNCTIONS
    '''
    # HAS to be named this
    def do_GET( self ):

        print("(!) Established connection on localhost")

        if self.path == "/":
            self._handle_root()

        elif self.path == "/test":
            self._handle_test()

        elif self.path == "/search":
            self._handle_search()
            pass

        else:
            self._handle_404()

    def do_POST(self):

        print("(!) Established connection on localhost")

        # Listening for:
            #curl -X POST -d "name=pikachu lol&id=12" 0:80/search
            
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)
        
        if self.path == "/search":

            self._handle_search( params=params )

        else:
            self._handle_404()

    '''
    PRIVATE FUNCTIONS
    '''

    # Handles bad response
    def _handle_404(self):
        response = 400
        title = "404 Not Found"
        body  = "<h1>404 Not Found</h1><p>The page you requested does not exist.</p>"
        self._serve_html( response, title, body )
        return response
    
    def _handle_empty_query(self):

        response = 404
        title = "Bad Search"
        body = "Must specify type_1, type_2, or both."
        self._serve_html( response, title, body )
        return response
    
    def _handle_search(self, params):

        print(params)
        if params == None or len(params) == 0:
            return  self._handle_empty_query()
        
        # craft query
        query = f"SELECT * FROM {self.db.table_name} WHERE "

        # loop thru params
        for key, list in params.items():
            val = list[0] # grab the list from the post request
            query += f'{key}="{val}" AND '

        # Remove the last " AND " from the query
        query = query[:-5]  # This removes the last 5 characters (" AND ")

        # grab data
        data = self.db.execute_query( query )  

        # Make sure we even grabbed anything
        if data != None and len(data) > 0:

            response = 200

            title = "Search found"

            items_html = "<ul>"
            for item in data:
                items_html += f"<li>{item}</li>" 
            items_html += "</ul>"

            body = f"<h1>Pokemon List</h1>{items_html}" 
        
        else:
            response = 404
            title = "Bad Search"
            body = "No Pokemon found"

        self._serve_html(response, title, body)

        return response

        
    # Handles the test endpoint
    def _handle_test(self):
        response = 200
        title = "Test Endpoint"
        body  = "<h1>Test Page</h1><p>This endpoint is different!.</p>"
        self._serve_html( response, title, body )
        return response

    # Handles the root endpoint
    def _handle_root(self):
        response = 200
        title = "Root Endpoint"
        body  = "<h1>Welcome to the Root!</h1><p>This is the main page.</p>"
        self._serve_html( response, title, body )
        return response

    def _serve_html( self, resp, title, body, extra_headers=None ): 

        self.send_response( resp )
        self.send_header("Content-type", "text/html")
        self.end_headers()

        title = f"<html><head><title>{title}</title></head>"
        body  = f"<body>{body}</body></html>"

        if isinstance(title, str):
            title = title.encode('utf-8')

        if isinstance(body, str):
            body = body.encode('utf-8')

        self.wfile.write( title)
        self.wfile.write( body )


