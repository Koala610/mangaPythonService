import src.logger as logger
from .crud_repository import CRUDRepository
from typing import Type
from ...entity.protocol.entity_protocol import DatabaseEntity

class UserRepository(CRUDRepository):
    def __init__(self, Object: Type[DatabaseEntity], dsn: str):
        super().__init__(Object, dsn)
        logger.info("UserRepository initialized...")
    
    def check_if_subscribed(self, user_id):
        user = self.find_by_id(user_id)
        return True if user.is_subscribed else False


def main():
    pass

if __name__ == "__main__":
    main()