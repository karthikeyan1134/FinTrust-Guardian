from datetime import datetime
import json
import os

class AuditService:
    def __init__(self, audit_log_file='backend/data/audit_logs.json'):
        self.audit_log_file = audit_log_file
        self.ensure_audit_log_exists()

    def ensure_audit_log_exists(self):
        if not os.path.exists(self.audit_log_file):
            with open(self.audit_log_file, 'w') as f:
                json.dump([], f)

    def log_access(self, user_id, partner_id, purpose, data_accessed):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "partner_id": partner_id,
            "purpose": purpose,
            "data_accessed": data_accessed
        }
        self.append_log_entry(log_entry)

    def append_log_entry(self, log_entry):
        with open(self.audit_log_file, 'r+') as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=4)

    def get_audit_logs(self):
        with open(self.audit_log_file, 'r') as f:
            return json.load(f)