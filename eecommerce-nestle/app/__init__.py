from flask import Flask, json
from werkzeug.exceptions import HTTPException, InternalServerError
from flask_cors import CORS

from app.domains.products.views import app_products
from app.domains.category.views import app_categories
from app.domains.users.views import app_users
from app.domains.product_line.views import app_product_line
from app.domains.providers.views import app_providers
from database import db, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    db.init_app(app)
    CORS(app)
    migrate.init_app(app, db)
    _register_blueprint(app)
    _register_error_handler(app)
    return app


def _register_blueprint(app):
    app.register_blueprint(app_users)
    app.register_blueprint(app_providers)
    app.register_blueprint(app_products)
    app.register_blueprint(app_categories)
    app.register_blueprint(app_product_line)


def _handle_default_exception(e):
    response = e.get_response()
    code = e.code
    description = e.description

    response.data = get_data(code, description)
    response.content_type = "application/json"
    return response, code


def get_data(code, description):
    return json.dumps({
        'code': code,
        'message': description,
    })


def _handle_internal_server_error_exception(e):
    response = e.get_response()
    code = 500
    description = 'Sorry, we cant process request. Try again.'
    response.data = get_data(code, description)
    response.content_type = "application/json"
    return response, code


def _register_error_handler(app):
    app.register_error_handler(HTTPException, _handle_default_exception)
    app.register_error_handler(InternalServerError, _handle_internal_server_error_exception)
