
from flask import Flask
from flask_restplus import Api

from apis import api


def create_app() -> Flask:
    """
    Function that creates a Flask application. App configuration is set here.
    Create application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    Args:
        debug: debug mode enabled or not.

    Returns:
        app: a Flask app already configured to run.
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    api.init_app(app)

    return app
