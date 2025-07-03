from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from app import mongo
from app.schemas.actions import ActionSchema, ActionQuerySchema
from app.utils import GithubWebhookExtractor
from marshmallow import ValidationError

router = Blueprint("actions", __name__)


@router.route("/actions", methods=["GET"])
def get_actions():
    try:
        query_args = ActionQuerySchema().load(request.args)

        query = {}
        if query_args.get("recent", False):
            time_threshold = datetime.now(timezone.utc) - timedelta(
                seconds=query_args["interval"]
            )
            query = {"timestamp": {"$gte": time_threshold}}

        actions = list(mongo.db.actions.find(query).sort("timestamp", -1))
        actions = ActionSchema(many=True).dump(actions)
        return jsonify(actions), 200

    except ValidationError as err:
        return jsonify(
            {"error": "Invalid query parameters", "details": err.messages}
        ), 400


@router.route("/github-webhook", methods=["POST"])
def handle_webhook_data():
    payload = request.get_json()
    event = request.headers.get("X-GitHub-Event")
    data = GithubWebhookExtractor.get_PR_data(event, payload)

    if data.get("action") == "closed" and not data.get("is_merged", False):
        return jsonify({"message": "PR closed but not merged"})

    data.update({"event": event})

    if event == "push":
        data.update(
            {
                "action": "push",
            }
        )

    result = mongo.db.actions.insert_one(data)
    new_event = mongo.db.actions.find_one({"_id": result.inserted_id})

    return jsonify({"message": "Data saved", "data": ActionSchema().dump(new_event)})
