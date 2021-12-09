from sqlalchemy.orm import Session
from .. import schema
from .. import  models,utils,oath2
from ..database import  engine,get_db
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter

router=APIRouter(tags=['Auth'])
@router.post('/login',status_code=status.HTTP_202_ACCEPTED,response_model=schema.Token)
def login(cred:schema.User,db:Session=Depends(get_db)):
    data=db.query(models.User).filter(models.User.email==cred.email).first()
    if not data or not utils.login(cred.password,data.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Creds")
    token=oath2.create_access_token(data={"user_id":data.id})
    tt=schema.Token(access_token=token)
    #return {"access_token":token,"token_type":"Bearer"}
    return tt