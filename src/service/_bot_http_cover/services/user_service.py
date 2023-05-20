from src.repository.mysql import user_repository

def get_users():
    users = user_repository.find_all()
    return users

def get_users_in_range(offset: int, limit: int):
    users = user_repository.find_in_range(offset=offset, limit=limit)
    return users

def get_user_by_id(user_id: str):
    user = user_repository.find_by_id(user_id)
    return user