import pytest

from app.sessions.session_manager import SessionManager


def test_update_session_status():
    manager = SessionManager()
    session = manager.create_session()

    updated = manager.update_status(
        session["session_id"],
        "running"
    )

    assert updated is True
    assert manager.get_session(session["session_id"])["status"] == "running"


def test_update_status_for_missing_session():
    manager = SessionManager()

    updated = manager.update_status(
        "non-existent-session",
        "running"
    )

    assert updated is False


def test_update_session_with_invalid_status():
    manager = SessionManager()
    session = manager.create_session()

    with pytest.raises(ValueError):
        manager.update_status(
            session["session_id"],
            "invalid_status"
        )
