from src.repository.mysql import user_repository

def get_users():
    users = user_repository.find_all()
    return users