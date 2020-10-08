from flask import Flask
from app.domain.tasks.views import app_tasks



def create_app():
    app = Flask(__name__)
    _register_blueprint(app)
    return app

def _register_blueprint(app):
    app.register_blueprint(app_tasks)