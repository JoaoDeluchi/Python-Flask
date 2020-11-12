from flask import Flask
from app.domain.tasks.views import app_tasks
from database import db, migrate
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///simple_api.db"
    db.init_app(app)
    migrate.init_app(app)
    db.create_all(app=app)
    _register_blueprint(app)
    return app

def _register_blueprint(app):
    app.register_blueprint(app_tasks)
