import sys
from os import mkdir
from os.path import join
from tempfile import TemporaryDirectory
from unittest import TestCase

from pygeneral import path
from pygeneral.exceptions import PathError


class TestModule(TestCase):
    def test_valid(self):
        with TemporaryDirectory() as temp_dir:
            open(join(temp_dir, "module_as_file.py"), "w")
            sys.path.append(temp_dir)
            import module_as_file  # pyright: ignore

            assert path.module(module_as_file) == temp_dir

    def test_valid_dir(self):
        with TemporaryDirectory() as temp_dir:
            sys.path.append(temp_dir)
            dir: str = join(temp_dir, "module_as_dir")
            mkdir(dir)
            import module_as_dir  # pyright: ignore

            assert path.module(module_as_dir) == dir

    def test_invalid(self):
        with self.assertRaises(PathError):
            path.module(object)  # pyright: ignore
