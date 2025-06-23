from flask import Blueprint, request, jsonify
from backend.services.policy_engine import PolicyEngine
from backend.utils.token_generator import generate_token

auth_bp = Blueprint('auth', __name__)
policy_engine = PolicyEngine()

@auth_bp.route('/authorize', methods=['POST'])
def authorize():
    data = request.get_json()
    partner_id = data.get('partner_id')
    user_id = data.get('user_id')
    purpose = data.get('purpose')

    if not partner_id or not user_id or not purpose:
        return jsonify({"error": "Missing required fields"}), 400

    # Check policy and generate token
    if policy_engine.is_authorized(partner_id, user_id, purpose):
        token = generate_token(user_id)
        return jsonify({
            "status": "approved",
            "token": token,
            "exchange_host": "localhost",
            "exchange_port": 9999,
            "expires_in": 300
        }), 200
    else:
        return jsonify({"status": "denied"}), 403