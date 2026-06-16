from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from .. import database,schemas,models,utils
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def create_user(user:schemas.UserCreate,db:Session = Depends(database.get_db)):
    try:
        user_data = user.model_dump()
        #Here put the hashing
        user_data["password"] = utils.hash(user.password)
        new_user =  models.User(**user_data)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session = Depends(database.get_db)):
    stmt = select(models.User).where(models.User.id == id)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id {id} does not exist"
        )
    
    return user