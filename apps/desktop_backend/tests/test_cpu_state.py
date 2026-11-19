from app.adapters.fake_engine_adapter import FakeEngineAdapter


def test_cpu_state_matches_protocol_structure():
    engine = FakeEngineAdapter()

    state = engine.get_cpu_state()

    assert state["available"] is True
    assert state["source"] == "mock"
    assert state["halted"] is True
    assert state["updated_at"]

    expected_registers = {
        "r0", "r1", "r2", "r3", "r4", "r5",
        "r6", "r7", "r8", "r9", "r10", "r11",
        "r12", "sp", "lr", "pc", "xpsr"
    }

    assert set(state["registers"].keys()) == expected_registers

    for value in state["registers"].values():
        assert value is None or (
            isinstance(value, int) and 0 <= value <= 4294967295
        )


def test_cpu_state_changes_when_engine_starts():
    engine = FakeEngineAdapter()
    engine.loaded_firmware = "sample_firmware.bin"

    engine.start()

    state = engine.get_cpu_state()

    assert state["halted"] is False
    assert state["available"] is True


def test_cpu_state_is_halted_when_paused():
    engine = FakeEngineAdapter()
    engine.loaded_firmware = "sample_firmware.bin"

    engine.start()
    engine.pause()

    assert engine.get_cpu_state()["halted"] is True
