from .crud_repository import CRUDRepository
from typing import Optional
from core_entity.user import Admin
from core_logger import logger

class AdminRepository(CRUDRepository):
    def __init__(self, dsn: str):
        super().__init__(Admin, dsn)
        logger.info("AdminRepository initialized...")
    
    def create(self, **kwargs) -> Optional[object]:
        if kwargs.get("password"):
            kwargs["password"] = str(CRUDRepository.get_password_hash(password=kwargs.get("password")))
        return super().create(**kwargs)

    def find_by_username_and_password(self, username: str, password: str, is_password_hashed: bool = False) -> object:
        if not is_password_hashed:
            password = str(CRUDRepository.get_password_hash(password=password))
        with self.Session() as session:
            user = session.query(self.Object).filter_by(username=username, password=password).first()
        return user

    def find_by_actial_jwt(self, jwt: str):
        with self.Session() as session:
            admin = session.query(self.Object).filter_by(actual_jwt=jwt).first()
            if admin is None:
                raise Exception("No such admin")
            return admin