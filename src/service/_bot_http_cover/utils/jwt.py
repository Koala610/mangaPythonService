import jwt

from datetime import datetime, timedelta
from src.entity.user import Admin
from src.config import SECRET_KEY
from src.logger import logger

def generate_token(admin: Admin):
    if admin is None:
        raise ValueError("Cannot generate a token for an anonymous user")
    exp_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "exp": exp_time,
        "username": admin.username,
        "password": admin.password
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_jwt(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.PyJWTError:
            return None
        return payload