"""environment configuration"""

import os

class Config(object):
    """Parent Configuration class"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

class DevelopentConfig(Config):
    """Development configuration class"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration class"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
    DEBUG = True

class StagingConfig(Config):
    """Configuration for Staging"""
    pass

class ProductionConfig(Config):
    """Configuration for production"""
    pass

app_config = {
    'development': DevelopentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}