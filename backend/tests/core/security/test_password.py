import unittest
from app.core.security.password import verify_password, get_password_hash

class TestPassword(unittest.TestCase):
    def test_get_password_hash_and_verify(self):
        password = "test_password"
        hashed_password = get_password_hash(password)

        self.assertNotEqual(password, hashed_password)
        self.assertTrue(verify_password(password, hashed_password))

    def test_verify_password_incorrect(self):
        password = "test_password"
        hashed_password = get_password_hash(password)

        self.assertFalse(verify_password("wrong_password", hashed_password))

if __name__ == '__main__':
    unittest.main()
