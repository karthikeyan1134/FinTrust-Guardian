import pytest
from backend.services.data_masking import DataMasking

@pytest.fixture
def data_masking():
    return DataMasking()

def test_mask_sensitive_data(data_masking):
    sensitive_data = {
        "name": "John Doe",
        "ssn": "123-45-6789",
        "email": "john.doe@example.com"
    }
    masked_data = data_masking.mask(sensitive_data)
    
    assert masked_data["name"] == "John Doe"
    assert masked_data["ssn"] == "XXX-XX-6789"
    assert masked_data["email"] == "john.doe@example.com"

def test_tokenize_data(data_masking):
    sensitive_data = "Sensitive Information"
    token = data_masking.tokenize(sensitive_data)
    
    assert token is not None
    assert token != sensitive_data

def test_detokenize_data(data_masking):
    sensitive_data = "Sensitive Information"
    token = data_masking.tokenize(sensitive_data)
    detokenized_data = data_masking.detokenize(token)
    
    assert detokenized_data == sensitive_data

def test_mask_empty_data(data_masking):
    sensitive_data = {}
    masked_data = data_masking.mask(sensitive_data)
    
    assert masked_data == {}