# module for reusable decorators
from flask import abort, request, current_app as app
from functools import wraps

def authenticate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        token = request.headers.get('Api-Key')
        if token is None:
            abort(400, 'expecting ' + ' Api-Key header')
        if(token != app.config['SECRET_KEY']):
            abort(403, 'invalid token')
        return func(*args, **kwargs)
    return wrapper

def validate_requestjson(request_parameters):
    def wrapper1(func):
        @wraps(func)
        def wrapper2(*args, **kwargs):
            requestjson = request.get_json()
            for request_parameter in request_parameters:
                if request_parameter not in requestjson:
                    abort(400, 'expecting ' + request_parameter + ' in request JSON')
            return func(*args, **kwargs)
        return wrapper2
    return wrapper1

def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message = getattr(e, 'message', repr(e))
            code = getattr(e, 'code', 500)
            abort(code, message)
    return wrapper