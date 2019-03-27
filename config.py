from os import getenv, environ

class Config(object):
  """App base congiguration"""
  FLASK_ENV = getenv('FLASK_ENV', 'production')
  DEBUG = False
  TESTING = False

class ProductionConfig(Config):
  """App production configuration."""

  pass

class DevelopmentConfig(Config):
  """App development configuration"""

  DEBUG = True
  
class TestingConfig(Config):
  """App testing configuration"""

  TESTING = True
  
config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig
}
