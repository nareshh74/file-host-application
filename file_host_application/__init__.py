# standard imports
import logging.config
from os import environ
import atexit

# 3rd party imports
from flask import Flask, current_app, make_response, abort
from werkzeug.exceptions import HTTPException
from werkzeug.contrib.fixers import ProxyFix
from flask_cors import CORS

# application imports
from file_host_application.routes import files_blueprint, files_namespace
from file_host_application.core.config import Development, Config, Production
from file_host_application.core import api, close_logfilehandlers, log_exception


# app factory
def create_app():
    # Flask app instance
    app = Flask(__name__)
    
    # flask restplus gets OpenAPI specs from HTTP site, to serve it through HTTPS, use a proxy
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # configure flask instance from config file
    if environ['FLASK_ENV'] == 'production':
        app.config.from_object(Production)
    else:
        app.config.from_object(Development)
    logging.config.dictConfig(app.config['LOGGING_CONFIG'])

    # attach extensions and blueprints
    api.init_app(app)

    # attach blueprints
    app.register_blueprint(files_blueprint)
    
    # logging doesn't close log files after app stops
    # Closing log files using atexit
    atexit.register(close_logfilehandlers)

    # app level error handler, all caught exceptions are bubbled up and caughts by this logger
    # single logger is used, so all exceptions are logged to a single file
    app.register_error_handler(HTTPException, log_exception)
    
    # categorizing endpoints in swagger UI
    api.add_namespace(files_namespace)

    # allow cross domain requests
    # should be taken care in hosting side, if we use 3rd party services like azure.
    CORS(app)

    # factory shud always return a flask instance
    return app


app = create_app()