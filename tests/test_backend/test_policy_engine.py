import pytest
from backend.services.policy_engine import PolicyEngine

@pytest.fixture
def policy_engine():
    return PolicyEngine()

def test_add_policy(policy_engine):
    policy = {
        "id": "policy_1",
        "name": "Test Policy",
        "rules": []
    }
    policy_engine.add_policy(policy)
    assert policy_engine.get_policy("policy_1") == policy

def test_remove_policy(policy_engine):
    policy = {
        "id": "policy_2",
        "name": "Test Policy 2",
        "rules": []
    }
    policy_engine.add_policy(policy)
    policy_engine.remove_policy("policy_2")
    assert policy_engine.get_policy("policy_2") is None

def test_enforce_policy(policy_engine):
    policy = {
        "id": "policy_3",
        "name": "Test Policy 3",
        "rules": [{"action": "allow", "resource": "data"}]
    }
    policy_engine.add_policy(policy)
    result = policy_engine.enforce_policy("policy_3", {"resource": "data"})
    assert result is True

def test_enforce_policy_denied(policy_engine):
    policy = {
        "id": "policy_4",
        "name": "Test Policy 4",
        "rules": [{"action": "deny", "resource": "data"}]
    }
    policy_engine.add_policy(policy)
    result = policy_engine.enforce_policy("policy_4", {"resource": "data"})
    assert result is False

def test_get_all_policies(policy_engine):
    policy1 = {"id": "policy_5", "name": "Test Policy 5", "rules": []}
    policy2 = {"id": "policy_6", "name": "Test Policy 6", "rules": []}
    policy_engine.add_policy(policy1)
    policy_engine.add_policy(policy2)
    all_policies = policy_engine.get_all_policies()
    assert len(all_policies) == 2
    assert policy1 in all_policies
    assert policy2 in all_policies