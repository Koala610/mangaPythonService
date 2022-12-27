from src.repository.mysql import admin_repository
from src.entity.user import Admin


def get_admin(username: str, password: str, is_password_hashed: bool = False) -> Admin:
    return admin_repository.find_by_username_and_password(username, password, is_password_hashed=is_password_hashed)

def update_jwt(id: int, jwt: str) -> None:
    admin_repository.update(id, actual_jwt=jwt)