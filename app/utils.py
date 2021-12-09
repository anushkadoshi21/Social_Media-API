from typing_extensions import ParamSpecKwargs
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def login(plain_pass:str, hashed:str):
    return pwd_context.verify(plain_pass,hashed)