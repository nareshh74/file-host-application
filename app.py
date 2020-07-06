from flask import Flask
from flask_restplus import Api
from application import auth, download, extensions
import config

api = Api(doc='/docs', version='1.0', title='Flask Application API Docs')

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Development_Config')

    api.init_app(app)
    extensions.db.init_app(app)
    extensions.jwt.init_app(app)

    app.register_blueprint(auth.auth_blueprint)
    app.register_blueprint(download.download_blueprint)

    api.add_namespace(auth.auth_namespace)
    api.add_namespace(download.download_namespace)

    return app