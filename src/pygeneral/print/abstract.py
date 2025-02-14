import sys
from abc import ABC, abstractmethod


class AbstractAnimation(ABC):
    """Abstract class for animations.

    Will write to stderr each time its `value` is changed.
    """

    _value: int | float

    def __init__(self, value: int | float = 0):
        """Initialize the animation."""
        self._value = 0

    @property
    def value(self) -> int | float:
        """Get the current value of the animation.

        Returns:
            int | float: The current value of the animation.
        """
        return self._value

    @value.setter
    def value(self, value: int | float):
        """Set the current value of the animation.

        Args:
            value: The new current value of the animation.
        """
        if value != self._value:
            self._value = value
            self.draw()

    def draw(self):
        """Draw the animation."""
        message = self.make_message()
        print(message, end="", file=sys.stderr, flush=True)
        self.hide_cursor()

    @abstractmethod
    def make_message(self) -> str:
        """Return the message to display.

        Returns:
            str: The message to display.
        """

    def set_value_no_draw(self, value: int | float):
        """Set the current value of the animation without drawing it.

        Args:
            value: The new current value of the animation.
        """
        self._value = value

    @staticmethod
    def hide_cursor():
        """Hide the cursor"""
        print("\033[?25l", end="", file=sys.stderr, flush=True)

    @staticmethod
    def show_cursor():
        """Show the cursor"""
        print("\033[?25h", end="", file=sys.stderr, flush=True)
