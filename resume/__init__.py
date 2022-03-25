import os

from flask import Flask

from . import repo
from .encoding import json
from .views.resume import bp as resumebp
from .views.admin import bp as adminbp
from .views.data import bp as databp
from .views.auth import bp as authbp

def create_app():
  app = Flask(__name__, instance_relative_config=True)
  app.json_encoder = json.ResumeEncoder
  app.config.from_object("resume.config.default")
  app.register_blueprint(resumebp, url_prefix="/resume")
  app.register_blueprint(adminbp, url_prefix="/list")
  app.register_blueprint(databp, url_prefix="/data")
  app.register_blueprint(authbp)

  repo.create_session(app.config["SQLALCHEMY_DATABASE_URI"])

  @app.teardown_appcontext
  def teardown(exception=None):
      repo.session.remove()

  return app
