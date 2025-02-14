import io
import unittest
from time import sleep
from unittest.mock import patch

from pygeneral.print.bar import ProgressBar


class TestProgressBar(unittest.TestCase):
    def test_init_defaults(self):
        """Test that ProgressBar initializes with default values correctly."""
        pb = ProgressBar()
        self.assertEqual(pb._min_value, 0)
        self.assertEqual(pb._max_value, 100)
        self.assertEqual(pb._length, 50)
        self.assertEqual(pb.value, 0)
        self.assertEqual(pb.fill, "█")
        self.assertEqual(pb.unfilled, "-")
        self.assertEqual(pb.prefix, "")
        self.assertEqual(pb.suffix, "")

    def test_init_valid_custom_values(self):
        """Test that ProgressBar accepts valid custom initialization values."""
        pb = ProgressBar(
            min_value=10, max_value=200, prefix="Start", suffix="End", length=40
        )
        self.assertEqual(pb._min_value, 10)
        self.assertEqual(pb._max_value, 200)
        self.assertEqual(pb._length, 40)
        self.assertEqual(pb.prefix, "Start")
        self.assertEqual(pb.suffix, "End")

    def test_init_invalid_min_max(self):
        """Test that providing min_value >= max_value raises ValueError."""
        with self.assertRaises(ValueError):
            ProgressBar(min_value=100, max_value=100)

        with self.assertRaises(ValueError):
            ProgressBar(min_value=101, max_value=100)

    def test_init_invalid_length(self):
        """Test that providing non-positive length raises ValueError."""
        with self.assertRaises(ValueError):
            ProgressBar(length=0)

        with self.assertRaises(ValueError):
            ProgressBar(length=-5)

    def test_init_invalid_fill(self):
        """Test that providing a fill character longer than 1 raises
        ValueError."""
        # fill is set by default in the class, but let's temporarily override
        original_fill = ProgressBar.fill
        try:
            ProgressBar.fill = "##"
            with self.assertRaises(ValueError):
                ProgressBar()
        finally:
            # Revert to the original fill to not affect other tests
            ProgressBar.fill = original_fill

    def test_value_setter_draw_call(self):
        """Test that setting `value` writes the progress bar to stdout."""
        pb = ProgressBar()

        # Capture output
        with patch("sys.stderr", new=io.StringIO()) as fake_out:
            pb.value = 50
            output = fake_out.getvalue()
            self.assertIn("50%", output, "Progress bar should show 50%.")
            # We expect the bar to be drawn once, because `value` changed.
            self.assertNotEqual(
                "", output, "Expected some output when value is set."
            )

    def test_value_setter_no_draw_when_same_value(self):
        """Test that setting the same value does not cause an additional
        draw."""
        pb = ProgressBar()
        pb.value = 50  # draw once

        # Capture output again and reassign to the same value
        with patch("sys.stderr", new=io.StringIO()) as fake_out:
            pb.value = 50
            output = fake_out.getvalue()
            self.assertEqual(
                "", output, "No output expected if value hasn't changed."
            )

    def test_set_value_quiet(self):
        """Test that set_value_quiet does not call draw."""
        pb = ProgressBar()
        with patch("sys.stderr", new=io.StringIO()) as fake_out:
            pb.set_value_no_draw(75)
            output = fake_out.getvalue()
            self.assertEqual(
                pb.value, 75, "Value should be updated internally."
            )
            self.assertEqual(
                "", output, "No output should be produced by set_value_quiet()."
            )

    def test_draw_manual_call(self):
        """Test drawing manually and check the output format."""
        pb = ProgressBar(min_value=0, max_value=100, length=10)
        pb.set_value_no_draw(50)

        with patch("sys.stderr", new=io.StringIO()) as fake_out:
            pb.draw()
            output = fake_out.getvalue()
            # For 50%, the bar should be half-filled
            self.assertIn("50%", output, "Output should contain 50%.")
            # 10-length bar => 5 filled, 5 unfilled
            self.assertIn("█" * 5, output, "Should have 5 fill chars.")
            self.assertIn("-" * 5, output, "Should have 5 unfilled chars.")

    def test_calc_percent_clamping(self):
        """Test that percent is clamped between min_value and max_value."""
        pb = ProgressBar(min_value=10, max_value=20)
        pb.set_value_no_draw(0)  # below min_value
        self.assertAlmostEqual(
            pb._calc_percent(), 0.0, msg="Should be clamped to 0%."
        )
        pb.set_value_no_draw(25)  # above max_value
        self.assertAlmostEqual(
            pb._calc_percent(), 100.0, msg="Should be clamped to 100%."
        )

    def test_complete_bar_output(self):
        """Test the output at 100%."""
        pb = ProgressBar()
        pb.set_value_no_draw(100)  # set to the max_value

        with patch("sys.stderr", new=io.StringIO()) as fake_out:
            pb.draw()
            output = fake_out.getvalue()
            self.assertIn("100%", output, "Output should contain 100%.")
            # By default, length=50, so the bar should be entirely filled
            self.assertIn(
                "█" * 50, output, "Bar should be fully filled at 100%."
            )


if __name__ == "__main__":
    bar = ProgressBar(
        min_value=0,
        max_value=100,
        prefix="Counting",
        suffix="Till 100",
        length=100,
    )
    for i in range(100):
        bar.value += 1
        sleep(0.01)
