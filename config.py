import os
from os import environ
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG=False
    TESTING=False
    CSRF_ENABLED=False
    WTF_CSRF_ENABLED = False
    SECRET_KEY='secret-key'
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

class ProductionConfig(Config):
    DEBUG=False

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True