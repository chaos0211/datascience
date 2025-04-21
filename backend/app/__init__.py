from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config  # ← 这里改为绝对路径导入即可解决问题
from app.routes.analysis import analysis_bp
from app.routes.monitor import monitor_bp
import os

db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # 注册路由蓝图
    from app.routes.analysis import analysis_bp
    from app.routes.monitor import monitor_bp
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(monitor_bp, url_prefix='/api/monitor')

    # ✅ 添加前端首页页面支持
    @app.route('/')
    def index():
        return send_from_directory(os.path.join(app.root_path, '..', 'frontend'), 'index.html')

    # ✅ 添加静态资源访问（JS/CSS）
    @app.route('/<path:filename>')
    def static_files(filename):
        return send_from_directory(os.path.join(app.root_path, '..', 'frontend'), filename)

    return app