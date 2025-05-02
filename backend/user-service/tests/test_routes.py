import unittest
from app.main import app

class UserServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'healthy')

    def test_register_login(self):
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass'
        }
        res = self.app.post('/users/register', json=user_data)
        self.assertEqual(res.status_code, 201)
        res = self.app.post('/users/login', json=user_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', res.get_json())

if __name__ == '__main__':
    unittest.main()
