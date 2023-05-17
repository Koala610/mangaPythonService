import src.logger as logger
from .crud_repository import CRUDRepository
from typing import Type
from ...entity.protocol.entity_protocol import DatabaseEntity
from src.entity.user import User

class UserRepository(CRUDRepository):
    def __init__(self, Object: Type[DatabaseEntity], dsn: str):
        super().__init__(Object, dsn)
        logger.info("UserRepository initialized...")
    
    def check_if_subscribed(self, user_id):
        user = self.find_by_id(user_id)
        return True if user.is_subscribed else False

    def check_if_support(self, user_id):
        with self.Session() as session:
            user = session.query(self.Object).get(user_id)
            return True if user.support else False

    def find_by_subscription(self, is_subscribed) -> object:
        with self.Session() as session:
            users = session.query(self.Object).filter_by(is_subscribed=is_subscribed).all()
            return users


def main():
    pass

if __name__ == "__main__":
    main()