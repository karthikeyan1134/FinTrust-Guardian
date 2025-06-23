# Configuration settings for the data exchange

HOST = 'localhost'
PORT = 9999
TOKEN_EXPIRY = 300  # Token expiry time in seconds
MAX_CONNECTIONS = 5  # Maximum number of simultaneous connections

# Encryption settings
ENCRYPTION_KEY = b'your-encryption-key'  # Replace with your actual encryption key
AES_BLOCK_SIZE = 16  # AES block size in bytes

# Logging settings
LOG_FILE = 'data_exchange.log'  # Log file for data exchange activities
LOG_LEVEL = 'INFO'  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)