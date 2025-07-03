import os

from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

load_dotenv()

mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)

    from app.routes import root

    app.register_blueprint(root, url_prefix="/")

    return app
