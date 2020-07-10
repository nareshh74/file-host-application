from flask import Blueprint, make_response, request, abort
from flask_restplus import Api, Resource
from flask_jwt_extended import create_access_token

from file_host_application.lib import db


auth_blueprint = Blueprint('auth', __name__)
auth_api = Api(auth_blueprint)
auth_namespace = auth_api.namespace('auth')


@auth_namespace.route('/tokens')
class Token(Resource):
    @auth_namespace.doc('Generate token')
    def get(self):
        if not request.authorization:
            return make_response('couldnt authenticate', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
        conn = db.engine.connect()
        row = conn.execute("EXECUTE VerifyAppUser '{m}', '{p}'".format(m = request.authorization.username, p = request.authorization.password)).fetchone()
        if row['Column'] == 0:
            abort(401)
        if row['Column'] == 1:
            abort(401)
        token = create_access_token(identity = row['Column'], expires_delta = False)
        return {'token' : token}, 200

@auth_blueprint.route('/test', methods=['GET'])
def test():
    return {"message":"API is UP!!"}, 200