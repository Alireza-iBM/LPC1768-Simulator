import asyncio
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProcessRecord:
    session_id: str
    process: asyncio.subprocess.Process
    stdout: list[str] = field(default_factory=list)
    stderr: list[str] = field(default_factory=list)
    return_code: Optional[int] = None
    stdout_task: Optional[asyncio.Task] = None
    stderr_task: Optional[asyncio.Task] = None
    wait_task: Optional[asyncio.Task] = None


class QemuProcessManager:
    """
    Manages external processes used by simulation sessions.

    Processes are launched without a shell.
    Each session has its own lock to prevent duplicate processes.
    """

    def __init__(self, max_output_lines: int = 1000):
        if max_output_lines < 1:
            raise ValueError("max_output_lines must be greater than zero")

        self.max_output_lines = max_output_lines
        self._processes: dict[str, ProcessRecord] = {}
        self._session_locks: dict[str, asyncio.Lock] = {}

    def _get_lock(self, session_id: str) -> asyncio.Lock:
        if session_id not in self._session_locks:
            self._session_locks[session_id] = asyncio.Lock()

        return self._session_locks[session_id]

    async def start(
        self,
        session_id: str,
        executable: str,
        args: Optional[list[str]] = None,
        cwd: Optional[str] = None,
        env: Optional[dict[str, str]] = None,
    ) -> dict:

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id cannot be empty")

        if not isinstance(executable, str) or not executable.strip():
            raise ValueError("executable cannot be empty")

        args = [] if args is None else args

        if not isinstance(args, (list, tuple)):
            raise TypeError("args must be a list or tuple of strings")

        if not all(isinstance(arg, str) for arg in args):
            raise TypeError("all process arguments must be strings")

        async with self._get_lock(session_id):
            existing = self._processes.get(session_id)

            if existing is not None:
                if existing.process.returncode is None:
                    return {
                        "success": False,
                        "message": "A process is already running for this session.",
                        "pid": existing.process.pid,
                    }

                if existing.wait_task is not None:
                    await existing.wait_task

            try:
                process = await asyncio.create_subprocess_exec(
                    executable,
                    *args,
                    cwd=cwd,
                    env=env,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

            except OSError as exc:
                return {
                    "success": False,
                    "message": f"Could not start process: {exc}",
                    "error": type(exc).__name__,
                }

            record = ProcessRecord(
                session_id=session_id,
                process=process,
            )

            self._processes[session_id] = record

            record.stdout_task = asyncio.create_task(
                self._read_output(process.stdout, record.stdout)
            )

            record.stderr_task = asyncio.create_task(
                self._read_output(process.stderr, record.stderr)
            )

            record.wait_task = asyncio.create_task(
                self._wait_for_process(record)
            )

            return {
                "success": True,
                "session_id": session_id,
                "pid": process.pid,
                "message": "Process started successfully.",
            }

    async def _read_output(self, stream, destination: list[str]) -> None:
        if stream is None:
            return

        while True:
            line = await stream.readline()

            if not line:
                break

            destination.append(
                line.decode("utf-8", errors="replace").rstrip("\r\n")
            )

            if len(destination) > self.max_output_lines:
                del destination[0]

    async def _wait_for_process(self, record: ProcessRecord) -> None:
        record.return_code = await record.process.wait()

        await asyncio.gather(
            record.stdout_task,
            record.stderr_task,
        )

    def get_status(self, session_id: str) -> Optional[dict]:
        record = self._processes.get(session_id)

        if record is None:
            return None

        return_code = (
            record.return_code
            if record.return_code is not None
            else record.process.returncode
        )

        return {
            "session_id": session_id,
            "pid": record.process.pid,
            "running": return_code is None,
            "return_code": return_code,
            "stdout": record.stdout.copy(),
            "stderr": record.stderr.copy(),
        }

    async def stop(
        self,
        session_id: str,
        timeout: float = 5.0,
    ) -> dict:

        if timeout < 0:
            raise ValueError("timeout cannot be negative")

        async with self._get_lock(session_id):
            record = self._processes.get(session_id)

            if record is None:
                return {
                    "success": False,
                    "message": "No process found for this session.",
                }

            if record.process.returncode is not None:
                await record.wait_task

                return {
                    "success": True,
                    "session_id": session_id,
                    "return_code": record.return_code,
                    "message": "Process has already exited.",
                }

            try:
                record.process.terminate()
            except ProcessLookupError:
                pass

            try:
                await asyncio.wait_for(
                    asyncio.shield(record.wait_task),
                    timeout=timeout,
                )

            except asyncio.TimeoutError:
                if record.process.returncode is None:
                    try:
                        record.process.kill()
                    except ProcessLookupError:
                        pass

                await record.wait_task

            return {
                "success": True,
                "session_id": session_id,
                "return_code": record.return_code,
                "message": "Process stopped.",
            }

    async def stop_all(self, timeout: float = 5.0) -> None:
        session_ids = list(self._processes.keys())

        for session_id in session_ids:
            await self.stop(session_id, timeout=timeout)
