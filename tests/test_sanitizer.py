import unittest
from app.utils.sanitize import sanitize_id_no

class TestSanitizer(unittest.TestCase):
    def test_removes_non_digits(self):
        self.assertEqual(sanitize_id_no("AB12C034"), "12034")
        self.assertEqual(sanitize_id_no("00X1Y2"), "0012")
        self.assertEqual(sanitize_id_no("999"), "999")
        self.assertEqual(sanitize_id_no("A"), "")

if __name__ == "__main__":
    unittest.main()
