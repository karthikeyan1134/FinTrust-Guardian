import socket
import json
import sys

def connect_to_data_vault(host, port, token):
    try:
        # Create a socket connection to the data vault server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            print("Connected to data vault.")

            # Send the token for authentication
            s.sendall(token.encode())
            response = s.recv(1024).decode()
            print("Response from server:", response)

            # If the response is valid, proceed to request data
            if response == "Token accepted":
                request_data(s)
            else:
                print("Invalid token. Exiting.")
                sys.exit(1)

    except Exception as e:
        print(f"Error connecting to data vault: {e}")
        sys.exit(1)

def request_data(socket):
    # Example request for data
    request = {
        "action": "retrieve_data",
        "parameters": {
            "user_id": "user_123"
        }
    }
    socket.sendall(json.dumps(request).encode())
    response = socket.recv(4096).decode()
    print("Data received:", response)

if __name__ == "__main__":
    # Configuration for the data vault connection
    DATA_VAULT_HOST = "localhost"
    DATA_VAULT_PORT = 9999
    TOKEN = sys.argv[1] if len(sys.argv) > 1 else None

    if TOKEN is None:
        print("Usage: python client.py <token>")
        sys.exit(1)

    connect_to_data_vault(DATA_VAULT_HOST, DATA_VAULT_PORT, TOKEN)