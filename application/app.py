from flask import Flask

from .extentions import db


def create_app(config_filename):
    """
    A Flask application factory
    """
    app = Flask(__name__)
    app.config.from_object(config_filename)
    db.init_app(app)

    with app.app_context():
        db.init_app(app)

    app.app_context().push()
    return app

