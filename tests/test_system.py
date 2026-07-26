import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import initialize_database, authenticate_user, add_student, get_all_students


class CoachingSystemTests(unittest.TestCase):
    def test_database_initialization(self):
        db_path = initialize_database()
        self.assertTrue(os.path.exists(db_path))

    def test_admin_login(self):
        self.assertTrue(authenticate_user("admin", "admin123"))

    def test_student_creation_and_listing(self):
        student_id = add_student("Asha", "12", "Science", "9876543210")
        self.assertIsNotNone(student_id)
        students = get_all_students()
        self.assertTrue(any(s[1] == "Asha" for s in students))


if __name__ == "__main__":
    unittest.main()
