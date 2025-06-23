def validate_user_id(user_id):
    if not isinstance(user_id, str) or len(user_id) == 0:
        raise ValueError("Invalid user ID: must be a non-empty string.")
    return True

def validate_partner_id(partner_id):
    if not isinstance(partner_id, str) or len(partner_id) == 0:
        raise ValueError("Invalid partner ID: must be a non-empty string.")
    return True

def validate_purpose(purpose):
    valid_purposes = ["loan_application", "credit_scoring", "regulatory_reporting", "third_party_integration"]
    if purpose not in valid_purposes:
        raise ValueError(f"Invalid purpose: must be one of {valid_purposes}.")
    return True

def validate_request_data(request_data):
    if not isinstance(request_data, dict):
        raise ValueError("Request data must be a dictionary.")
    
    required_fields = ["partner_id", "user_id", "purpose"]
    for field in required_fields:
        if field not in request_data:
            raise ValueError(f"Missing required field: {field}")
    
    validate_partner_id(request_data["partner_id"])
    validate_user_id(request_data["user_id"])
    validate_purpose(request_data["purpose"])
    
    return True