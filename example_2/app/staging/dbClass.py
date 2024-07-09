import sqlite3
import pandas as pd # TO DO: Import this with requirements.txt
import os

class DataBase:

    '''
    PUBLIC FUNCTIONS
    '''

    def create_db( self, db_name=None, csv_file=None ):

        # create db if it exists
        if not os.path.exists(self.db_name):

            print( f"(!) Database file '{self.db_name}' not found.")
            # set name stuff
            if ( db_name != None ):
                self.db_name = db_name
            
            if ( csv_file != None ):
                self.csv_file =  csv_file

            # create the db
            return self._create_db()

        return False


    def execute_query( self, query ):

        data = self._execute_query( query )

        if self._conn != None:
            
            self._close_db()

        # Return result, if there is one.
        return data

    '''
    PRIVATE FUNCTIONS
    '''
    def _execute_query( self, query ):

        print("Query:", query)

        # try to connect
        if self._connect_db():

            try:
                self._cursor.executescript(query)
                return self._cursor.fetchall()

            # catches integrity error
            except sqlite3.IntegrityError as e:
                print(f"Integrity error: {e}")
                return None
            
            # catches operational
            except sqlite3.OperationalError as e:
                print(f"Operational error: {e}")
                return None
            
            # catches database error
            except sqlite3.DatabaseError as e:
                print(f"Database error: {e}")
                return None
            
            # Catches any other unexpected errors
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return None
        
        # return none
        return None

    def _close_db( self ):
        
        if self._conn != None:

            self._conn.close()
            print(f"(!) Closed connection to '{self.db_name}'.")

        else:
            print(f"(!) '{self.db_name}' not currently open.")

    def _commit_db( self ): # Simple command: commit to db
        if self._conn != None:
            self._conn.commit()
            return True
        return False
        
    def _connect_db( self ): # Simple command: Connect to to db

        # open connection
        self._conn = sqlite3.connect( self.db_name )

        # ensure it opened
        if self._conn != None:

            # grab cursor
            self._cursor = self._conn.cursor()

            # print success :)
            print(f"(!) Opened connection to '{self.db_name}'.")

            # return true
            return True
        
        # set cursor to None
        self._cursor = None

        # print false :(
        print(f"(!) Connection with '{self.db_name}' failed.")

        # return false, bad connect
        return False

    def _create_db( self ):

        # check if exists

        # Load CSV into a DataFrame
        df = pd.read_csv( self.csv_file )

        if self._conn != None:
            print("(!) You should never see this message.")

        # ensure we can connect
        if self._connect_db():

            # Create table with appropriate column names and types
                # this is so yucky sorry
            query = f"CREATE TABLE IF NOT EXISTS {self.table_name}"
            df.to_sql(self.table_name, self._conn, if_exists='append', index=False)

            # commit
            if self._commit_db():

                # close db
                self._close_db()

                return True

        return False

    def _insert( self, query ): # Simple command: insert to db

        # execute query
        try:
            self._conn.executescript( query ) # SECURITY ISSUE: BUGGY!
        
        # catches integrity error
        except sqlite3.IntegrityError as e:
            print(f"Integrity error: {e}")
            return False
        
        # catches operational
        except sqlite3.OperationalError as e:
            print(f"Operational error: {e}")
            return False
        
        # catches database error
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return False
        
        # Catches any other unexpected errors
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
        
        return True

    # INITIALIZE DB
    def __init__( self, DB_NAME, CSV_FILE ): 

        # initialize variables
        self.db_name = DB_NAME
        self.csv_file = CSV_FILE
        self.table_name = "pkmon_tbl"
        self._conn = None
        self._cursor = None

        # initialize database
        self.create_db()