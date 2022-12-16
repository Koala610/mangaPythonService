import src.logger as logger
from .crud_repository import CRUDRepository
from typing import Type
from ...entity.protocol.database_object import DatabaseObject

class UserRepository(CRUDRepository):
    def __init__(self, Object: Type[DatabaseObject], dsn: str):
        super().__init__(Object, dsn)
        logger.logger.info("UserRepository initialized...")


def main():
    pass

if __name__ == "__main__":
    main()