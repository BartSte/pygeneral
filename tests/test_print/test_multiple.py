from time import sleep
from unittest import TestCase

from pygeneral.print.bar import ProgressBar
from pygeneral.print.counter import Counter
from pygeneral.print.multiple import Multiple
from pygeneral.print.rotator import Rotator


class TestMultiple(TestCase):
    pass


if __name__ == "__main__":
    counter = Counter(prefix="Counter: ", suffix=" of 100")
    bar = ProgressBar(prefix="Progress: ", suffix=" %", length=20)
    rotator = Rotator(prefix="Rotator: ", suffix="")
    multiple = Multiple([counter, bar, rotator])

    for i in range(101):
        counter.set_value_no_draw(i)
        bar.set_value_no_draw(i)
        rotator.set_value_no_draw(i)
        multiple.draw()
        sleep(0.1)
