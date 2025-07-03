import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

load_dotenv()

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    origins_allowed = []
    if os.getenv("DEBUG"):
        origins_allowed.extend(["null", "http://localhost:3000"])
    else:
        origins_allowed.extend([os.getenv("FRONTEND_URL")])

    CORS(
        app,
        resources={
            r"/api/actions": {
                "origins": origins_allowed,
                "methods": ["GET", "OPTIONS"],
            }
        },
    )

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)

    from app.routes import root

    app.register_blueprint(root, url_prefix="/")

    return app
