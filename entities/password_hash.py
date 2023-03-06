from werkzeug.security import generate_password_hash, check_password_hash

class PasswordHasher:
    def __init__(self):
        pass

    def hashPassword(pwd):
        return generate_password_hash(pwd)

    def validatePassword(password, pwdHash):
        print(str(password))
        print(pwdHash)
        print(check_password_hash(pwdHash, password))
        return check_password_hash(pwdHash,password)
