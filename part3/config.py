import os

class Config:
    """
    Base configuration class.
    Contains default settings that apply to all environments.
    """
    # The SECRET_KEY is used for security (sessions, tokens, etc.)
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # DEBUG is False by default for safety
    DEBUG = False

class DevelopmentConfig(Config):
    """
    Development configuration.
    Enables debug mode for easier development and troubleshooting.
    """
    DEBUG = True

class TestingConfig(Config):
    """
    Testing configuration.
    Used when running automated tests.
    """
    TESTING = True
    DEBUG = True

# Dictionary to easily switch between environments if needed
config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': Config
}
