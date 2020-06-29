from flask import Flask, send_from_directory, request, redirect, make_response
from flask_restplus import Api, Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity, create_access_token, JWTManager)
from flask_sqlalchemy import SQLAlchemy
import os

# create flask app
app = Flask(__name__)

# configure flask app
app.config.from_pyfile('config - dev.py', silent=True)

# create extension instances
api = Api(app, doc = '/docs')
db = SQLAlchemy(app)
jwt = JWTManager(app)

# protected download API
@api.route('/app/v1/resources/<path:path>')
class File(Resource):
    @jwt_required
    def get(self, path):
        current_user = get_jwt_identity
        if not current_user:
            return 'authentiation failed'
        if not os.path.isfile(path):
            return "invalid file/path"
        return send_from_directory(app.root_path, path, as_attachment = True)

# generate token
@api.route('/app/v1/resources/tokens')
class Token(Resource):
    def get(self):
        if not request.authorization:
            return make_response('couldnt authenticate', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
        if not request.authorization.username:
            return 'provide username'
        conn = db.engine.connect()
        row = conn.execute("SELECT Name, Password FROM AppUser WHERE Name = '{u}'".format(u = "user1")).fetchone()
        if not row:
            return "invalid user"
        if row[1] != request.authorization.password:
            return "wrong password"
        token = create_access_token(identity = request.authorization.username, expires_delta = False)
        return token

app.run()