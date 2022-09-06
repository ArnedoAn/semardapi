import bcrypt

salt = bcrypt.gensalt()

def validatePwd(password, pwdHash):
    return bcrypt.checkpw(password, pwdHash)

def encryptPwd(password):
    return str(bcrypt.hashpw(password, salt))