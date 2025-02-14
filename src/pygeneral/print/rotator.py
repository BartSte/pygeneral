from typing import override

from pygeneral.print.abstract import AbstractAnimation


class Rotator(AbstractAnimation):
    """Rotate through a list of characters to create an animation"""

    _chars: list[str]
    prefix: str
    suffix: str

    def __init__(
        self, chars: list[str] | None = None, prefix: str = "", suffix: str = ""
    ):
        """Initializes a Spinner instance.

        Args:
            prefix: A string to display before the spinner.
                Defaults to an empty string.
            suffix: A string to display after the spinner.
                Defaults to an empty string.
        """
        super().__init__()
        self.prefix = prefix
        self.suffix = suffix
        self._chars = chars or ["|", "/", "-", "\\"]

    @override
    def make_message(self) -> str:
        """Return the message to display.

        Returns:
            str: The message to display.
        """
        index: int = int(self._value) % len(self._chars)
        char: str = self._chars[index]
        return f"\r{self.prefix}{char}{self.suffix}"
