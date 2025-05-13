from authx import AuthX, AuthXConfig
from models import UserLogin
from fastapi import HTTPException, Response

config = AuthXConfig()
config.JWT_SECRET_KEY = "ANTON_SCHERBAK"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

