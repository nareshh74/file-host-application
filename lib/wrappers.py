from flask import abort, request, current_app as app
from functools import wraps

def authenticate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        token = request.headers.get('Api-Key')
        if token is None:
            abort(400, 'missing token')
        if(token != app.config['SECRET_KEY']):
            abort(403, 'invalid token')
        return func(*args, **kwargs)
    return wrapper