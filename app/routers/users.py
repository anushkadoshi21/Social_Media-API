from sqlalchemy.orm import Session
from .. import schema
from .. import  models,utils
from ..database import  engine,get_db
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter

router=APIRouter(tags=['Users'])
@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schema.User_out)
def create_users(post:schema.User,db:Session=Depends(get_db)):
    post.password=utils.hash(post.password)
    data=models.User(**post.dict())
    try:
        db.add(data)
        db.commit()
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User already exists, please sign in")
    
    db.refresh(data)
    return data

@router.get("/users/{id}",status_code=status.HTTP_200_OK,response_model=schema.User_out)
def geta(id:int ,db:Session=Depends(get_db) ):
    data=db.query(models.User).filter(models.User.id==id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID not Found")
    return data