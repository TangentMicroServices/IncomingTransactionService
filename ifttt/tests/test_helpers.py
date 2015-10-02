from django.test import TestCase
from ifttt.helpers import IfThisThenThatHelpers
import responses, json

class TestIFTTTHelpers(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calculate_difference(self):
        inputs = [
            ("April 29, 2013 at 08:01PM", "April 29, 2013 at 09:01PM", 1),
            ("April 29, 2013 at 08:01PM", "April 29, 2013 at 08:32PM", 1),
            ("April 29, 2013 at 08:01PM", "April 29, 2013 at 08:29PM", 0),
        ]

        for entered, exited, expected in inputs:
            result = IfThisThenThatHelpers.calculate_hours_diff(entered, exited)
            assert result == expected, 'Expect {} to be {})' .format (result, expected)

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

    @responses.activate
    def test_hours_service_post(self):

        mock_response = {
            "foo":"bar",            
        }

        responses.add(responses.POST, "http://hoursservice.staging.tangentmicroservices.com/api/v1/entry/",
                  body=json.dumps(mock_response),
                  content_type="application/json",
                  status=200)

        data = { "user": "3",
          "project_id": "43",
          "project_task_id": "57",
          "time": "October 1, 2015 at 09:34PM",
          "entered_or_exited": "exited",
          "auth_token" : "371d3b5584b977abb8005e57eb04aacc76b703f1"
        }

        result = IfThisThenThatHelpers.make_hours_post(data, 8)
        
        from requests import Response

        assert isinstance(result, Response)
        assert result.json() == mock_response
        assert result is not None, "Result Empty"
