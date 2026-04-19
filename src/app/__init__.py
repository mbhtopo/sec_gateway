"""
Contains Flask factory

To enable generating easy Flask Apps for
test cases or scaling
"""
from flask import Flask
from flasgger import Swagger

#Flask application factory, outsourced to init.py
def create_app():
    """
        Creates Flask app
        :return: app: Flask app by factory
    """
    # Instance
    app = Flask(__name__)
    # Initialize Swagger documentation
    Swagger(app)

    # Import routes after app creation
    from src.app.gateway import register_routes
    # Circle back to gateway to process function calls
    register_routes(app)
    # give back Flask App
    return app
