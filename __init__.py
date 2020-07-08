from flask import Flask, current_app, jsonify
from flask_restplus import Api
from .application import auth, files, extensions
from .application.config import Development, Config
import logging.config

api = Api(doc='/docs', version='1.0', title='File Host API Docs')

def handle(err):
    current_app.logger.error(err)
    return jsonify({'message': err.description}), err.code

def create_app():
    app = Flask(__name__)
    app.config.from_object(Development)
    logging.config.dictConfig(Config.LOGGING_CONFIG)

    api.init_app(app)
    extensions.db.init_app(app)
    extensions.jwt.init_app(app)

    app.register_error_handler(404, handle)
    app.register_blueprint(auth.auth_blueprint)
    app.register_blueprint(files.files_blueprint)

    api.add_namespace(auth.auth_namespace)
    api.add_namespace(files.files_namespace)

    return app