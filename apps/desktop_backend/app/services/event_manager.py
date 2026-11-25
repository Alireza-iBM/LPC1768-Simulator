
from datetime import datetime, timezone
from uuid import uuid4


class EventManager:

    def __init__(self):
        self.events = []

    def emit(self, event_type, session_id=None, data=None, payload=None):
        # Support both the old "data" argument and the new "payload" argument.
        event_payload = payload if payload is not None else data

        event = {
            "schema_version": "1.0.0",
            "type": event_type,
            "event_id": str(uuid4()),
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": event_payload or {}
        }

        self.events.append(event)

        return event

    def get_events(self):
        return self.events.copy()

    def clear_events(self):
        self.events.clear()

        return {
            "success": True,
            "message": "Events cleared"
        }
