from django.test import TestCase
from ifttt.helpers import IfThisThenThatHelpers

class TestIFTTTHelpers(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_negative_time_diff(self):
        enter = "April 29, 2013 at 12:01PM"
        exit = "April 29, 2013 at 08:01PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)
        assert result < 0, 'Less than 0 hours'

    def test_over_day_time_diff(self):
        enter = "April 29, 2013 at 12:01PM"
        exit = "April 31, 2013 at 12:01PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)
        assert result > 24, 'More than 24 hours'

    def test_zero_time_diff(self):
        enter = "April 29, 2013 at 12:01PM"
        exit = "April 29, 2013 at 12:01PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)
        assert result == 0, 'Equals 0 hours'
