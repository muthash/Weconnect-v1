"""The Config class contains the general settings that we want all
    environments to have by default.Other environment classes
    inherit from it and can be used to set settings that are only unique to
    them. Additionally, the dictionary app_config is used to export the 4
    environments we've specified.
"""
import os


class Config(object):
    """Parent configuration class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    JWT_BLACKLIST_ENABLED = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL')


class DevelopmentConfig(Config):
    """Configurations for Development"""
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configuraions for Staging"""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for production"""
    DEBUG = False
    Testing = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
