from time import sleep
from typing import override
from unittest import TestCase

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

    def test_counter(self):
        counter = Counter(goal=10)
        for i in range(10):
            self.cnt += 1
            counter.value += 1
            assert counter.make_message() == f"\r{self.cnt}/10"


if __name__ == "__main__":
    counter = Counter(goal=10, prefix="Counting: ", suffix=" seconds")
    for i in range(10):
        counter.value += 1
        sleep(.1)
    counter.show_cursor()
