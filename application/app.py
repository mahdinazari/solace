import importlib

from flask import Flask, jsonify

from application.config import Config
from .extensions import db, migrate, ma
from .exceptions import ApplicationException


application_views = Config.APPLICATION_VIEWS


def create_app(config_filename):
    """
    A Flask application factory
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    for installed_app in application_views:
        view = importlib.import_module(
            'views.{}'.format(installed_app)
        )
        app.register_blueprint(view.blueprint)

    with app.app_context():
        db.init_app(app)

    # Register the error handler
    @app.errorhandler(ApplicationException)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app.app_context().push()
    return app

