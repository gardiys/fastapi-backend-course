from dotenv import load_dotenv
from authx import AuthX, AuthXConfig
import os

load_dotenv()

config = AuthXConfig(
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY"),
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_TOKEN_EXPIRES=30,
    JWT_TOKEN_LOCATION=["headers"],
    JWT_HEADER_TYPE="Bearer",
    JWT_HEADER_NAME="Authorization",
    JWT_COOKIE_SECURE=False,
    JWT_COOKIE_CSRF_PROTECT=False
)