class SocketHandler:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.socket = None

    def create_socket(self):
        import socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def accept_connection(self):
        conn, addr = self.socket.accept()
        print(f"Connection established with {addr}")
        return conn, addr

    def send_data(self, conn, data):
        conn.sendall(data)

    def receive_data(self, conn, buffer_size=1024):
        return conn.recv(buffer_size)

    def close_connection(self, conn):
        conn.close()

    def close_socket(self):
        if self.socket:
            self.socket.close()