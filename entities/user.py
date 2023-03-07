from database.database import DatabaseConnection as db
from entities.password_hash import PasswordHasher as pwdHasher


class User:
    def __init__(self, dni: str, name: str, password: str):
        self.dni = dni
        self.name = name
        self.__password = str(pwdHasher.hashPassword(password))

    def to_dict(self):
        return {
            'name': self.name,
            'password': self.__password,
        }

    def setPassword(self, password):
        self.__password = pwdHasher.hashPassword(password)

    def add_user(self):
        query = "INSERT INTO public.users (dni, name, password) VALUES (%s,%s, %s)"
        params = (self.dni, self.name, self.__password)
        print(query)
        print(params)
        result = db.get_instance().query(query, params)
        if result is False:
            return False
        return result

    def remove_user(self):
        query = "DELETE FROM users WHERE dni = %s"
        params = (self.dni,)
        result = db.get_instance().query(query, params)
        if result is False:
            return False
        return result

    def update_user(self):
        query = "UPDATE users SET name = %s, password = %s WHERE dni = %s"
        params = (self.name, self.__password, self.dni)
        result = db.get_instance().query(query, params)
        if result is False:
            return False
        return result

    def login(self, pwd):
        query = "SELECT password FROM users WHERE dni = %s"
        params = (self.dni,)
        result = db.get_instance().query(query, params)
        if result is False or result is None or len(result) == 0:
            return False
        if pwdHasher.validatePassword(pwd, result[0]):
            return True
        return False

    @staticmethod
    def from_dict(user_dict):
        print(user_dict.get('dni', None), user_dict.get('name', None), user_dict.get('password', 0))
        return User(user_dict.get('dni', None), user_dict.get('name', None), str(user_dict.get('password', 0)))
    
