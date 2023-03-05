import os
from flask import Flask
from financial.extensions import db
from financial.extensions import ma

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
  """Flask's factory application

  Returns:
      Flask: The Flask factory application instance 
  """
  app = Flask(__name__)
  app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY'),
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False)
  
  # [start] Initializing Flask extensions
  db.init_app(app)
  ma.init_app(app)
  # [end]
  
  # [start] Registering blueprints here
  from financial.routes import financial_data
  app.register_blueprint(financial_data.bp)
  
  from financial.routes import statistics
  app.register_blueprint(statistics.bp)
  # [end]
  
  return app