import  api as server_api

from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail


def create_app(debug: bool) -> Flask:
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
    api = Api(app)

    if debug:
        app.config['DEBUG'] = True
    
    api.route(server_api.Index, 'index', '/')
    api.route(server_api.ClientPassword, "client_detail", "/client_detail/<int:id>")
    configure_extensions(app)
    
    return app

def configure_extensions(app: Flask):
    """
    It initializes a Flask app with its extensions.

    Args:
        app: a Flask application
    """
    pass
