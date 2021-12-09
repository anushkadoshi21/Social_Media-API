from operator import mod
from os import stat
from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.sql.expression import join
from sqlalchemy.sql.functions import mode
from app import oath2, schema
from app import  models,utils
from sqlalchemy.orm import Session
from app.database import  engine,get_db
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import func
from app.config import settings
router=APIRouter(tags=['Posts'])
while True:
    try:
        conn=psycopg2.connect(host=settings.database_host,database=settings.database_name,user=settings.database_username,password=settings.database_password,
        cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("connected to database")
        break 
    except Exception as e:
        print("Cannot connect")
        print(e)
        time.sleep(2)

@router.post("/createposts/",status_code=status.HTTP_201_CREATED)
def post(newp:schema.Post=Body(...),id:int=Body(default=None)):
    #global ii,lis
    #newp=newp.dict()
    #if id is not None:
        #newp["id"]=id 
    #else:
        #newp["id"]=ii
    #lis.append(newp)
    #ii+=1 
    #print(lis)
    #return{"data":newp} 
    cursor.execute("""INSERT INTO social_media(content,title,is_published) VALUES(%s,%s,%s) returning *""",(newp.content,newp.title,newp.is_published))
    conn.commit()
    data=cursor.fetchone()
    return data

@router.get("/getpost/{id}",status_code=status.HTTP_200_OK)
def get_post(id:int):
    #global ii,lis
    #if id>=ii or id<0:
        #raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail="Post with id : "+str(id)+" not found")
    #return {"data":lis[id]}
    cursor.execute("""SELECT * FROM social_media where id= %s""",(str(id)))
    data=cursor.fetchone()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    return {"data":data}


@router.get("/getallposts/",status_code=status.HTTP_200_OK)
def get_all():
    cursor.execute("""SELECT * FROM social_media""")
    post=cursor.fetchall()
    return{"posts":post}

@router.delete("/deletepost/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int):
    cursor.execute("""DELETE  FROM social_media where id= %s returning *""",(str(id)))
    conn.commit()
    del_post=cursor.fetchone()
    if del_post is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    return {"deleted post":del_post}

@router.get("/orm_allposts",response_model=List[schema.Post_out])
def sqll(db: Session = Depends(get_db),skip:int=0,search:Optional[str]="",limit:int=10,user_id:int=Depends(oath2.get_current_user)):
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all() 
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).limit(limit).all()
    print(user_id)
    #posta=db.query(models.Post).all()
    return posts

@router.post("/orm_createpost",status_code=status.HTTP_201_CREATED,response_model=schema.response_post)
def create(postn:schema.Post,db:Session=Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    #postn=postn.dict()
    #postn["user_id"]=user_id.id
    newpost=models.Post(user_id=user_id.id,**postn.dict())
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    #print(newpost)
    return newpost

@router.get("/orm_getpost/{id}",status_code=status.HTTP_200_OK,response_model=schema.Post_out)
def gett(id:int, db:Session=Depends(get_db)):
    sel=db.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Post.id==models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if sel is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="POST NOT FOUND")
    return sel

@router.delete("/orm_delpost/{id}",status_code=status.HTTP_204_NO_CONTENT)
def dell(id:int,db:Session=Depends(get_db)):
    sel=db.query(models.Post).filter(models.Post.id==id)
    if sel.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    sel.delete(synchronize_session=False)
    db.commit()
    return{"deleted_post":"deleted successfully"}

@router.get("/orm_uppost/{id}",status_code=status.HTTP_200_OK,response_model=schema.response_post)
def gett(id:int ,post:schema.Post, db:Session=Depends(get_db)):
    sel=db.query(models.Post).filter(models.Post.id==id)
    if sel.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="POST NOT FOUND")
    sel.update(post.dict(),synchronize_session=False)
    db.commit()
    return sel.first()

@router.get("/postid",response_model=List[schema.Postid],status_code=status.HTTP_200_OK)
def get_allpostids(db: Session = Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    data=db.query(models.Post).all()
    return data