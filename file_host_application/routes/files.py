from flask import Blueprint, send_from_directory, current_app as app, abort, request, make_response, redirect, url_for
from flask_restplus import Api, Resource
import os

from file_host_application.lib import handle_exception, authenticate_token, authorizations


files_blueprint = Blueprint('files', __name__)
files_api = Api(files_blueprint)
files_namespace = files_api.namespace(name='files', description='API to handle file requests', authorizations=authorizations)


@files_namespace.route('/<string:file_version>', endpoint='version_check')
class FileVersion(Resource):
    @authenticate_token
    @files_namespace.doc(security='apiKey')
    @files_namespace.doc(params={'file_version':{'description':'Version of the file in the requesting device','in':'path'}})
    @files_namespace.doc(responses={'200':'{"message":"Success message description"}'})
    @files_namespace.doc(responses={'500':'{"message":"Internal server Error message description"}'})
    @files_namespace.doc(responses={'400':'{"message":"Bad Request Error message description"}'})
    @files_namespace.doc(responses={'403':'{"message":"Not Authorized Error message description"}'})
    @files_namespace.doc(responses={'303':'Redirect to the route /files. Please refer /files route response documentation'})
    @handle_exception
    def get(self, file_version):
        latest_file_name = None
        for root, dirs, files in os.walk(app.root_path + '\\' + app.config['FILES_FOLDER']):
            for file in files:
                if file.endswith(".onnx"):
                    latest_file_name = file
                    break
        if(file_version == os.path.splitext(latest_file_name)[0]):
            return {'message':'up to date'}, 200
        
        redirect_url = url_for('files.file_download', latest_file_name=latest_file_name)
        response = make_response(redirect(redirect_url), 303)
        return response

@files_namespace.route('/', endpoint='file_download')
class FileName(Resource):
    @authenticate_token
    @files_namespace.doc(security='apiKey')
    @files_namespace.doc(params={'latest_file_name':{'description':'Latest file in the server','in':'query'}})
    @files_namespace.response(200, 'latest file as attachment', headers={'Content_disposition':'attachment', 'Content-Type':'application/octet-stream'})
    @files_namespace.doc(responses={'500':'{"message":"Internal server Error message description"}'})
    @files_namespace.doc(responses={'400':'{"message":"Bad Request Error message description"}'})
    @files_namespace.doc(responses={'403':'{"message":"Not Authorized Error message description"}'})
    @handle_exception
    def get(self):
        latest_file_name = request.args.get('latest_file_name', None)
        if latest_file_name is None:
            for root, dirs, files in os.walk(app.root_path + '/' + app.config['FILES_FOLDER']):
                for file in files:
                    if file.endswith(".onnx"):
                        latest_file_name = file
                        break
        response = send_from_directory(app.config['FILES_FOLDER'], latest_file_name, as_attachment=True, conditional=True)
        return response

@files_namespace.route('/test', methods=['GET'])
@files_namespace.hide
class Test(Resource):
    def get(self):
        return {"message":"API is UP!!"}, 200
