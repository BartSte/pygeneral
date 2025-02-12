import sys


class ProgressBar:
    """A progress bar for the command line.

    This class represents a progress bar that can be drawn on the command line
    to indicate the progress of a task. Users can update the progress by setting
    the `value` property, or using the `set_value_quiet` method to update the
    value without redrawing immediately.
    """

    _length: int
    _max_value: int | float
    _min_value: int | float
    _value: int | float
    _template: str
    prefix: str
    suffix: str

    fill: str = "█"
    unfilled: str = "-"

    def __init__(
        self,
        min_value: int | float = 0,
        max_value: int | float = 100,
        prefix: str = "",
        suffix: str = "",
        length: int = 50,
        decimals: int = 0,
    ):
        """Initializes a ProgressBar instance.

        Args:
            min_value: The value at which the progress bar is empty.
                Defaults to 0.
            max_value: The value at which the progress bar is full.
                Defaults to 100.
            prefix: A string to display before the progress bar.
                Defaults to an empty string.
            suffix: A string to display after the progress bar.
                Defaults to an empty string.
            length: The character length of the progress bar itself.
                Defaults to 50.
            decimals: Number of decimals to show in the percentage.
                Defaults to 0.

        Raises:
            ValueError: If `min_value` is not less than `max_value`.
            ValueError: If `length` is less than or equal to 0.
            ValueError: If `fill` is not a single character.
        """
        self._min_value = min_value
        self._max_value = max_value
        self._length = length
        self.prefix = prefix
        self.suffix = suffix

        self._check()

        self._value = self._min_value
        self._template = (
            f"{{prefix}} |{{bar}}| {{percent:.{decimals}f}}% {{suffix}}"
        )

    def _check(self):
        """Checks the initialization arguments for validity.

        Raises:
            ValueError: If `min_value` >= `max_value`.
            ValueError: If `_length` <= 0.
            ValueError: If `fill` is not a single character.
        """
        if self._min_value >= self._max_value:
            raise ValueError("min_value must be less than max_value.")
        elif self._length <= 0:
            raise ValueError("length must be greater than 0.")
        elif len(self.fill) != 1:
            raise ValueError("fill must be a single character.")

    @property
    def value(self) -> int | float:
        """Gets the current value of the progress bar.

        Returns:
            int | float: The current progress value.
        """
        return self._value

    @value.setter
    def value(self, value: int | float):
        """Sets the current value and redraws the progress bar.

        Args:
            value: The new current value. If it differs from the
                existing value, the progress bar is redrawn.
        """
        if value != self._value:
            self._value = value
            self.draw()

    def set_value_quiet(self, value: int | float):
        """Sets the current value without drawing the progress bar.

        Args:
            value: The new current value.
        """
        self._value = value

    def draw(self):
        """Draws the progress bar to stdout.

        This method calculates the percentage of completion, constructs the
        bar string, and writes it to stdout in place (overwriting the previous
        line). It also flushes stdout immediately.
        """
        percent: float = self._calc_percent()
        bar: str = self._make_bar(percent)
        message: str = self._template.format(
            prefix=self.prefix, bar=bar, percent=percent, suffix=self.suffix
        )
        sys.stderr.write(f"\r{message}")
        sys.stderr.flush()

    def _make_message(self) -> str:
        """Constructs the current progress bar message.

        Returns:
            A string containing the prefix, progress bar, percentage, and
            suffix. If the progress is 100%, a newline is appended."""
        percent: float = self._calc_percent()
        bar: str = self._make_bar(percent)
        message: str = self._template.format(
            prefix=self.prefix, bar=bar, percent=percent, suffix=self.suffix
        )
        return f"\r{message}\n" if percent == 100 else f"\r{message}"

    def _calc_percent(self) -> float:
        """Calculates the current progress as a percentage of the total range.

        This method clamps the internal value between `min_value` and
        `max_value` to ensure the percentage never goes below 0% or above 100%.

        Returns:
            float: The current percentage of completion.
        """
        clamp: float = max(self._min_value, min(self._value, self._max_value))
        num: float = clamp - self._min_value
        den: float = self._max_value - self._min_value
        return (num / den) * 100

    def _make_bar(self, percent: float) -> str:
        """Constructs the visual progress bar based on the percentage.

        Args:
            percent: The current percentage of completion.

        Returns:
            A string containing a number of `fill` characters and `unfilled`
            characters, whose total length is equal to `_length`.
        """
        filled: int = int(self._length * percent // 100)
        unfilled: int = self._length - filled
        return self.fill * filled + self.unfilled * unfilled
