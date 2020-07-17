# module to serve flask app instance to WSGI like gunicorn or werkzeug
from file_host_application import create_app


app = create_app()