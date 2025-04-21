from flask import Blueprint, jsonify, send_from_directory, current_app, abort
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'Monitor module is running!'})

@monitor_bp.route('/model_compare', methods=['GET'])
def compare_page():
    # print(os.path.abspath(os.path.join(current_app.root_path, '..', '..', 'frontend')))
    frontend_path = os.path.abspath(os.path.join(current_app.root_path, '..', '..', 'frontend'))
    full_path = os.path.join(frontend_path, 'model_compare.html')
    # print("完整路径为：", full_path)
    # print(">>> File exists:", os.path.isfile(full_path))
    if not os.path.isfile(full_path):
        abort(404)
    return send_from_directory(frontend_path, 'model_compare.html')

@monitor_bp.route('/model_metrics', methods=['GET'])
def get_model_metrics():
    from data_processing.metrics_storage import get_model_metrics as fetch_model_metrics
    return jsonify(fetch_model_metrics())