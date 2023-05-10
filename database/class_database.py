from abc import ABC, abstractmethod
import os

class Database(ABC):

    def __init__(self) -> None:
        self.HOST = os.getenv('DB_HOST')
        self.USER = os.getenv('DB_USER')
        self.PASSWORD = os.getenv('DB_PWD')
        self.DATABASE = os.getenv('DB_DB')

    @abstractmethod
    def Createconexion(self):
        pass
    
    def query(self, query, conn, params=None):
        # Ejecuta una consulta en la base de datos. 
        try:
            cur = self.conn.cursor()
            cur.execute(query, params)
            
            if query.lower().startswith('select'):
                result = cur.fetchall()
                conn.commit()
                return result
            
            conn.commit()
            return True

        except (Exception, ) as error:
            print(error, "Esto es un error")
            self.conn.rollback()
            return False
        finally:
            cur.close()
