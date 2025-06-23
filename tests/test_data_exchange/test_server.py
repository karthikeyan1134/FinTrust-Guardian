import unittest
from data_exchange.server import app

class TestDataVaultServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def test_server_running(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_data_exchange_endpoint(self):
        response = self.app.post('/data-exchange', json={'data': 'test_data'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.get_json())

    def test_invalid_token(self):
        response = self.app.post('/data-exchange', headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()