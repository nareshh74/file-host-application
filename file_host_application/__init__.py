from flask import Flask, current_app, make_response, abort
from flask_restplus import Api
import logging.config
from werkzeug.exceptions import HTTPException
from os import environ
import atexit
from werkzeug.contrib.fixers import ProxyFix

from file_host_application.routes import files_blueprint, files_namespace
from file_host_application.config import Development, Config, Production


def close_logfilehandlers():
    for handler in reversed(logging.getLogger().handlers):
        handler.close()


api = Api(doc='/docs', version='1.0', title='File Host API Docs')

def handle_exception(e):
    current_app.logger.error(e.description)
    return make_response({'message':e.description}, e.code)


def create_app():
    app = Flask(__name__)
    
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if environ['FLASK_ENV'] == 'production':
        app.config.from_object(Production)
    else:
        app.config.from_object(Development)
    
    logging.config.dictConfig(app.config['LOGGING_CONFIG'])

    api.init_app(app)
    atexit.register(close_logfilehandlers)

    app.register_error_handler(HTTPException, handle_exception)
    app.register_blueprint(files_blueprint)

    api.add_namespace(files_namespace)

    CORS(app)

    return app