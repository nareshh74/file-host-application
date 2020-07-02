from os import environ

class Config:
    SECRET_KEY = environ['APPLICATION_SECRET_KEY']

class Production_Config(Config):
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://application1:application1@PRINHYLTPDL1561/HumanResource?driver=SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development_Config(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://application1:application1@PRINHYLTPDL1561/HumanResource?driver=SQL+Server"
    SQLALCHEMY_TRACK_MODIFICATIONS = False