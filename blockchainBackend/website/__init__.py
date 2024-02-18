from flask import Flask
from flask_cors import CORS, cross_origin

def create_app():

    app = Flask(__name__, static_url_path='/static')

    from .blockchain import blockchain

    app.register_blueprint(blockchain, url_prefix='/')


    CORS(app)
    return app

