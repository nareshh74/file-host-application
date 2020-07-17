# module for global variables and functions

# 3rd party imports
from flask import make_response
from werkzeug.exceptions import HTTPException
import logging

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

def log_exception(e):
    logging.exception(e.get('description', None))
    return make_response({'message':e.get('description', None)}, e.get('code', 500))
