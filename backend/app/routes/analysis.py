from flask import Blueprint, request, jsonify
from app.services.sentiment_service import analyze_sentiment

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data['text']
    result = analyze_sentiment(text)
    return jsonify(result)

