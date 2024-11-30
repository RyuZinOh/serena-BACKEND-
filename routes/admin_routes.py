from flask import Blueprint, jsonify
from flask_cors import CORS
from middlewares.is_admin import is_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
CORS(admin_bp)

@admin_bp.route('/test', methods=['GET'])
@is_admin
def test_admin_route():
    return {'message': 'This is a protected admin route.'}, 200
