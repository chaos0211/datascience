from datetime import datetime, timedelta
import random
import logging
from flask import Blueprint, jsonify
from app.models import db
from app.models.sentiment import EventComment, SentimentResult
from app.services.sentiment_service import analyze_sentiment

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake_bp = Blueprint('fake_data', __name__)


def generate_fake_data_logic():
    events = [
        {"name": "TechPhone Launch", "date": "2025-04-14"},
        {"name": "Movie Premiere", "date": "2025-04-15"}
    ]
    comment_templates = {
        1: [  # 正面
            "Love the {feature} of {event}, {adjective}!",
            "{event} is {adjective}, highly recommend!"
        ],
        0: [  # 负面
            "{issue} with {event}, so {adjective}!",
            "{event}’s {feature} is {adjective}, very disappointed."
        ],
        None: [  # 中性（由模型决定）
            "What’s the {feature} like on {event}?",
            "Just got {event}, testing the {feature} now."
        ]
    }
    features = ["camera", "battery", "design", "screen", "performance"]
    positive_adjectives = ["awesome", "fantastic", "great", "amazing"]
    negative_adjectives = ["disappointing", "terrible", "frustrating", "bad"]
    issues = ["Battery drains fast", "Too expensive", "Shipping delayed", "Screen flickers"]

    logger.info("Starting fake data generation")
    for day in range(7):
        date = (datetime(2025, 4, 14) + timedelta(days=day)).strftime("%Y-%m-%d")
        sentiment_weights = [0.50, 0.20, 0.30] if day == 2 else [0.30, 0.30, 0.40]  # [负, 正, 中]

        for _ in range(50):  # 每天50条
            event = random.choice(events)
            sentiment = random.choices([0, 1, None], weights=sentiment_weights, k=1)[0]
            template = random.choice(comment_templates[sentiment])
            comment = template.format(
                event=event["name"],
                feature=random.choice(features),
                adjective=random.choice(positive_adjectives if sentiment == 1 else negative_adjectives),
                issue=random.choice(issues) if sentiment == 0 else ""
            )

            event_comment = EventComment(
                event_name=event["name"],
                event_date=datetime.strptime(event["date"], "%Y-%m-%d").date(),
                comment=comment,
                comment_date=datetime.strptime(
                    f"{date} {random.randint(0, 23):02d}:{random.randint(0, 59):02d}:00",
                    "%Y-%m-%d %H:%M:%S"
                )
            )
            db.session.add(event_comment)
            db.session.flush()

            sentiment_result = analyze_sentiment(comment)
            sentiment = 0 if sentiment_result == "negative" else 1
            sentiment_result = SentimentResult(
                event_id=event_comment.id,
                sentiment=sentiment,
                comment_date=event_comment.comment_date
            )
            db.session.add(sentiment_result)

    db.session.commit()
    logger.info("Fake data generation completed")


@fake_bp.route('/api/generate_fake_data', methods=['POST'])
def generate_fake_data():
    try:
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