class AuditLog:
    def __init__(self, user_id, partner_id, purpose, data_accessed):
        self.user_id = user_id
        self.partner_id = partner_id
        self.purpose = purpose
        self.data_accessed = data_accessed
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "partner_id": self.partner_id,
            "purpose": self.purpose,
            "data_accessed": self.data_accessed,
            "timestamp": self.timestamp.isoformat()
        }