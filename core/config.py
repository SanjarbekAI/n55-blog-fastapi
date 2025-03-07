import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

conf = ConnectionConfig(
    MAIL_USERNAME="sanjarbekwork@gmail.com",
    MAIL_PASSWORD="llzc ngfi szjs djeh",
    MAIL_FROM="sanjarbekwork@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="N55 blog api",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)