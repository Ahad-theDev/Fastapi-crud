from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy import select
from .. import database,schemas,models,utils,oath2
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/",response_model=schemas.Token)
async def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    stmt = select(models.User).where(models.User.email == user_credentials.username)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )
    if not utils.verify_password(user_credentials.password,user.password):
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail= "Invalid credentials"
        )
    # Here to create a token
    access_token = oath2.create_access_token(data={"user_id":user.id})
    # returning the token
    return {"access_token":access_token,"token_type":"bearer"}