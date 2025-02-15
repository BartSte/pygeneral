import os
import sys
from collections.abc import Iterable

from pygeneral.print import ansi
from pygeneral.print.abstract import AbstractAnimation


class Multiple(list[AbstractAnimation]):
    """Display multiple animations at once."""

    def __init__(self, animations: Iterable[AbstractAnimation]) -> None:
        if os.name == "nt":
            raise OSError("This class is not supported on Windows.")
        super().__init__(animations)

    def draw(self) -> None:
        """Draw (or redraw) all animations, overwriting previous lines."""
        messages = self.make_message()
        print(ansi.HIDE_CURSOR, end="", file=sys.stderr)
        print(*messages, sep="\n", end="", file=sys.stderr, flush=True)
        self.move_up()

    def move_up(self) -> None:
        """Move the cursor up to the first line of the animations."""
        lines: int = len(self) - 1
        print(ansi.MOVE_UP * lines, end="", file=sys.stderr)

    def make_message(self) -> list[str]:
        """
        Build a list of lines to display, one for each animation.

        Returns:
            A list of lines that should be displayed.
        """
        return [x.make_message().lstrip("\n") for x in self]

    def __del__(self) -> None:
        print(ansi.SHOW_CURSOR, end="", file=sys.stderr, flush=True)
