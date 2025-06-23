import pytest
from flask import json
from backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_authorize_success(client):
    response = client.post('/authorize', json={
        "partner_id": "partner_ABC",
        "user_id": "user_123",
        "purpose": "loan_application"
    })
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['status'] == 'approved'
    assert 'token' in data
    assert 'exchange_host' in data
    assert 'exchange_port' in data
    assert 'expires_in' in data

def test_authorize_failure(client):
    response = client.post('/authorize', json={
        "partner_id": "invalid_partner",
        "user_id": "user_123",
        "purpose": "loan_application"
    })
    data = json.loads(response.data)
    assert response.status_code == 403
    assert data['status'] == 'denied'

def test_authorize_missing_fields(client):
    response = client.post('/authorize', json={
        "partner_id": "partner_ABC",
        "purpose": "loan_application"
    })
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Missing user_id field'