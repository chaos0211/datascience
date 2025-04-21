from flask import Blueprint, jsonify

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Monitor module is running!'})