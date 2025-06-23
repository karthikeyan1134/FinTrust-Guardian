class TokenValidator:
    def __init__(self, valid_tokens):
        self.valid_tokens = valid_tokens

    def is_valid(self, token):
        """Check if the provided token is valid."""
        return token in self.valid_tokens

    def is_expired(self, token):
        """Check if the provided token has expired."""
        # Placeholder for expiration logic
        return False

    def validate(self, token):
        """Validate the token and return its status."""
        if self.is_expired(token):
            return {"status": "error", "message": "Token has expired"}
        if self.is_valid(token):
            return {"status": "success", "message": "Token is valid"}
        return {"status": "error", "message": "Invalid token"}