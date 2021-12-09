from jose import JWTError, jwt
from datetime import timedelta,datetime
from fastapi import status,HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from jose.constants import Algorithms
from app import schema
from .config import settings
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(settings.access_token_expire_minutes))
    to_encode["exp"]=expire
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        data=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        id:str=data.get("user_id")
        if id is None:
            raise credentials_exception
        print(id)
        token_data=schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not authorize credentials",
                                                                                 headers={"WWW Auth":"bearer"})
    return verify_token(token,credentials_exception)

