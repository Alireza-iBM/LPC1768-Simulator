
from app.services.event_manager import EventManager


def test_event_has_protocol_envelope():
    manager = EventManager()

    event = manager.emit(
        "LOG",
        session_id="test-session",
        payload={
            "level": "info",
            "message": "Test message",
            "component": "backend"
        }
    )

    assert event["schema_version"] == "1.0.0"
    assert event["type"] == "LOG"
    assert event["event_id"]
    assert event["session_id"] == "test-session"
    assert event["timestamp"]
    assert event["payload"]["message"] == "Test message"

    assert "event" not in event
    assert "data" not in event


def test_event_ids_are_unique():
    manager = EventManager()

    first = manager.emit("LOG")
    second = manager.emit("LOG")

    assert first["event_id"] != second["event_id"]


def test_emit_supports_old_data_argument():
    manager = EventManager()

    event = manager.emit(
        "LOG",
        data={"message": "Old format"}
    )

    assert event["payload"] == {"message": "Old format"}


def test_clear_events():
    manager = EventManager()

    manager.emit("LOG")
    result = manager.clear_events()

    assert result["success"] is True
    assert manager.get_events() == []
