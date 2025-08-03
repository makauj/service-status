import unittest
from app.db import get_connection

class DBTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Cleanup data after each test
        self.cursor.execute("DELETE FROM Collection")
        self.cursor.execute("DELETE FROM Production")
        self.cursor.execute("DELETE FROM Users")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
