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
