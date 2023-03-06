import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('DB_HOST')
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PWD')
DATABASE = os.getenv('DB_DB')


class DatabaseConnection:
    __instance = None

    @staticmethod
    def get_instance():
        """ Retorna la instancia única de la clase. """
        if DatabaseConnection.__instance is None:
            DatabaseConnection()
        return DatabaseConnection.__instance

    def __init__(self):
        """ Si no existe instancia, la crea. """
        if DatabaseConnection.__instance is not None:
            raise Exception("Esta clase es un Singleton.")
        else:
            # Crea la conexión a la base de datos.
            self.conn = psycopg2.connect(
                host=HOST,
                database=DATABASE,
                user=USER,
                password=PASSWORD
            )
            DatabaseConnection.__instance = self

    def query(self, query, params=None):
        """ Ejecuta una consulta en la base de datos. """
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            if query.lower().startswith('select'):
                result = cur.fetchall()
                self.conn.commit()
                return result
            self.conn.commit()
            return True 
        except (Exception, psycopg2.DatabaseError) as error:
            print(error, "Esto es un error")
            self.conn.rollback()
            return False
        finally:
            cur.close()
