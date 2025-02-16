import unittest
from time import sleep
from unittest.mock import MagicMock, patch

from pygeneral.print import Rotator
from pygeneral.print.abstract import AbstractAnimation
from pygeneral.print.multiple import Multiple


class TestMultiple(unittest.TestCase):
    def setUp(self):
        self.animations = [MagicMock(spec=AbstractAnimation) for _ in range(3)]
        self.multiple = Multiple(self.animations)

    @patch("pygeneral.print.ansi.hide_cursor")
    @patch("pygeneral.print.ansi.move_up")
    def test_draw(self, mock_move_up, mock_hide_cursor):
        self.multiple.draw()
        mock_hide_cursor.assert_called_once()
        mock_move_up.assert_called_once_with(count=2)
        for animation in self.animations:
            animation.make_message.assert_called_once()

    @patch("pygeneral.print.ansi.move_up")
    def test_move_up(self, mock_move_up):
        self.multiple.move_up()
        mock_move_up.assert_called_once_with(count=2)

    def test_make_message(self):
        messages = self.multiple.make_message()
        self.assertEqual(len(messages), 3)
        for animation in self.animations:
            animation.make_message.assert_called_once()

    @patch("pygeneral.print.ansi.show_cursor")
    def test_del(self, mock_show_cursor):
        del self.multiple
        mock_show_cursor.assert_called_once()

    def test_show(self):
        self.multiple.show()
        self.assertTrue(self.multiple._visible)
        for animation in self.animations:
            animation.show.assert_called_once()

    def test_hide(self):
        self.multiple.hide()
        self.assertFalse(self.multiple._visible)
        for animation in self.animations:
            animation.hide.assert_called_once()

    def test_value_getter(self):
        self.assertEqual(self.multiple.value, 0)

    def test_value_setter(self):
        self.multiple.value = 10
        self.assertEqual(self.multiple.value, 10)
        for animation in self.animations:
            self.assertEqual(animation.value, 10)

    @patch.object(Multiple, "draw")
    def test_value_setter_draw(self, mock_draw):
        self.multiple._visible = True
        self.multiple.value = 20
        mock_draw.assert_called_once()


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
