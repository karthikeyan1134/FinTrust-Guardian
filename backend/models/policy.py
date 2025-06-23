class Policy:
    def __init__(self, policy_id, partner_id, data_usage_rules, consent_required):
        self.policy_id = policy_id
        self.partner_id = partner_id
        self.data_usage_rules = data_usage_rules
        self.consent_required = consent_required

    def is_consent_required(self):
        return self.consent_required

    def __repr__(self):
        return f"<Policy(policy_id={self.policy_id}, partner_id={self.partner_id})>"


class PolicyManager:
    def __init__(self):
        self.policies = {}

    def add_policy(self, policy):
        self.policies[policy.policy_id] = policy

    def get_policy(self, policy_id):
        return self.policies.get(policy_id)

    def remove_policy(self, policy_id):
        if policy_id in self.policies:
            del self.policies[policy_id]

    def list_policies(self):
        return list(self.policies.values())