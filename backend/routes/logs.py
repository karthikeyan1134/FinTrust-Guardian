from flask import Blueprint, jsonify
from backend.utils import validators
import json

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/logs', methods=['GET'])
def get_audit_logs():
    try:
        with open('backend/data/audit_logs.json') as f:
            audit_logs = json.load(f)
        return jsonify(audit_logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@logs_bp.route('/logs/<user_id>', methods=['GET'])
def get_user_logs(user_id):
    try:
        with open('backend/data/audit_logs.json') as f:
            audit_logs = json.load(f)
        
        user_logs = [log for log in audit_logs if log['user_id'] == user_id]
        return jsonify(user_logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500