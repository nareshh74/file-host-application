from flask import Flask, current_app, jsonify, json
from flask_restplus import Api
from .routes import auth, files
from .lib import extensions
from .config import Development, Config
import logging.config
from werkzeug.exceptions import HTTPException

api = Api(doc='/docs', version='1.0', title='File Host API Docs')

def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    current_app.logger(e.description)
    return response, e.code

def create_app():
    app = Flask(__name__)
    app.config.from_object(Development)
    logging.config.dictConfig(Config.LOGGING_CONFIG)

    api.init_app(app)
    extensions.db.init_app(app)
    extensions.jwt.init_app(app)

    app.register_error_handler(HTTPException, handle_exception)
    app.register_blueprint(auth.auth_blueprint)
    app.register_blueprint(files.files_blueprint)

    api.add_namespace(auth.auth_namespace)
    api.add_namespace(files.files_namespace)

    return app