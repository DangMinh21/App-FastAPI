from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(pwd: int):
    return pwd_context.hash(pwd)
