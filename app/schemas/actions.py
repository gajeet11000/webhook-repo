from datetime import datetime

from marshmallow import Schema, post_dump

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
