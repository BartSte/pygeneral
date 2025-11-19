import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from pygeneral.process import stream_subprocess


class StreamSubprocessTests(unittest.TestCase):
    """Tests for stream_subprocess."""

    def test_stream_subprocess_success(self) -> None:
        """Test that a successful subprocess streams output correctly."""
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        command = [
            sys.executable,
            "-c",
            "import sys; print('Hello World!'); sys.exit(0)",
        ]

        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            return_code = stream_subprocess(command)

        self.assertEqual(return_code, 0)
        self.assertEqual(stdout_buffer.getvalue(), "Hello World!\n")
        self.assertEqual(stderr_buffer.getvalue(), "")

    def test_stream_subprocess_failure(self) -> None:
        """Test that a failing subprocess streams output and returns its code."""
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        command = [
            sys.executable,
            "-c",
            (
                "import sys; sys.stdout.write('Oops\\n'); "
                "sys.stderr.write('Bad things happened\\n'); sys.exit(3)"
            ),
        ]

        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            return_code = stream_subprocess(command)

        self.assertEqual(return_code, 3)
        self.assertEqual(stdout_buffer.getvalue(), "Oops\n")
        self.assertEqual(stderr_buffer.getvalue(), "Bad things happened\n")

    def test_stream_subprocess_custom_sinks(self) -> None:
        """Test that explicit stdout and stderr sinks capture the output."""
        stdout_buffer = StringIO()
        stderr_buffer = StringIO()
        command = [
            sys.executable,
            "-c",
            (
                "import sys; print('custom stdout'); "
                "sys.stderr.write('custom stderr\\n'); sys.exit(0)"
            ),
        ]

        return_code = stream_subprocess(
            command, stdout=stdout_buffer, stderr=stderr_buffer
        )

        self.assertEqual(return_code, 0)
        self.assertEqual(stdout_buffer.getvalue(), "custom stdout\n")
        self.assertEqual(stderr_buffer.getvalue(), "custom stderr\n")

    def test_stream_subprocess_multiple_stdout_targets(self) -> None:
        """Test that multiple stdout targets each receive the same output."""
        first_buffer = StringIO()
        second_buffer = StringIO()
        command = [
            sys.executable,
            "-c",
            "import sys; print('fan out'); sys.exit(0)",
        ]

        return_code = stream_subprocess(
            command, stdout=[first_buffer, second_buffer]
        )

        self.assertEqual(return_code, 0)
        expected_output = "fan out\n"
        self.assertEqual(first_buffer.getvalue(), expected_output)
        self.assertEqual(second_buffer.getvalue(), expected_output)

    def test_stream_subprocess_callable_sink(self) -> None:
        """Test that a callable sink receives each stdout line."""
        captured: list[str] = []
        command = [
            sys.executable,
            "-c",
            "import sys; print('callable sink'); sys.exit(0)",
        ]

        return_code = stream_subprocess(command, stdout=captured.append)

        self.assertEqual(return_code, 0)
        self.assertEqual(captured, ["callable sink\n"])
