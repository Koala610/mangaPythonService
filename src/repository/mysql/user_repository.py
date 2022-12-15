from .crud_repository import CRUDRepository
from typing import Type
from ...entity.database_object import DatabaseObject

class UserRepository(CRUDRepository):
    def __init__(self, Object: Type[DatabaseObject], dsn: str):
        super().__init__(Object, dsn)


def main():
    pass

if __name__ == "__main__":
    main()