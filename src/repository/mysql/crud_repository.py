import src.logger as logger

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from typing import Type, Optional
from ...entity.protocol.entity_protocol import DatabaseEntity


class CRUDRepository:
    def __init__(self, Object: Type[DatabaseEntity], dsn: str):
        self.engine = create_engine(dsn)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.Object = Object

    def create(self,**kwargs) -> int:
        valid_args = {key: value for key, value in kwargs.items() if key in self.validate_arguments(**kwargs)}
        with self.Session() as session:
            user = self.Object(**valid_args)
            session.add(user)
            try:
                session.commit()
            except RuntimeError as e:
                logger.logger.critical(f"{str(e)}")
                return None
            return user

    def find_by_id(self, id) -> object:
        with self.Session() as session:
            user = session.query(self.Object).get(id)
            return user

    def find_by_subscription(self, is_subscribed) -> object:
        with self.Session() as session:
            users = session.query(self.Object).filter_by(is_subscribed=is_subscribed).all()
            return users

    def update(self, id, **kwargs):
        valid_keys = self.validate_arguments(**kwargs)
        valid_args = {key:kwargs[key] for key in valid_keys}
        with self.Session() as session:
            session.query(self.Object).filter_by(user_id=id).update(valid_args)
            session.expire_all()
            session.commit()

    def delete_by_id(self, id):
        with self.Session() as session:
            user = self.find_by_id(id)
            session.delete(user)
            session.commit()

    def count(self) -> int:
        with self.Session() as session:
            cnt = session.query(func.count(self.Object.user_id)).scalar()
            return cnt

    def validate_arguments(self, **kwargs):
        valid_keys = set(arg for arg in kwargs if arg in self.Object.__table__.columns)
        invalid_keys = set(kwargs.keys()) - valid_keys
        if invalid_keys:
            raise ValueError(f'Invalid keys: {invalid_keys}')
        return valid_keys