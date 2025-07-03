import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo

load_dotenv()

mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    if os.getenv("DEBUG", "").lower() in ("true", "1", "t"):
        origins_allowed = [
            # "*",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    else:
        frontend_url = os.getenv("FRONTEND_URL")
        if not frontend_url:
            raise ValueError(
                "FRONTEND_URL environment variable must be set in production"
            )
        origins_allowed = [frontend_url]

    CORS(
        app,
        resources={
            r"/api/actions": {
                "origins": origins_allowed,
                "methods": ["GET", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "max_age": 86400,
            }
        },
        origins=origins_allowed,
        supports_credentials=True,
        send_wildcard=False,
    )

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)

    from app.routes import root

    app.register_blueprint(root, url_prefix="/")

    return app
