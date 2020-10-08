from flask import Flask



def create_app():
    app = Flask(__name__)
    migrate.init_app(app, db)
    _register_blueprint(app)
    return app

def _register_blueprint(app)
    