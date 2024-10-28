import firebase_admin
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1212arwsda'

    from .recommendationAPI import recommendationAPI
    app.register_blueprint(recommendationAPI, url_prefix='/recommend')
    
    return app