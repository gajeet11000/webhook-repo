from datetime import datetime

from marshmallow import Schema, fields, post_dump, validate

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
