from datetime import datetime, timezone


class EventManager:

    def __init__(self):
        self.events = []

    def emit(self, event_type, session_id=None, data=None):
        event = {
            "event": event_type,
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data or {}
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