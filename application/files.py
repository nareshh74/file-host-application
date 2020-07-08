from flask import Blueprint, send_from_directory, current_app as app, abort, jsonify, request, make_response
from flask_restplus import Api, Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
import os
import logging

files_blueprint = Blueprint('files', __name__)
files_api = Api(files_blueprint)
files_namespace = files_api.namespace('files')
files_logger = logging.getLogger()

@files_blueprint.errorhandler
def handle(err):
    files_logger.error(err.message)
    return jsonify({'message':str(err)}), err.code

@files_namespace.route('/')
@files_namespace.param('version', 'version of the ML model in device')
class Files(Resource):
    @jwt_required
    def get(self):
        
        current_user = get_jwt_identity
        if not current_user:
            abort(401, 'invalid token')
        
        latest_file = None
        for root, dirs, files in os.walk(app.root_path + app.config['DOWNLOAD_FOLDER']):
            for file in files:
                if file.endswith(".onnx"):
                    latest_file = file
                    break
        print(os.path.splitext(file.name)[0])
        
        version = request.get_json(force=True)['version']
        if(version == None):
            abort(400, 'version parameter expected')

        if(version == os.path.splitext(file.name)[0]):
            return {'message':'up to date'}, 200
        
        response = send_from_directory(app.root_path, latest_file.name, as_attachment=True, conditional=True)
        response.status = 200
        return response

@files_blueprint.route('/test', methods=['GET'])
def test():
    return {"message":"API is UP!!"}, 200

@files_blueprint.route('/<path:wrong_path>', methods=['GET', 'POST'])
def throw(wrong_path):
    abort(404, request.method + ' to the route ' + str(wrong_path) + ' is not valid')