from os import environ
from datetime import date

class Config(object):
    SECRET_KEY = environ['APPLICATION_SECRET_KEY']
    DOWNLOAD_FOLDER = '/application/host_files/01/'
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
        }},
        'handlers': {'default': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'C:\\Users\\nareshv\\Downloads\\Naresh\\01 - Programming\\projects\\file_host_application\\logs\\' + 'application - ' + str(date.today()) + '.log',
            'maxBytes': 10000,
            'backupCount': 10
        }},
        'root': {
            'level': 'DEBUG',
            'handlers': ['default']
        }
    }

class Production(Config):
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://application1:application1@PRINHYLTPDL1561/HumanResource?driver=SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://application1:application1@PRINHYLTPDL1561/HumanResource?driver=SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False