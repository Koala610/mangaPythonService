from src.config import DSN
from src.entity.user import User, Admin
from .user_repository import UserRepository
from .admin_repository import AdminRepository

user_repository = UserRepository(User, DSN)
admin_repository = AdminRepository(Admin, DSN)