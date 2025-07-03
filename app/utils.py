from datetime import datetime, timezone


class DateTimeUtils:
    @classmethod
    def to_datetime(cls, time_input):
        try:
            if isinstance(time_input, (int, float)):
                # Handle Unix timestamp
                return datetime.fromtimestamp(time_input, tz=timezone.utc)
            elif isinstance(time_input, str):
                # Handle ISO 8601 string
                if time_input.endswith("Z"):
                    time_input = time_input[:-1] + "+00:00"
                return datetime.fromisoformat(time_input).astimezone(timezone.utc)
            else:
                raise ValueError(
                    "Input must be Unix timestamp (number) or ISO 8601 string"
                )
        except Exception as e:
            raise ValueError(f"Failed to parse time input: {e}") from e

    @classmethod
    def format_utc_timestamp(cls, utc_time):
        day = utc_time.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]

        return utc_time.strftime(f"{day}{suffix} %B %Y - %I:%M %p UTC")


class GithubWebhookExtractor:
    @classmethod
    def get_PR_data(cls, event, payload):
        if event == "push":
            return cls.extract_push_data(payload)
        else:
            return cls.extract_PR_data(payload)

    def extract_push_data(payload):
        repo = payload.get("repository", {})
        pusher_info = payload.get("pusher", {})

        username = pusher_info.get("name")

        ref = payload.get("ref", "")
        branch = ref.split("/")[-1]

        pushed_at = repo.get("pushed_at")
        timestamp = DateTimeUtils.to_datetime(pushed_at)

        return {"username": username, "branch": branch, "timestamp": timestamp}

    def extract_PR_data(payload):
        action = payload.get("action", "")
        pr = payload.get("pull_request", {})
        username = pr.get("user", {}).get("login")
        head_branch = pr.get("head", {}).get("ref")
        base_branch = pr.get("base", {}).get("ref")
        is_merged = pr.get("merged", False)

        timestamp = None
        if action == "opened":
            timestamp = pr.get("created_at")

        if is_merged:
            timestamp = pr.get("merged_at")

        timestamp = DateTimeUtils.to_datetime(timestamp) if timestamp else None

        return {
            "action": action,
            "username": username,
            "head_branch": head_branch,
            "base_branch": base_branch,
            "is_merged": is_merged,
            "timestamp": timestamp,
        }
