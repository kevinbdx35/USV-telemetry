import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    CAMERA_INDEX = int(os.environ.get('CAMERA_INDEX', 0))
    TELEMETRY_UPDATE_INTERVAL = float(os.environ.get('TELEMETRY_UPDATE_INTERVAL', 1.0))
    MAX_HISTORY_SIZE = int(os.environ.get('MAX_HISTORY_SIZE', 1000))
    CAMERA_FPS = int(os.environ.get('CAMERA_FPS', 15))
    CAMERA_WIDTH = int(os.environ.get('CAMERA_WIDTH', 640))
    CAMERA_HEIGHT = int(os.environ.get('CAMERA_HEIGHT', 480))

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-must-be-set'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}