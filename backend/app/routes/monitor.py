from flask import Blueprint, jsonify, send_from_directory, current_app

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Monitor module is running!'})

@monitor_bp.route('/model_compare', methods=['GET'])
def compare_page():
    return send_from_directory(current_app.static_folder, 'model_compare.html')