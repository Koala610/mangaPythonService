from ..config import DSN
from src.core_repository.user_repository import UserRepository
from src.core_repository.admin_repository import AdminRepository
from src.core_repository.crud_repository import CRUDRepository

user_repository = UserRepository(DSN)
admin_repository = AdminRepository(DSN)