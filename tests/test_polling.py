import unittest
from queue import Queue
from unittest.mock import Mock, patch

from herepy.polling import (
    MaxCallException,
    TimeoutException,
    is_truthy,
    poll,
    step_constant,
    step_linear_double,
)


class PollingTest(unittest.TestCase):
    def test_step_helpers_and_truthiness(self):
        self.assertEqual(step_constant(2), 2)
        self.assertEqual(step_linear_double(2), 4)
        self.assertTrue(is_truthy("ready"))
        self.assertFalse(is_truthy(""))

    @patch("herepy.polling.time.sleep")
    def test_poll_retries_with_arguments_and_collects_values(self, sleep):
        target = Mock(side_effect=[None, "ready"])
        values = Queue()

        result = poll(
            target,
            step=1,
            args=("item",),
            kwargs={"suffix": "!"},
            max_tries=2,
            check_success=lambda value: value == "ready",
            collect_values=values,
        )

        self.assertEqual(result, "ready")
        target.assert_any_call("item", suffix="!")
        self.assertEqual(values.get_nowait(), None)
        sleep.assert_called_once_with(1)

    @patch("herepy.polling.time.sleep")
    def test_poll_raises_after_max_tries(self, sleep):
        with self.assertRaises(MaxCallException) as error:
            poll(lambda: False, step=0, max_tries=2)

        self.assertEqual(error.exception.last, False)
        self.assertEqual([error.exception.values.get_nowait() for _ in range(2)], [False, False])
        self.assertEqual(sleep.call_count, 2)

    @patch("herepy.polling.time.sleep")
    @patch("herepy.polling.time.time", side_effect=[0, 2])
    def test_poll_raises_on_timeout_after_first_attempt(self, _time, sleep):
        with self.assertRaises(TimeoutException) as error:
            poll(lambda: False, step=0, timeout=1)

        self.assertFalse(error.exception.last)
        self.assertFalse(error.exception.values.get_nowait())
        sleep.assert_not_called()

    @patch("herepy.polling.time.sleep")
    def test_poll_collects_ignored_exceptions(self, sleep):
        target = Mock(side_effect=[ValueError("retry"), "ready"])
        values = Queue()

        result = poll(target, step=0, max_tries=2, ignore_exceptions=(ValueError,), collect_values=values)

        self.assertEqual(result, "ready")
        self.assertIsInstance(values.get_nowait(), ValueError)
        sleep.assert_called_once_with(0)

    def test_poll_requires_a_stop_condition(self):
        with self.assertRaisesRegex(AssertionError, "maximum number of tries or a timeout"):
            poll(lambda: True, step=0)
        with self.assertRaisesRegex(AssertionError, "cannot specify both"):
            poll(lambda: True, step=0, max_tries=1, poll_forever=True)

    def test_poll_does_not_swallow_unignored_exceptions(self):
        target = Mock(side_effect=ValueError("unexpected"))
        with self.assertRaisesRegex(ValueError, "unexpected"):
            poll(target, step=0, max_tries=1)
