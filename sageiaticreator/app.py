from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

from sageiaticreator import extensions
from sageiaticreator import routes
from sageiaticreator.views import activities, generate, organisations, users


def create_app(config_object='config'):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_blueprints(app)
    register_extensions(app)
    CORS(app)
    return app


def register_blueprints(app):
    app.register_blueprint(routes.app)
    app.register_blueprint(activities.app)
    app.register_blueprint(generate.app)
    app.register_blueprint(organisations.app)
    app.register_blueprint(users.app)


def register_extensions(app):
    extensions.db.init_app(app)
    #extensions.migrate.init_app(app, extensions.db)
    extensions.login_manager.init_app(app)
