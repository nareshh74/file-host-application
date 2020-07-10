from flask import Blueprint, send_from_directory, current_app as app, abort, request, make_response
from flask_restplus import Api, Resource, fields
import os

from file_host_application.lib import authenticate_token, handle_exception


files_blueprint = Blueprint('files', __name__)
files_api = Api(files_blueprint)
files_namespace = files_api.namespace(name='files', description='API to handle file requests')
file_version = files_namespace.model('File version', {'version':fields.Raw(required=True, description='File version of the requesting device', example='v1.0.0')})


@files_namespace.route('/')
class Files(Resource):
    @files_namespace.header('Api-Key', description='Authentication token')
    @files_namespace.header('Content-Type', description='serialization type - expected value = application/json')
    @files_namespace.expect(file_version)
    @files_namespace.response(200, '{"message":"up to date"}')
    @files_namespace.produces('application/json')
    @authenticate_token
    @handle_exception
    def get(self):
        latest_file_name = None
        print(app.root_path + '\\' + app.config['FILES_FOLDER'])
        for root, dirs, files in os.walk(app.root_path + '\\' + app.config['FILES_FOLDER']):
            for file in files:
                if file.endswith(".onnx"):
                    latest_file_name = file
                    break
        
        if(request.json['version'] == os.path.splitext(latest_file_name)[0]):
            return {'message':'up to date'}, 200

        response = send_from_directory(app.root_path + app.config['FILES_FOLDER'], latest_file_name, as_attachment=True, conditional=True)
        return response


@files_blueprint.route('/test', methods=['GET'])
def test():
    return {"message":"API is UP!!"}, 200
