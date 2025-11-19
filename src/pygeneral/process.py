import subprocess
import sys
import threading
from collections.abc import Callable
from typing import IO, cast, override

Sink = IO[str] | Callable[[str], None]


def stream_subprocess(
    command: list[str],
    stdout: Sink | list[Sink] | None = None,
    stderr: Sink | list[Sink] | None = None,
    **kwargs,
) -> int:
    """Run `command` as a subprocess while streaming its stdout and stderr.

    Args:
        command: The command to execute.
        stdout: Optional sinks or sink collections that receive stdout data.
        stderr: Optional sinks or sink collections that receive stderr data.
        **kwargs: Additional keyword arguments to pass to `subprocess.Popen`. The
            following kwargs cannot be overridden:
                - stdout: Set to `subprocess.PIPE`.
                - stderr: Set to `subprocess.PIPE`.
                - text: Set to `True`.
                - bufsize: Set to `1` (line-buffered).

    Returns:
        The return code of the subprocess.
    """
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    if stdout is None or stderr is None:
        raise ValueError(f"stdout and/or stderr is None: {stdout=}, {stderr=}")

    stdout = stdout if isinstance(stdout, list) else [stdout]
    stderr = stderr if isinstance(stderr, list) else [stderr]

    kwargs["bufsize"] = 1
    kwargs["stderr"] = subprocess.PIPE
    kwargs["stdout"] = subprocess.PIPE
    kwargs["text"] = True
    with subprocess.Popen(command, **kwargs) as process:
        return _stream(process, stdout, stderr)


def _stream(
    process: subprocess.Popen[str], stdout: list[Sink], stderr: list[Sink]
) -> int:
    """Stream stdout and stderr from a subprocess to standard streams.

    Args:
        process: The subprocess instance whose output will be streamed.
        stdout: Targets that receive stdout data.
        stderr: Targets that receive stderr data.

    Returns:
        The subprocess return code.
    """
    if process.stdout is None or process.stderr is None:
        raise RuntimeError(
            "Stdout and/or stderr cannot be None"
            f"{process.stdout=}, {process.stderr=}"
        )

    threads = [
        _Streamer(process.stdout, stdout),
        _Streamer(process.stderr, stderr),
    ]

    for thread in threads:
        thread.start()
    try:
        return_code = process.wait()
    finally:
        for thread in threads:
            thread.join()

    return return_code


class _Streamer(threading.Thread):
    """Stream lines from a text source into one or more targets."""

    _source: IO[str]
    _targets: list[tuple[Callable[[str], int | None], Callable[[], None]]]

    def __init__(self, source: IO[str], targets: list[Sink]) -> None:
        """Initialize a streamer.

        Args:
            source: The subprocess stream to read from.
            targets: Sinks that will receive the streamed text.
        """
        super().__init__(daemon=True)
        self._source = source
        self._targets = []
        for target in targets:
            write_callable = getattr(target, "write", None)
            if write_callable is None:
                write_callable = cast(Callable[[str], None], target)
            flush_callable = getattr(target, "flush", lambda: None)
            self._targets.append((write_callable, flush_callable))

    @override
    def run(self) -> None:
        """Continuously copy lines from the source to each target."""
        try:
            for line in self._source:
                for write, flush in self._targets:
                    write(line)
                    flush()
        finally:
            self._source.close()
