from flask import Blueprint, send_from_directory, current_app as app, abort, request, make_response, redirect, url_for, g
from flask_restplus import Api, Resource
import os

from file_host_application.lib import handle_exception, authenticate_token, authorizations


files_blueprint = Blueprint('files', __name__)
files_api = Api(files_blueprint)
files_namespace = files_api.namespace(name='files', description='API to handle file requests', validate=False, decorators=[authenticate_token, handle_exception], authorizations=authorizations)


@files_namespace.route('/<string:file_version>', endpoint='version_check')
class FileVersion(Resource):
    @files_namespace.doc(security='apiKey')
    @files_namespace.doc(params={'file_version':{'description':'Version of the file in the requesting device','in':'path'}})
    @files_namespace.doc(responses={'200':'{"message":"Success message description"}'})
    @files_namespace.doc(responses={'500':'{"message":"Internal server Error message description"}'})
    @files_namespace.doc(responses={'400':'{"message":"Bad Request Error message description"}'})
    @files_namespace.doc(responses={'403':'{"message":"Not Authorized Error message description"}'})
    @files_namespace.response(303, 'Redirect to route files/ to download the latest file', headers={'Content-Disposition':'attachment', 'Content-Type':'application/octet-stream'}, schema={'type':'file'})
    @files_namespace.produces(['application/octet-stream'])
    def get(self, file_version):
        latest_file_name = None
        print(app.root_path + '\\' + app.config['FILES_FOLDER'])
        for root, dirs, files in os.walk(app.root_path + '\\' + app.config['FILES_FOLDER']):
            for file in files:
                if file.endswith(".onnx"):
                    latest_file_name = file
                    break
        print(latest_file_name)
        if(file_version == os.path.splitext(latest_file_name)[0]):
            return {'message':'up to date'}, 200
        
        if getattr(g, 'latest_file_name', None) is None:
            g.latest_file_name = latest_file_name
        redirect_url = url_for('files.file_download')
        response = make_response(redirect(redirect_url), 303, {'Content-Type':'application/octet-stream'})
        return response

@files_namespace.route('/', endpoint='file_download')
class FileName(Resource):
    @files_namespace.produces(['application/octet-stream'])
    def get(self):
        response = send_from_directory(app.root_path + '\\' + app.config['FILES_FOLDER'], g.get('latest_file_name'), as_attachment=True, conditional=True)
        print(response.headers)
        return response

@files_namespace.route('/test', methods=['GET'])
@files_namespace.hide
class Test(Resource):
    def get(self):
        return {"message":"API is UP!!"}, 200
