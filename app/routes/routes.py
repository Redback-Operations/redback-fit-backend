# /api/routes.py
from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/test', methods=['GET'])
def test_endpoint():
    print("hit")
    return jsonify({"message": "Hello, API!"})
