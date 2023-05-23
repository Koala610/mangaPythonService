import jwt

from datetime import datetime, timedelta
from src.core_entity.user import Admin
from src.config import SECRET_KEY

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

def generate_refresh_token(admin: Admin):
    refresh_token_expiration_time =datetime.utcnow() + timedelta(days=30)
    refresh_token_payload = {
        "username": admin.username,
        "password": admin.password,
        'exp': refresh_token_expiration_time
    }
    return jwt.encode(refresh_token_payload, SECRET_KEY, algorithm='HS256')

def verify_jwt(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
                 return None
        except jwt.exceptions.PyJWTError:
            return None
        return payload