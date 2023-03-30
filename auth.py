from fastapi import FastAPI , APIRouter , Depends , HTTPException , Response ,status
from sqlalchemy.orm import Session
from .. import oauth2 , database , schemas , models , utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..import database,schemas,utils,models

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):

    # Creating a schema - UserLogin , so that users enters details in proper format 
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # finding the user with the particular email
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"invalid credentials")

    if not utils.verify(user_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"invalid credentials")
    # from utils folder , calling "verify" function to verify hashed and plain password

    # from oauth2 file calling create_access_token which returns user_id
    token = oauth2.create_acess_token(data = {"user_id" : user.id})
    return {"access_token":token , "token-type":"bearer"}
    

  