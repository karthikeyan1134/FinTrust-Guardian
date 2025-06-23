from unittest import TestCase
import socket
import json

class TestDataExchangeClient(TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.port = 9999
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tearDown(self):
        self.client_socket.close()

    def test_secure_data_retrieval(self):
        # Assuming the server is running and we have a valid token
        token = "valid_token_example"
        self.client_socket.connect((self.host, self.port))
        
        request_data = {
            "token": token,
            "request": "get_data"
        }
        
        self.client_socket.sendall(json.dumps(request_data).encode())
        response = self.client_socket.recv(4096)
        
        self.assertIsNotNone(response)
        response_data = json.loads(response.decode())
        self.assertEqual(response_data.get("status"), "success")
        self.assertIn("data", response_data)

    def test_invalid_token(self):
        self.client_socket.connect((self.host, self.port))
        
        request_data = {
            "token": "invalid_token",
            "request": "get_data"
        }
        
        self.client_socket.sendall(json.dumps(request_data).encode())
        response = self.client_socket.recv(4096)
        
        self.assertIsNotNone(response)
        response_data = json.loads(response.decode())
        self.assertEqual(response_data.get("status"), "error")
        self.assertEqual(response_data.get("message"), "Invalid token")