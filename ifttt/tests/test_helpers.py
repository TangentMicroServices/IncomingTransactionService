from django.test import TestCase
from ifttt.helpers import IfThisThenThatHelpers

class TestIFTTTHelpers(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_correctly_calculate_difference_in_hours(self):
        enter = "April 29, 2013 at 08:01PM"
        exit = "April 29, 2013 at 09:01PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)

        assert result == 1, 'Expect 1 hour to be returned (result = {})' .format (result)


    def test_should_round_up_half_hour(self):
        enter = "April 29, 2013 at 08:0PM"
        exit = "April 29, 2013 at 08:31PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)

        assert result == 1, 'Expect 1 hour to be returned (result = {})' .format (result)

    def test_should_round_down_under_half_hour(self):
        enter = "April 29, 2013 at 08:0PM"
        exit = "April 29, 2013 at 08:29PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)

        assert result == 0, 'Expect 1 hour to be returned (result = {})' .format (result)


    def test_negative_time_diff(self):
        enter = "April 29, 2013 at 09:01PM"
        exit = "April 29, 2013 at 08:01PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)

        assert result < 0, 'Less than 0 hours'

    def test_over_day_time_diff(self):
        enter = "April 23, 2013 at 12:01PM"
        exit = "April 24, 2013 at 12:01PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)

        assert result == 24, 'More than 24 hours. result = {}' . format (result)

    def test_zero_time_diff(self):
        enter = "April 29, 2013 at 12:01PM"
        exit = "April 29, 2013 at 12:01PM"

        result = IfThisThenThatHelpers.calculate_hours_diff(enter, exit)

        assert result == 0, 'Equals 0 hours'
