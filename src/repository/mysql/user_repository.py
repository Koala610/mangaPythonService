from .crud_repository import CRUDRepository
from typing import Type
from ...entity.database_object import DatabaseObject

class UserRepository(CRUDRepository):
    def __init__(self, Object: Type[DatabaseObject], db_credentials: dict):
        super().__init__(Object, db_credentials)


def main():
   repo = UserRepository() 

if __name__ == "__main__":
    main()