import subprocess
import sys
import threading
from typing import IO, TextIO, override


class _Streamer(threading.Thread):
    """Stream lines from a text source into a target on a background thread."""

    _source: IO[str]
    _target: TextIO

    def __init__(self, source: IO[str], target: TextIO):
        """Init.

        Args:
            source: Text stream to read from.
            target: Text stream to write to.
        """
        super().__init__(daemon=True)
        self._source = source
        self._target = target

    @override
    def run(self):
        """Continuously copy lines from the source to the target."""
        try:
            for line in self._source:
                self._target.write(line)
                self._target.flush()
        finally:
            self._source.close()


def stream_subprocess(command: list[str], **kwargs) -> int:
    """Run `command` as a subprocess while streaming its stdout and stderr.

    Args:
        command: The command to execute.
        **kwargs: Additional keyword arguments to pass to `subprocess.Popen`.
        The following kwargs cannot be overridden:
            - stdout: Set to `subprocess.PIPE`.
            - stderr: Set to `subprocess.PIPE`.
            - text: Set to `True`.
            - bufsize: Set to `1` (line-buffered).

    Returns:
        The return code of the subprocess.
    """
    kwargs["bufsize"] = 1
    kwargs["stderr"] = subprocess.PIPE
    kwargs["stdout"] = subprocess.PIPE
    kwargs["text"] = True

    with subprocess.Popen(command, **kwargs) as process:
        return _stream(process)


def _stream(process: subprocess.Popen[str]) -> int:
    """Stream stdout and stderr from a subprocess to standard streams.

    Args:
        process: The subprocess instance whose output will be streamed.

    Returns:
        The subprocess return code.
    """
    if process.stdout is None or process.stderr is None:
        raise RuntimeError(
            "Stdout and/or stderr cannot be None"
            f"{process.stdout=}, {process.stderr=}"
        )

    stdout_thread = _Streamer(process.stdout, sys.stdout)
    stderr_thread = _Streamer(process.stderr, sys.stderr)

    stdout_thread.start()
    stderr_thread.start()
    try:
        return_code = process.wait()
    finally:
        stdout_thread.join()
        stderr_thread.join()

    return return_code
