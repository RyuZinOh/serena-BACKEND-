from flask import Blueprint, request, jsonify
from flask_cors import CORS
import jwt
from services.currency_service import get_user_currency
from config import Config

currency_bp = Blueprint('currency', __name__, url_prefix='/currency')
CORS(currency_bp)


@currency_bp.route('/<user_id>/get', methods=['GET'])
def get_currency(user_id):
    token = request.headers.get('Authorization', "").replace("Bearer ", "")
    
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401

    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        logged_in_user_id = decoded_token.get('sub')
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

    if logged_in_user_id != user_id:
        return jsonify({'message': 'Unauthorized access!'}), 403

    currency_data = get_user_currency(user_id)
    if not currency_data:
        return jsonify({'message': 'Currency data not found!'}), 404

    return jsonify(currency_data), 200
