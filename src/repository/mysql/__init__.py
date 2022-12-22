from src.config import DSN
from src.entity.user import User
from .user_repository import UserRepository

user_repository = UserRepository(User, DSN)