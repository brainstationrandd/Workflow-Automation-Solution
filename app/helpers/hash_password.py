import bcrypt


def hash_password(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.verify(password, hashed_password)

def check_password_for_login(plain_password: str, stored_password_hash: str) -> bool:
    plain_pwd_bytes = plain_password.encode('utf-8')
    stored_pwd_bytes = stored_password_hash.encode('utf-8')
    return bcrypt.checkpw(plain_pwd_bytes, stored_pwd_bytes)
