# /api/routes.py
from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

@api.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "Hello, API!"})
