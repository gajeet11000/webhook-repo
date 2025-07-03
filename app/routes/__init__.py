from flask import Blueprint
from .actions import router as actions_router

root = Blueprint("root", __name__)


@root.route("/")
def index():
    return "Welcome to my Flask app!"


root.register_blueprint(actions_router, url_prefix="/api")
