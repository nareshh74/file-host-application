from flask import Blueprint, send_from_directory, current_app as app, abort, request, make_response
from flask_restplus import Api, Resource
import os

from file_host_application.lib import authenticate_token


files_blueprint = Blueprint('files', __name__)
files_api = Api(files_blueprint)
files_namespace = files_api.namespace('files')


@files_namespace.route('/')
@files_namespace.param('version', 'version of the ML model in device')
class Files(Resource):
    @authenticate_token
    def get(self):
        try:
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
        
        except Exception as e:
            message = getattr(e, 'message', repr(e))
            code = getattr(e, 'code', 500)
            abort(code, message)


@files_blueprint.route('/test', methods=['GET'])
def test():
    return {"message":"API is UP!!"}, 200
