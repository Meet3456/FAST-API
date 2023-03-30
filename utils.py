from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

# function that converts normal password into hashed password:
def hash(password:str):
    return pwd_context.hash(password)

def verify(pLain_password , hashed_password):
    return pwd_context.verify(pLain_password,hashed_password)