from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from backend.config import Config  # ← 这里改为绝对路径导入即可解决问题
from app.routes.analysis import analysis_bp
from app.routes.monitor import monitor_bp
from app.routes.generate_fake_data import fake_bp
import os
from config import Config
from app import models
from flask_migrate import Migrate
from app.models import db

migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    # models.db.init_app(app)
    # with app.app_context():
    #     models.db.create_all()
    # 注册路由蓝图
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(monitor_bp, url_prefix='/api/monitor')

    with app.app_context():
        from app.models import sentiment
        db.create_all()

    # ✅ 添加前端首页页面支持
    @app.route('/')
    def index():

        frontend_path = os.path.abspath(os.path.join(app.root_path, '..', '..', 'frontend'))
        return send_from_directory(frontend_path, 'index.html')

    # 提供静态资源访问（如 JS/CSS）
    @app.route('/<path:filename>')
    def static_files(filename):
        frontend_path = os.path.abspath(os.path.join(app.root_path, '..', '..', 'frontend'))
        return send_from_directory(frontend_path, filename)

    return app