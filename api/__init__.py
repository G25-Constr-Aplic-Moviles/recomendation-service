import firebase_admin
from flask import Flask
from firebase_admin import credentials,initialize_app

cred = credentials.Certificate("api/key.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1212arwsda'

    from .recommendationAPI import recommendationAPI
    app.register_blueprint(recommendationAPI, url_prefix='/recommend')
    
    return app