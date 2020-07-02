from flask import Blueprint, send_from_directory, current_app as app
from flask_restplus import Api, Resource
from flask_jwt_extended import (jwt_required, get_jwt_identity)
import os
from . import jwt

download_blueprint = Blueprint('files', __name__)
download_api = Api(download_blueprint)
download_namespace = download_api.namespace('files')

@download_namespace.route('/<string:file_name>')
@download_namespace.param('file_name', 'Name of the file to be downloaded')
class Files(Resource):
    @jwt_required
    def get(self, file_name):
        
        current_user = get_jwt_identity
        if not current_user:
            return 'authentiation failed'
        
        file_name = 'application/host_files/01/' + file_name
        print(file_name)
        print("root path")
        print(app.root_path)
        print(os.path.join(app.root_path, file_name))
        if not os.path.isfile(os.path.join(app.root_path, file_name)):
            return "invalid file/path"
            
        return send_from_directory(app.root_path, file_name, as_attachment = True)

@download_namespace.route('/test')
class Test(Resource):
    def get(self):
        return {"Test":"Test"}, 200