from datetime import datetime
import json
import os

class PolicyEngine:
    def __init__(self, policy_file='data/policies.json'):
        self.policy_file = policy_file
        self.policies = self.load_policies()

    def load_policies(self):
        if not os.path.exists(self.policy_file):
            return []
        with open(self.policy_file, 'r') as file:
            return json.load(file)

    def enforce_policy(self, partner_id, user_id, purpose):
        policy = self.get_policy(partner_id)
        if not policy:
            return False, "Policy not found"
        
        if self.is_policy_compliant(policy, user_id, purpose):
            return True, "Policy approved"
        return False, "Policy denied"

    def get_policy(self, partner_id):
        for policy in self.policies:
            if policy['partner_id'] == partner_id:
                return policy
        return None

    def is_policy_compliant(self, policy, user_id, purpose):
        # Implement compliance checks based on policy rules
        allowed_purposes = policy.get('allowed_purposes', [])
        if purpose not in allowed_purposes:
            return False
        
        # Additional checks can be added here
        return True

    def log_policy_decision(self, partner_id, user_id, purpose, decision):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "partner_id": partner_id,
            "user_id": user_id,
            "purpose": purpose,
            "decision": decision
        }
        self.append_to_log(log_entry)

    def append_to_log(self, log_entry):
        log_file = 'data/policy_logs.json'
        if not os.path.exists(log_file):
            with open(log_file, 'w') as file:
                json.dump([], file)
        
        with open(log_file, 'r+') as file:
            logs = json.load(file)
            logs.append(log_entry)
            file.seek(0)
            json.dump(logs, file)