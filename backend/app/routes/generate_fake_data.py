from datetime import datetime, timedelta
import random
import logging
from flask import Blueprint, jsonify
from app import db
from app.models.sentiment import EventComment, SentimentResult
from app.services.sentiment_service import analyze_sentiment

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake_bp = Blueprint('fake_data', __name__)


def generate_fake_data_logic():
    # 定义两个事件
    events = [
        {"name": "TechPhone", "date": "2025-03-01"},
        {"name": "Movie", "date": "2025-03-02"}
    ]
    comment_templates = {
        1: [  # 正面
            "Love the {feature} of {event}, {adjective}!",
            "{event} is {adjective}, highly recommend!",
            "Really impressed with {event}'s {feature}!",
            "{event} exceeded my expectations, {adjective}!"
        ],
        0: [  # 负面
            "{issue} with {event}, so {adjective}!",
            "{event}’s {feature} is {adjective}, very disappointed.",
            "Not happy with {event}, {issue}.",
            "{event} was {adjective}, wouldn’t recommend."
        ]
    }
    features = ["camera", "battery", "design", "screen", "performance", "price", "software"]
    positive_adjectives = ["awesome", "fantastic", "great", "amazing", "excellent", "superb"]
    negative_adjectives = ["disappointing", "terrible", "frustrating", "bad", "poor", "awful"]
    issues = [
        "Battery drains fast", "Too expensive", "Shipping delayed",
        "Screen flickers", "Overheats", "Software glitches", "Poor quality"
    ]

    logger.info("Starting fake data generation")

    # 生成 30 天数据
    for day in range(30):
        date = datetime(2025, 3, 1) + timedelta(days=day)
        for _ in range(50):  # 每天50条
            event = random.choice(events)
            # 随机选择正面或负面（40% 正面，60% 负面）
            sentiment = random.choices([0, 1], weights=[0.60, 0.40], k=1)[0]
            template = random.choice(comment_templates[sentiment])
            comment = template.format(
                event=event["name"],
                feature=random.choice(features),
                adjective=random.choice(positive_adjectives if sentiment == 1 else negative_adjectives),
                issue=random.choice(issues) if sentiment == 0 else ""
            )

            # 创建 EventComment
            event_comment = EventComment(
                event_name=event["name"],
                event_date=datetime.strptime(event["date"], "%Y-%m-%d").date(),
                comment=comment,
                comment_date=datetime.strptime(
                    f"{date.strftime('%Y-%m-%d')} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00",
                    "%Y-%m-%d %H:%M:%S"
                )
            )
            db.session.add(event_comment)
            db.session.flush()

            # 创建 SentimentResult（直接使用随机 sentiment，避免 analyze_sentiment 偏差）
            sentiment_result = SentimentResult(
                event_id=event_comment.id,
                sentiment=sentiment,
                comment_date=event_comment.comment_date
            )
            db.session.add(sentiment_result)
            logger.debug(f"Generated comment: {comment} | Sentiment: {sentiment} | Event ID: {event_comment.id}")

    db.session.commit()
    # 统计情绪分布
    negative_count = SentimentResult.query.filter_by(sentiment=0).count()
    positive_count = SentimentResult.query.filter_by(sentiment=1).count()
    logger.info(f"Fake data generation completed. Events Comments: {EventComment.query.count()}, Sentiment Results: {SentimentResult.query.count()}, Negative: {negative_count}, Positive: {positive_count}")

@fake_bp.route('/api/generate_fake_data', methods=['POST'])
def generate_fake_data():
    try:
        # 清空现有数据
        # SentimentResult.query.delete()
        # EventComment.query.delete()
        # db.session.commit()
        generate_fake_data_logic()
        return jsonify({"message": "Fake data generated successfully"}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error generating fake data: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        generate_fake_data_logic()