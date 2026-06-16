from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .. import database,models,schemas,oath2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(vote:schemas.Vote,db: Session = Depends(database.get_db),current_user:int = Depends(oath2.get_current_user)):
    post = db.execute(select(models.Post).where(models.Post.id == vote.post_id)).scalar_one_or_none()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} doesn't exist"
        )
    stmt = select(models.Vote).where(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    voted = db.execute(stmt).scalar_one_or_none()
    if vote.dir == 1:
        if voted:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.email} has already voted on post with id {vote.post_id} "
            )
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        if not voted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vote does not exist"
            )
        db.delete(voted)
        db.commit()
        return {"message":"successfully deleted vote"}