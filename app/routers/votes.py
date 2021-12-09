from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.sql.functions import mode
from app import oath2, schema
from app import  models,utils
from sqlalchemy.orm import Session
from app.database import get_db

router=APIRouter(tags=["Votes"])

@router.post('/votes/{id}',status_code=status.HTTP_202_ACCEPTED)
def vote(id:int,db: Session = Depends(get_db),user_id:int=Depends(oath2.get_current_user)):
    sel=db.query(models.Post).filter(models.Post.id==id)
    voted=None
    print(voted)
    if sel.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="POST NOT FOUND")
    vote_exists=db.query(models.Vote).filter(models.Vote.post_id==id and models.Vote.user_id==user_id)
    
    if vote_exists.first() is None:
        newvote=models.Vote(user_id=user_id.id,post_id=id)
        voted="UpVote"
        db.add(newvote)
        db.commit()
    else:
        #raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail="Downvoting")
        #downvote=db.query(models.Vote).filter(models.Vote.user_id==user_id and models.Vote.post_id==id)
        vote_exists.delete(synchronize_session=False)
        voted="DownVote"
        db.commit()
    
    return {"voted":voted}
    