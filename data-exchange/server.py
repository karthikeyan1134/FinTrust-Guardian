from socket import socket, AF_INET, SOCK_STREAM
import json
import threading

class DataVaultServer:
    def __init__(self, host='localhost', port=9999):
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        print(f"Data Vault Server running on {host}:{port}")

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            print(f"Received request: {request}")
            response = self.process_request(request)
            client_socket.sendall(response.encode('utf-8'))
        finally:
            client_socket.close()

    def process_request(self, request):
        # Here you would implement the logic to handle the request
        # For now, we will just echo back the request
        return json.dumps({"status": "success", "data": request})

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = DataVaultServer()
    server.start()