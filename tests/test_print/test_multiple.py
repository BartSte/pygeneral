from time import sleep
from unittest import TestCase

from pygeneral.print import Rotator
from pygeneral.print.multiple import Multiple


class TestMultiple(TestCase):
    pass


if __name__ == "__main__":
    # Draw a snake that zigzags across 4 lines.
    line1 = [
        "---->               ",
        " ----               ",
        "  ---               ",
        "   --               ",
        "    -               ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                   ^",
        "                   |",
        "                   |",
        "                   |",
        "                   |",
        "                    ",
        "                    ",
    ]
    line2 = [
        "                    ",
        "    v               ",
        "    |               ",
        "    |               ",
        "    |               ",
        "    |               ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                   ^",
        "                   |",
        "                   |",
        "                   |",
        "                   |",
        "                    ",
        "                    ",
        "                    ",
    ]
    line3 = [
        "                    ",
        "                    ",
        "    v               ",
        "    |               ",
        "    |               ",
        "    |               ",
        "    |               ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                   ^",
        "                   |",
        "                   |",
        "                   |",
        "                   |",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
    ]
    line4 = [
        "                    ",
        "                    ",
        "                    ",
        "    >               ",
        "    ->              ",
        "    -->             ",
        "    --->            ",
        "    ---->           ",
        "     ---->          ",
        "      ---->         ",
        "       ---->        ",
        "        ---->       ",
        "         ---->      ",
        "          ---->     ",
        "           ---->    ",
        "            ---->   ",
        "             ---->  ",
        "              ----> ",
        "               ---->",
        "                ----",
        "                 ---",
        "                  --",
        "                   -",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
        "                    ",
    ]
    animations = [Rotator(chars=line) for line in (line1, line2, line3, line4)]
    multiple = Multiple(animations)
    multiple.show()
    for i in range(100):
        multiple.value += 1
        sleep(0.2)
