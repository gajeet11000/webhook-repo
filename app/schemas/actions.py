import hmac
import os
from datetime import datetime
from http import HTTPStatus

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    post_dump,
    validate,
    validates_schema,
)

from app.utils import DateTimeUtils


class ActionSchema(Schema):
    @post_dump(pass_original=True)
    def convert_datetime(self, data, original, **kwargs):
        id = original.get("_id")
        if id:
            original["_id"] = str(id)
        timestamp = original.get("timestamp")
        if timestamp and isinstance(timestamp, datetime):
            original["timestamp"] = DateTimeUtils.format_utc_timestamp(timestamp)
        return original


class ActionQuerySchema(Schema):
    recent = fields.Boolean(required=False, truthy={"true", "1"}, falsy={"false", "0"})
    interval = fields.Integer(
        required=False,
        strict=False,
        validate=validate.Range(min=1, error="Interval must be a positive integer"),
        load_default=15,
    )


class GitHubWebhookHeadersSchema(Schema):
    """Validate GitHub webhook headers and signature"""

    def __init__(self, *args, **kwargs):
        self.raw_body = kwargs.pop("raw_body", None)
        super().__init__(*args, **kwargs)

    x_hub_signature_256 = fields.Str(required=True, data_key="X-Hub-Signature-256")
    x_github_event = fields.Str(required=True, data_key="X-GitHub-Event")
    x_github_delivery = fields.Str(required=True, data_key="X-GitHub-Delivery")

    @validates_schema
    def verify_signature(self, data, **kwargs):
        secret = os.getenv("GITHUB_WEBHOOK_SECRET").encode()
        if not secret:
            raise ValidationError(
                "Webhook secret not configured",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        request_signature = data.get("x_hub_signature_256", "")
        if not request_signature:
            raise ValidationError(
                "Missing signature header", status_code=HTTPStatus.FORBIDDEN
            )

        raw_body = self.raw_body
        if not raw_body:
            raise ValidationError(
                "Missing request body for verification",
                status_code=HTTPStatus.BAD_REQUEST,
            )

        expected_signature = (
            "sha256=" + hmac.new(secret, raw_body, "sha256").hexdigest()
        )
        if not hmac.compare_digest(expected_signature, request_signature):
            raise ValidationError("Invalid signature", status_code=HTTPStatus.FORBIDDEN)
