from cryptography.fernet import Fernet

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@mysql/db'
    SECRET_KEY = Fernet.generate_key()

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True

class PreviewDeploymentConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class DeploymentConfig(PreviewDeploymentConfig):
    # None, to be configured in config.cfg in instance directory
    SQLALCHEMY_DATABASE_URI = None
    SECRET_KEY = None

