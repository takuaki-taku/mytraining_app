from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

from app import models
from app.auth import bp as auth_bp
from app.main import bp as main_bp


def create_app(config_class=Config):
    """Flaskアプリケーションを作成する。"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")

    app.register_blueprint(main_bp)

    @app.errorhandler(404)
    def not_found_error(error):
        """404エラーハンドラー。"""
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        """500エラーハンドラー。"""
        return render_template("500.html"), 500

    return app
