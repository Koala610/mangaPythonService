import hashlib

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, DataError
from typing import Type, Optional
from core_entity.protocol.entity_protocol import DatabaseEntity
from core_logger import logger


class CRUDRepository:
    def __init__(self, Object: Type[DatabaseEntity], dsn: str):
        self.engine = create_engine(dsn)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.Object = Object

    @classmethod
    def get_password_hash(cls, password: str) -> int:
        h = hashlib.md5()
        h.update(password.encode())
        return int(h.hexdigest(), 16)

    def find_all(self):
        with self.Session() as session:
            objects = session.query(self.Object).all()
            return objects

    def create(self,**kwargs) -> Optional[object]:
        valid_args = {key: value for key, value in kwargs.items() if key in self.validate_arguments(**kwargs)}
        with self.Session() as session:
            user = self.Object(**valid_args)
            session.add(user)
            try:
                session.commit()
            except RuntimeError as e:
                logger.critical(f"{str(e)}")
                return None
            return user

    def find_by_id(self, id) -> object:
        with self.Session() as session:
            user = session.query(self.Object).get(id)
            return user

    def update(self, id, **kwargs):
        valid_keys = self.validate_arguments(**kwargs)
        valid_args = {key:kwargs[key] for key in valid_keys}
        with self.Session() as session:
            try:
                session.query(self.Object).filter_by(id=id).update(valid_args)
                session.expire_all()
                session.commit()
            except IntegrityError or DataError as e:
                raise Exception(f"Can not update entity with id {id}")

    def delete_by_id(self, id):
        with self.Session() as session:
            user = self.find_by_id(id)
            session.delete(user)
            session.commit()

    def count(self) -> int:
        with self.Session() as session:
            cnt = session.query(func.count(self.Object.id)).scalar()
            return cnt

    def validate_arguments(self, **kwargs):
        valid_keys = set(arg for arg in kwargs if arg in self.Object.__table__.columns)
        invalid_keys = set(kwargs.keys()) - valid_keys
        if invalid_keys:
            raise ValueError(f'Invalid keys: {invalid_keys}')
        return valid_keys
    
    def find_in_range(self, offset, limit):
        with self.Session() as session:
            return session.query(self.Object).offset(offset).limit(limit).all()