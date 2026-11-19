from datetime import datetime, timezone
from uuid import uuid4


class SessionManager:

    def __init__(self):
        self.sessions = {}

    def create_session(self, config=None):
        session_id = str(uuid4())

        session = {
            "session_id": session_id,
            "status": "created",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "config": config or {},
            "events": []
        }

        self.sessions[session_id] = session

        return session

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def update_status(self, session_id, status):
        valid_statuses = {
            "created",
            "ready",
            "running",
            "paused",
            "stopped",
            "error"
        }

        if status not in valid_statuses:
            raise ValueError(f"Invalid session status: {status}")

        session = self.get_session(session_id)

        if session is None:
            return False

        session["status"] = status
        session["updated_at"] = datetime.now(timezone.utc).isoformat()

        return True

    def list_sessions(self):
        return list(self.sessions.values())

    def delete_session(self, session_id):
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True

        return False

    def add_event(self, session_id, event):
        session = self.get_session(session_id)

        if session is None:
            return False

        session["events"].append(event)
        return True

    def get_session_events(self, session_id):
        session = self.get_session(session_id)

        if session is None:
            return None

        return session["events"].copy()
