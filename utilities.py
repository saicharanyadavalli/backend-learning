from passlib.context import CryptContext
passlib = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return passlib.hash(password)

def verify_password(plain_password, hashed_password):
    return passlib.verify(plain_password, hashed_password)