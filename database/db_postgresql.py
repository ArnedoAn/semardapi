import psycopg2
from database.class_database import Database as db

class DBPostgresql(db):
    __instance = None

    def __init__(self):
        super().__init__()

        # Si no existe instancia, la crea.
        if DBPostgresql.__instance is not None:
            raise Exception('This class is Singleton.')
        else:
            self.Createconexion()

    @staticmethod
    def get_instance():
        # Retorna la instancia única de la clase.
        if DBPostgresql.__instance is None:
            DBPostgresql()
        return DBPostgresql.__instance

    def querys(self, query, params=None):
        return super().query(query, self.conn, params)
    
    # Crea la conexión a la base de datos.
    def Createconexion(self):
        self.conn = psycopg2.connect(
            host=self.HOST,
            database=self.DATABASE,
            user=self.USER,
            password=self.PASSWORD
        )
        DBPostgresql.__instance = self
