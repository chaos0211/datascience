from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  # ← 这里改为绝对路径导入即可解决问题
from app.routes.analysis import analysis_bp
from app.routes.monitor import monitor_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)


    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(monitor_bp, url_prefix='/api/monitor')

    @app.route('/')
    def index():
        return 'Hello, Flask is running!'

    return app