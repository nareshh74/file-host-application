from os import environ
from datetime import date

class Config(object):
    SECRET_KEY = environ['APPLICATION_SECRET_KEY']
    FILES_FOLDER = environ['APPLICATION_FILES_FOLDER']
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] {%(pathname)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
        }},
        'handlers': {'default': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': environ['APPLICATION_LOG_FOLDER'] + '\\application - ' + str(date.today()) + '.log',
            'maxBytes': 10000,
            'backupCount': 10
        }},
        'root': {
            'level': environ['APPLICATION_DEBUG_LEVEL'],
            'handlers': ['default']
        }
    }

class Production(Config):
    pass

class Development(Config):
    pass