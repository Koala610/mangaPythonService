from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Type
from ...entity.database_object import DatabaseObject


class CRUDRepository:
    def __init__(self, Object: Type[DatabaseObject], dsn: str):
        self.engine = create_engine(dsn)
        self.Session = sessionmaker(bind=self.engine)
        self.Object = Object

    def create(self, **kwargs):
        valid_kwargs = {k: v for k,
                        v in kwargs.items() if k in self.Object.__dict__}
        with self.Session() as session:
            user = self.Object(**valid_kwargs)
            session.add(user)
            session.commit()

    def find_by_id(self, id):
        with self.Session() as session:
            user = session.query(self.Object).get(id)
        return user

    def update(self, id, **kwargs):
        valid_kwargs = {k: v for k,
                        v in kwargs.items() if k in self.Object.__dict__}
        with self.Session() as session:
            user = session.query(self.Object).get(id)
            user = self.Object(user, **valid_kwargs)
            session.commit()

    def delete_by_id(self, id):
        with self.Session() as session:
            user = session.query(self.Object).get(id)
            session.delete(user)
            session.commit()
