# FinTrust Guardian Demo Workflow Script

import requests
import time

def authorize_partner(partner_id, user_id, purpose):
    response = requests.post("http://localhost:5000/authorize", json={
        "partner_id": partner_id,
        "user_id": user_id,
        "purpose": purpose
    })
    return response.json()

def retrieve_data(token):
    response = requests.get(f"http://localhost:9999/data", headers={"Authorization": f"Bearer {token}"})
    return response.json()

def main():
    print("Starting FinTrust Guardian Demo Workflow...\n")
    
    # Step 1: Authorize Partner
    partner_id = "partner_ABC"
    user_id = "user_123"
    purpose = "loan_application"
    
    print("Authorizing partner...")
    auth_response = authorize_partner(partner_id, user_id, purpose)
    print("Authorization Response:", auth_response)
    
    if auth_response.get("status") == "approved":
        token = auth_response.get("token")
        print("Token received:", token)
        
        # Step 2: Wait for a moment before data retrieval
        time.sleep(2)
        
        # Step 3: Retrieve Data
        print("Retrieving data...")
        data_response = retrieve_data(token)
        print("Data Retrieved:", data_response)
    else:
        print("Authorization failed. Exiting demo.")

if __name__ == "__main__":
    main()