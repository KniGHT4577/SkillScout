import unittest
from app.core.security.password import verify_password, get_password_hash

class TestPassword(unittest.IsolatedAsyncioTestCase):
    async def test_get_password_hash_and_verify(self):
        password = "test_password"
        hashed_password = await get_password_hash(password)

        self.assertNotEqual(password, hashed_password)
        self.assertTrue(await verify_password(password, hashed_password))

    async def test_verify_password_incorrect(self):
        password = "test_password"
        hashed_password = await get_password_hash(password)

        self.assertFalse(await verify_password("wrong_password", hashed_password))

if __name__ == '__main__':
    unittest.main()
