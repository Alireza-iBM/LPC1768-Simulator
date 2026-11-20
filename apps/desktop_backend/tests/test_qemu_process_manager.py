import asyncio
import sys
import unittest

from app.processes.qemu_process_manager import QemuProcessManager


class TestQemuProcessManager(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.manager = QemuProcessManager(max_output_lines=1000)

    async def asyncTearDown(self):
        await self.manager.stop_all(timeout=1)

    async def wait_until_finished(self, session_id, timeout=5, manager=None):
        for _ in range(int(timeout / 0.05)):
            status = (manager or self.manager).get_status(session_id)

            if status is not None and not status["running"]:
                return status

            await asyncio.sleep(0.05)

        self.fail("Process did not finish within the expected time.")

    async def test_start_and_capture_output(self):
        result = await self.manager.start(
            session_id="test-output",
            executable=sys.executable,
            args=[
                "-c",
                "import sys; print('hello stdout'); print('hello stderr', file=sys.stderr)"
            ],
        )

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["pid"])

        status = await self.wait_until_finished("test-output")

        self.assertEqual(status["return_code"], 0)
        self.assertIn("hello stdout", status["stdout"])
        self.assertIn("hello stderr", status["stderr"])

    async def test_stop_running_process(self):
        result = await self.manager.start(
            session_id="test-stop",
            executable=sys.executable,
            args=["-c", "import time; time.sleep(30)"],
        )

        self.assertTrue(result["success"])

        stop_result = await self.manager.stop(
            "test-stop",
            timeout=2,
        )

        self.assertTrue(stop_result["success"])

        status = self.manager.get_status("test-stop")
        self.assertFalse(status["running"])
        self.assertIsNotNone(status["return_code"])

    async def test_prevent_duplicate_process_for_session(self):
        first = await self.manager.start(
            session_id="test-duplicate",
            executable=sys.executable,
            args=["-c", "import time; time.sleep(30)"],
        )

        second = await self.manager.start(
            session_id="test-duplicate",
            executable=sys.executable,
            args=["-c", "print('should not run')"],
        )

        self.assertTrue(first["success"])
        self.assertFalse(second["success"])

        await self.manager.stop("test-duplicate", timeout=2)

    async def test_output_line_limit(self):
        manager = QemuProcessManager(max_output_lines=2)

        try:
            await manager.start(
                session_id="test-output-limit",
                executable=sys.executable,
                args=[
                    "-c",
                    "print('line1'); print('line2'); print('line3')",
                ],
            )

            status = await self.wait_until_finished("test-output-limit", manager=manager)

            self.assertEqual(
                status["stdout"],
                ["line2", "line3"],
            )
        finally:
            await manager.stop_all(timeout=1)

    async def test_invalid_executable_returns_error(self):
        result = await self.manager.start(
            session_id="test-invalid-executable",
            executable="this_executable_does_not_exist_12345",
        )
        self.assertFalse(result["success"])
        self.assertIn("message", result)

    async def test_concurrent_start_for_same_session(self):
        try:
            results = await asyncio.gather(
                self.manager.start(
                    session_id="test-concurrent",
                    executable=sys.executable,
                    args=["-c", "import time; time.sleep(10)"],
                ),
                self.manager.start(
                    session_id="test-concurrent",
                    executable=sys.executable,
                    args=["-c", "import time; time.sleep(10)"],
                ),
            )

            successful_starts = [
                result for result in results if result["success"]
            ]

            self.assertEqual(len(successful_starts), 1)

        finally:
            await self.manager.stop("test-concurrent", timeout=2)


if __name__ == "__main__":
    unittest.main()
