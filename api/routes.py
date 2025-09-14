from flask import Blueprint, jsonify, request
from flask_login import login_required
import time

api = Blueprint('api', __name__)

@api.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "Hello, API!"})


@api.route("/time-sync", methods=["GET", "POST"])
@login_required              # keep if you want it behind login
def time_sync():
    # GET: simple “what time is it on the server?”
    if request.method == "GET":
        return jsonify({"server_time": int(time.time())}), 200

    # POST: minimal schema check (adjust later as your design evolves)
    body = request.get_json(silent=True) or {}
    device_id = body.get("device_id")
    readings  = body.get("readings")
    if not isinstance(device_id, str) or not isinstance(readings, list):
        return jsonify({"error": "invalid request"}), 400

    # TODO: store/process readings here if needed
    return jsonify({"server_time": int(time.time())}), 200