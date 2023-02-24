from database.database import DatabaseConnection as db
from password_hash import PasswordHasher as pwdHasher


class User:
    def __init__(self, id: str, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.__password = pwdHasher.hashPassword(password)

    def to_dict(self):
        return {
            'username': self.name,
            'password': self.__password,
            'email': self.email
        }

    def setPassword(self, password):
        self.__password = pwdHasher.hashPassword(password)

    def add_user(self):
        query = "INSERT INTO users (id, name, password, email) VALUES (%s,%s, %s, %s)"
        params = (self.id, self.name, self.__password, self.email)
        result = db.get_instance().query(query, params)
        if result is False:
            return False
        return result

    def remove_user(self):
        query = "DELETE FROM users WHERE id = %s"
        params = (self.id,)
        result = db.get_instance().query(query, params)
        if result is False:
            return False
        return result

    def update_user(self):
        query = "UPDATE users SET name = %s, password = %s, email = %s WHERE id = %s"
        params = (self.name, self.__password, self.email, self.id)
        result = db.get_instance().query(query, params)
        if result is False:
            return False
        return result

    def login(self):
        query = "SELECT password FROM users WHERE id = %s"
        params = (self.id,)
        result = db.get_instance().query(query, params)
        if result is False or result is None or len(result) == 0:
            return False
        if pwdHasher.validatePassword(self.__password, result[0]):
            return True
        return False

    @staticmethod
    def from_dict(user_dict):
        return User(user_dict.get('id', None), user_dict.get('name', None), user_dict.get('password', 0), user_dict.get('email', None))
