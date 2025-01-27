import mysql.connector
from mysql.connector import Error

class Connection: 
    def __init__(self, host, db, user,password ):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
            host= self.host,       # Change the address for your server
            database= self.db,   # Name of the Database
            user=self.user,      # User of the Database
            password= self.password)
            if self.connection.is_connected():
                print("Conexion exitosa")
        except Error as e:
            print("Error al conectarse a la base de datos: ", e)
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")

    #Select in the Database.
    def select(self, query, params=None):
        
        if not self.connection or not self.connection.is_connected():
            print("The connection is not active. Please, first connect.")
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error in the command SELECT: {e}")
            return None
        finally:
            cursor.close()
    