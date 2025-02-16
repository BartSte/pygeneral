import sys
from abc import ABC, abstractmethod

from pygeneral.print import ansi


class AbstractAnimation(ABC):
    """Abstract class for animations.

    Will write to stderr each time its `value` is changed.
    """

    _value: int | float
    _visible: bool

    def __init__(self, value: int | float = 0):
        """Initialize the animation."""
        self._value = 0
        self._visible = False

    @property
    def value(self) -> int | float:
        """Get the current value of the animation.

        Returns:
            int | float: The current value of the animation.
        """
        return self._value

    def set_value_no_draw(self, value: int | float):
        """Set the current value of the animation without drawing it.

        Args:
            value: The new current value of the animation.
        """
        self._value = value

    @value.setter
    def value(self, value: int | float):
        """Set the current value of the animation.

        Args:
            value: The new current value of the animation.
        """
        if value != self._value:
            self._value = value
            if self._visible:
                self.draw()

    def draw(self):
        """Draw the animation."""
        message = self.make_message()
        print(message, end="", file=sys.stderr, flush=True)
        ansi.hide_cursor()

    @abstractmethod
    def make_message(self) -> str:
        """Return the message to display.

        Returns:
            str: The message to display.
        """

    def __del__(self):
        """Destructor to show the cursor when the object is deleted."""
        ansi.show_cursor()

    def show(self):
        """Show the animation."""
        self._visible = True
        self.draw()

    def hide(self):
        """Hide the animation."""
        self._visible = False
        ansi.show_cursor()

