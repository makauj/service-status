from tests.base_test import DBTestCase
from app.models.collection import insert_collection, fetch_collections

class TestCollection(DBTestCase):
    def test_insert_and_fetch_collection(self):
        insert_collection("TEST125", "Tester", "0712345678", "tester@example.com")
        collections = fetch_collections()
        self.assertTrue(any(c["ID No"] == "125" for c in collections))
        self.assertTrue(any(c["collected_by"] == "Tester" for c in collections))
        self.assertTrue(any(c["phone_no"] == "0712345678" for c in collections))