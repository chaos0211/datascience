from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # 蓝图导入必须在 init_app 之后进行，避免循环引用
    from app.routes.analysis import analysis_bp
    from app.routes.monitor import monitor_bp
    from app.routes.generate_fake_data import fake_bp

    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(monitor_bp, url_prefix='/api/monitor')
    app.register_blueprint(fake_bp, url_prefix='/api/fake')

    with app.app_context():
        from app.models import sentiment
        db.create_all()

    @app.route('/')
    def index():
        frontend_path = os.path.abspath(os.path.join(app.root_path, '..', '..', 'frontend'))
        return send_from_directory(frontend_path, 'index.html')

    @app.route('/<path:filename>')
    def static_files(filename):
        frontend_path = os.path.abspath(os.path.join(app.root_path, '..', '..', 'frontend'))
        return send_from_directory(frontend_path, filename)
    @app.route('/cart')
    def cart():
        frontend_path = os.path.abspath(os.path.join(app.root_path, '..', '..', 'frontend'))
        return send_from_directory(frontend_path, 'cart.html')


    return app