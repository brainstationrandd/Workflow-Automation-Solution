from passlib.hash import bcrypt


def hash_password(password):
    hashed = bcrypt.hash(password)
    return hashed

def check_password(password, hashed_password):
    return bcrypt.verify(password, hashed_password)