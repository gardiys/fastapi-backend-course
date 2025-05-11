from authx import AuthX
from models import UserLogin
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from settings import config

auth = AuthX(config=config)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users = {}

#Извлекаем токен из заголовка
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Зависимость для авторизации
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        #Верификация токена
        user = auth.get_current_subject(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) 

#Функция для логина
def login(user: UserLogin):
    hashed_password = fake_users.get(user.username)
    if not hashed_password or not pwd_context.verify(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = auth.create_access_token(uid=user.username)
    return {"access_token": token, "token_type": "Bearer"}

#Функция для регистрации
def register(user: UserLogin):
    if user.username in fake_users:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    fake_users[user.username] = hashed_password
    return {"msg": "User registered successfully"}

