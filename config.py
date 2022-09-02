import os, datetime
from os import environ
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG=False
    TESTING=False
    CSRF_ENABLED=False
    WTF_CSRF_ENABLED = False
    SECRET_KEY='secret-key'
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SESSION_PERMANENT = True
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=3)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG=False

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URL')
    TESTING = True