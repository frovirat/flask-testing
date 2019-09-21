"""
Flask server run
"""
from app import create_app

def run(debug: bool = False):
    """
    Serves a flask application using waitress.

        Args:
            debug: enables debug mode or not. Default is False so it is disabled.
    """
    app = create_app(debug)
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    run(True)
