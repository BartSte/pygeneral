from time import sleep
from typing import override
from unittest import TestCase
from unittest.mock import patch

from pygeneral.print import Counter


class TestCounter(TestCase):
    """Test case for StdoutCounter.

    Attributes:
        cnt: the current count.
    """

    cnt: int

    @override
    def setUp(self):
        self.cnt = 0

    @patch("sys.stderr.write")
    def test_counter(self, patched_write):
        def assert_write(actual: str):
            assert actual == f"\r{self.cnt}/10"

        patched_write.side_effect = assert_write

        counter = Counter(goal=10)
        for i in range(10):
            self.cnt += 1
            counter.value += 1


if __name__ == "__main__":
    counter = Counter(goal=10, prefix="Counting: ", suffix=" seconds")
    for i in range(10):
        counter.value += 1
        sleep(1)
