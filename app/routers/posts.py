from typing import Optional

from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session
from .. import database, models, schemas, oath2

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostOut])
async def posts(
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oath2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    stmt = (
        select(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
    ).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    posts = db.execute(stmt).all()
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no posts found"
        )
    return [
        {"Post":post,
        "votes":votes
        }
        for post,votes in posts
    ]


@router.get("/{id}", response_model=schemas.PostOut)
async def get_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oath2.get_current_user),
):
    stmt = select(models.Post,func.count(models.Vote.post_id)).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).where(models.Post.id == id).group_by(models.Post.id)
    result = db.execute(stmt).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    post,votes = result
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not autherized to perform the required action",
        )
    return {"Post":post,"votes":votes}


@router.post("/", response_model=schemas.Post)
async def create_post(
    post: schemas.PostsCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oath2.get_current_user),
):
    # print("*"*20)
    # print(current_user.id)
    # print("*"*20)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.PostBase)
async def update_post(
    id: int,
    post: schemas.PostsCreate,
    db: Session = Depends(database.get_db),
    current_user=Depends(oath2.get_current_user),
):
    stmt = select(models.Post).where(models.Post.id == id)
    post_query = db.execute(stmt).scalar_one_or_none()
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    # print("*" * 40)
    # print(current_user.id)
    # print("*" * 40)
    if post_query.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not autherized to perform the required action",
        )
    update_post = post.model_dump()

    for key, value in update_post.items():
        setattr(post_query, key, value)

    db.commit()
    db.refresh(post_query)
    return post_query


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user=Depends(oath2.get_current_user),
):
    stmt = select(models.Post).where(models.Post.id == id)
    post = db.execute(stmt).scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not autherized to perform the required action",
        )

    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
