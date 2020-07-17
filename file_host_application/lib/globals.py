# module for global variables and functions

# python package imports
import logging

# internal imports
from flask import make_response, current_app as app

authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Api-Key'
    }
}

def close_logfilehandlers():
    for handler in reversed(logging.getLogger().handlers):
        handler.close()

def handle_exception(e):
    app.logger.error(e.description)
    return make_response({'message':e.description}, e.code)