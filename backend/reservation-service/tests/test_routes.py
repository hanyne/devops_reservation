import unittest
from app import create_app, db
import json

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nothing123@db:5432/reservation_db'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login(self):
        response = self.client.post('/auth/login', json={'username': 'admin', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

if __name__ == '__main__':
    unittest.main()