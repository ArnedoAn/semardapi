from werkzeug.security import generate_password_hash, check_password_hash

def encryptPwd(pwd):
    return generate_password_hash(pwd)

def validatePwd(password, pwdHash):
    return check_password_hash(pwdHash,password)
     