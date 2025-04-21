from flask_sqlalchemy import SQLAlchemy

from app import db
class EventComment(db.Model):
    __tablename__ = "events_comments"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(255), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, nullable=False)
    sentiment_results = db.relationship("SentimentResult", backref="event_comment", lazy=True)

class SentimentResult(db.Model):
    __tablename__ = "sentiment_results"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events_comments.id"), nullable=False)
    sentiment = db.Column(db.Integer, nullable=False)  # 0: negative, 1: positive
    comment_date = db.Column(db.DateTime, nullable=False)