from flask import Blueprint, jsonify, send_from_directory, current_app, abort
import os, sys
from app import db
from app.models.sentiment import EventComment, SentimentResult
import pandas as pd
import logging
from sqlalchemy import func

logging.basicConfig(level=logging.INFO, filename='trend.log')
logger = logging.getLogger(__name__)

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


@monitor_bp.route('/trend/<int:event_id>', methods=['GET'])
def trend_data(event_id):
    try:
        # 获取 event_id 对应的 event_name
        event = db.session.query(EventComment.event_name).filter(EventComment.id == event_id).first()
        if not event:
            logger.warning(f"No event found for event_id: {event_id}")
            return jsonify({"dates": [], "positive": [], "negative": []}), 200

        event_name = event.event_name
        # 查询所有同 event_name 的 SentimentResult
        results = db.session.query(SentimentResult.comment_date, SentimentResult.sentiment).join(
            EventComment, SentimentResult.event_id == EventComment.id
        ).filter(EventComment.event_name == event_name).all()

        if not results:
            logger.warning(f"No data found for event_name: {event_name}")
            return jsonify({"dates": [], "positive": [], "negative": []}), 200

        # 转换为 DataFrame
        data = [{"comment_date": r.comment_date, "sentiment": r.sentiment} for r in results]
        df = pd.DataFrame(data)
        logger.info(f"Retrieved {len(df)} records for event_name: {event_name}")

        # 按日期分组，计算正/负面百分比
        df["date"] = pd.to_datetime(df["comment_date"]).dt.date
        trend_data = df.groupby("date")["sentiment"].value_counts(normalize=True).unstack().fillna(0) * 100

        # 返回 JSON
        response = {
            "dates": trend_data.index.astype(str).tolist(),
            "positive": trend_data[1].tolist() if 1 in trend_data.columns else [0] * len(trend_data),
            "negative": trend_data[0].tolist() if 0 in trend_data.columns else [0] * len(trend_data)
        }
        logger.info(f"Trend data for event_id {event_id} (event_name: {event_name}): {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error processing trend for event_id {event_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@monitor_bp.route('/events', methods=['GET'])
def get_events():
    try:
        # 按 event_name 分组，取最小的 id
        events = db.session.query(
            func.min(EventComment.id).label('id'),
            EventComment.event_name
        ).group_by(EventComment.event_name).all()
        if not events:
            return jsonify({"events": []}), 200
        return jsonify({
            "events": [{"id": event.id, "name": event.event_name} for event in events]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500