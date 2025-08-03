from tests.base_test import DBTestCase
from app.models.users import insert_user, fetch_users

class TestUsers(DBTestCase):
    def test_insert_and_fetch_user(self):
        dummy_image = b'\x89PNG\r\n'
        insert_user("TEST123", "Test User", "1990-01-01", "2026-01-01 00:00:00", "0700111222", dummy_image)
        users = fetch_users()
        self.assertTrue(any(user["ID No"] == "123" for user in users))
