import os
import sys
from collections.abc import Iterable

from pygeneral.print import ansi
from pygeneral.print.abstract import AbstractAnimation


class Multiple(list[AbstractAnimation]):
    """Display multiple animations at once."""

    _value: int | float
    _visible: bool

    def __init__(self, animations: Iterable[AbstractAnimation]) -> None:
        if os.name == "nt":
            raise OSError("This class is not supported on Windows.")
        super().__init__(animations)
        self._value = 0
        self._visible = False

    def draw(self) -> None:
        """Draw (or redraw) all animations, overwriting previous lines."""
        messages = self.make_message()
        ansi.hide_cursor()
        print(*messages, sep="\n", end="", file=sys.stderr, flush=True)
        self.move_up()

    def move_up(self) -> None:
        """Move the cursor up to the first line of the animations."""
        lines: int = len(self) - 1
        ansi.move_up(count=lines)

    def make_message(self) -> list[str]:
        """
        Build a list of lines to display, one for each animation.

        Returns:
            A list of lines that should be displayed.
        """
        return [x.make_message().lstrip("\n") for x in self]

    def __del__(self) -> None:
        ansi.show_cursor()

    def show(self) -> None:
        """Show the cursor."""
        self._visible = True
        for animation in self:
            animation.show()

    def hide(self) -> None:
        """Hide the cursor."""
        self._visible = False
        for animation in self:
            animation.hide()

    @property
    def value(self) -> int | float:
        """Get the current value of the animation."""
        return self._value

    @value.setter
    def value(self, value: int | float) -> None:
        """Set the current value of the animation."""
        if value != self._value:
            self._value = value
            for animation in self:
                animation.value = value
            if self._visible:
                self.draw()
