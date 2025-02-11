from os.path import join
from subprocess import check_output
from unittest import TestCase

from tests import paths


class TestLenSort(TestCase):
    EXPECTED = b"\n=;\nx = 1;\nxx = 2;\nxxx = 3;\nxxxx = 4;\nxxxxx === 5;\n"

    def test(self) -> None:
        """"""
        test_lines_file: str = join(paths.static, "test_lines.txt")
        stdout = check_output(["lensort", "=", "-f", test_lines_file])
        self.assertEqual(self.EXPECTED, stdout)
