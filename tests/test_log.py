import logging
import os
import unittest
from tempfile import TemporaryDirectory

import pygeneral.log


class TestSetup(unittest.TestCase):
    """Tests for the logging setup helper."""

    def test(self):
        """Ensures setup writes a critical message to the log file.

        Returns:
            None.
        """
        with TemporaryDirectory() as tempdir:
            name = "test_logger"
            log_file = os.path.join(tempdir, f"{name}.log")
            obj = pygeneral.log.setup(
                name, log_file, "%(message)s", logging.CRITICAL
            )
            obj.info("Info message")
            obj.critical("Critical message")

            assert os.path.isfile(log_file)
            with open(log_file, "r", encoding="utf-8") as f:
                assert "Critical message\n" == f.read()

    def test_debug(self):
        """Ensures setup writes a debug message to the log file.

        Returns:
            None.
        """
        with TemporaryDirectory() as tempdir:
            name = "test_logger"
            log_file = os.path.join(tempdir, f"{name}.log")
            obj = pygeneral.log.setup(name, log_file, loglevel=logging.DEBUG)
            obj.debug("Debug message")

            assert os.path.isfile(log_file)
            with open(log_file, "r", encoding="utf-8") as f:
                assert "Debug message" in f.read()
