from .crud_repository import CRUDRepository
from core_entity.user import User
from typing import List, Optional
from core_logger import logger

class UserRepository(CRUDRepository):
    def __init__(self, dsn: str):
        super().__init__(User, dsn)
        logger.info("UserRepository initialized...")
    
    def check_if_subscribed(self, user_id)-> bool:
        user = self.find_by_id(user_id)
        return True if user.is_subscribed else False

    def check_if_support(self, user_id)-> bool:
        with self.Session() as session:
            user = session.query(self.Object).get(user_id)
            return True if user.support else False

    def find_by_subscription(self, is_subscribed) -> List[User]:
        with self.Session() as session:
            users = session.query(self.Object).filter_by(is_subscribed=is_subscribed).all()
            return users
    
    def find_user_support_id(self, user_id)-> Optional[int]:
        with self.Session() as session:
            user = session.query(self.Object).get(user_id)
            if len(user.support) == 0:
                return None
            return user.support[0].id


def main():
    pass

if __name__ == "__main__":
    main()