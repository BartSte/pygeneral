import time
from typing import override

from pygeneral.print import ansi
from pygeneral.print.abstract import AbstractAnimation


class DottedLine(AbstractAnimation):
    """A dotted line animation that moves left and right.

    Attributes:
        length: Total width of the animation in characters
        speed: Number of steps between position updates
        position: Current position of the leading dot
        direction: Current movement direction (1 for right, -1 for left)
    """

    def __init__(
        self,
        length: int = 20,
        speed: int = 1,
        prefix: str = "",
        suffix: str = "",
    ):
        """Initialize the dotted line animation.

        Args:
            length: Total width of the animation
            speed: Steps between position updates (higher = slower)
            prefix: Text to display before the animation
            suffix: Text to display after the animation
        """
        super().__init__()
        self.length = length
        self.speed = speed
        self.prefix = prefix
        self.suffix = suffix
        self._position = 0
        self._direction = 1
        self._step_counter = 0

    @property
    def position(self) -> int:
        """Get current dot position."""
        return self._position

    @override
    def make_message(self) -> str:
        """Generate the dotted line string."""
        self._step_counter += 1
        if self._step_counter >= self.speed:
            self._step_counter = 0
            self._position += self._direction
            if self._position >= self.length - 1 or self._position <= 0:
                self._direction *= -1

        line = ["."] * self.length
        line[self._position] = "o"
        return (
            f"{ansi.MOVE_UP}{ansi.CLEAR_LINE}\r{self.prefix}{''.join(line)}"
            f"{self.suffix}"
        )

    def animate(self, duration: float = 5.0):
        """Run the animation for specified duration."""
        self.show()
        start = time.time()
        while time.time() - start < duration:
            self.draw()
            time.sleep(0.1)
        self.hide()
