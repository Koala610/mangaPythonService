import unittest
import config
import src.logger as logger
from src.repository.mysql.user_repository import UserRepository
from src.entity.user import User

class TestUserRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.user_repository = UserRepository(User, config.DSN)

    def test_delete_user(self) -> None:
        cnt = self.user_repository.count()
        user = self.user_repository.create(name="test", user_id=123)
        self.user_repository.delete_by_id(user.user_id)
        new_cnt = self.user_repository.count()
        self.assertEqual(new_cnt, cnt)

    def test_create_user(self) -> None:
        cnt = self.user_repository.count()
        user = self.user_repository.create(name="testtest", user_id=123)
        new_cnt = self.user_repository.count()
        self.assertEqual(cnt+1, new_cnt)
        self.user_repository.delete_by_id(user.user_id)
        del user

    def test_update_user(self) -> None:
        user = self.user_repository.create(name="test", user_id=123)
        id = user.user_id
        self.user_repository.update(id=id, name="test123123")
        new_user = self.user_repository.find_by_id(id)
        self.assertEqual(new_user.name, "test123")
        self.user_repository.delete_by_id(id)