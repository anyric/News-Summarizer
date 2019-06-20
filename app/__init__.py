import os
from flask import Flask
from flask_cors import CORS
from flask_bootstrap import Bootstrap

def create_app(config):
  """ create and configure the app instance"""

  app = Flask(__name__)
  app.config.from_object(config)
  CORS(app)
  Bootstrap(app)

  return app
