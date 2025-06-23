import pytest
import requests

BASE_URL = "http://localhost:5000"

def test_full_workflow():
    # Step 1: Authorize partner
    response = requests.post(f"{BASE_URL}/authorize", json={
        "partner_id": "partner_ABC",
        "user_id": "user_123",
        "purpose": "loan_application"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    token = response.json()["token"]
    
    # Step 2: Secure data retrieval
    data_response = requests.get(f"{BASE_URL}/data", headers={
        "Authorization": f"Bearer {token}"
    })
    assert data_response.status_code == 200
    assert "sensitive_data" in data_response.json()

    # Step 3: Check audit logs
    logs_response = requests.get(f"{BASE_URL}/logs")
    assert logs_response.status_code == 200
    assert len(logs_response.json()) > 0

    # Step 4: Validate compliance dashboard
    compliance_response = requests.get("http://localhost:3000/compliance")
    assert compliance_response.status_code == 200
    assert "data_sharing_activity" in compliance_response.json()