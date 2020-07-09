from flask import Blueprint, send_from_directory, current_app as app, abort, jsonify, request, make_response, json
from flask_restplus import Api, Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
import os
import logging
from werkzeug.exceptions import HTTPException


files_blueprint = Blueprint('files', __name__)
files_api = Api(files_blueprint)
files_namespace = files_api.namespace('files')
files_logger = logging.getLogger()


@files_namespace.route('/')
@files_namespace.param('version', 'version of the ML model in device')
class Files(Resource):
    @jwt_required
    def get(self):
        try:
            current_user = get_jwt_identity
            version = request.get_json()['version']

            latest_file_name = None
            for root, dirs, files in os.walk(app.root_path + app.config['DOWNLOAD_FOLDER']):
                for file in files:
                    if file.endswith(".onnx"):
                        latest_file_name = file
                        break
            
            if(version == os.path.splitext(latest_file_name)[0]):
                return {'message':'up to date'}, 200

            response = make_response({send_from_directory(app.root_path + app.config['DOWNLOAD_FOLDER'], latest_file_name, as_attachment=True, conditional=True)}, 200)
            return response
        
        except Exception as e:
            message = getattr(e, 'message', repr(e))
            code = getattr(e, 'code', 500)
            abort(code, message)


@files_blueprint.route('/test', methods=['GET'])
def test():
    return {"message":"API is UP!!"}, 200
