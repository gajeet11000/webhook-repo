from flask import Blueprint
from .actions import router as actions_router

root = Blueprint("root", __name__)

root.register_blueprint(actions_router, url_prefix="/api")
