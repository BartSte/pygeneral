import os
import unittest
from tempfile import TemporaryDirectory


from pygeneral import log


class TestSetup(unittest.TestCase):
    def test(self):
        with TemporaryDirectory() as tempdir:
            name = "test_logger"
            log_file = os.path.join(tempdir, f"{name}.log")
            obj = log.setup(name, log_file)
            obj.critical("Critical message")

            assert os.path.isfile(log_file)
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                assert "Critical message" in content
