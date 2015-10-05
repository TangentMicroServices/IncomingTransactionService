from django.test import TestCase
from ifttt.helpers import IfThisThenThatHelpers, get_hipchat_message, quick_validate
import responses, json
from mock import patch

class MockResponse:

    def __init__(self, content, status_code=200):
        self.status_code=status_code
        self.content = json.dumps(content)

    def json(self):
        return json.loads(self.content)

class GenericHelpersTestCase(TestCase):

    def test_quick_validate_validation_fails(self):

        with self.assertRaises(AssertionError):
            quick_validate(['foo'], {})

    def test_quick_validate_valid_input(self):

        quick_validate(['foo'], {'foo':'bar'})


class HipchatIntegrationTestCase(TestCase):

    def test_get_hipchat_message_entered(self):
        user = {"first_name": "Joe"}
        project = {"title": "ACME"}

        message = get_hipchat_message(user, project, "entered")

        assert message == 'Joe has arrived at ACME'

    def test_get_hipchat_message_exited(self):
        user = {"first_name": "Joe"}
        project = {"title": "ACME"}

        message = get_hipchat_message(user, project, "exited")
        
        self.assertEqual(message, 'Joe has left ACME')

class TestIFTTTHelpers(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('ifttt.helpers.hipchat_speak')
    @patch('ifttt.helpers.get_project')
    @patch('ifttt.helpers.get_current_user')
    def test_post_to_hipchat(self, 
            mock_get_current_user, 
            mock_get_project,
            mock_hipchat_speak):

        mock_user_response = MockResponse({"first_name": "Joe"})
        mock_project_response = MockResponse({"title": "ACME"})

        mock_get_current_user.return_value = mock_user_response
        mock_get_project.return_value = mock_project_response
        
        payload = {
            'auth_token': '123',
            'user': 1,
            'project_id': 2,
            'entered_or_exited': 'entered'
        }

        # item under test:
        IfThisThenThatHelpers.post_to_hipchat(payload)

        # assertions
        mock_hipchat_speak.assert_called_with('Joe has arrived at ACME')
        
    def test_post_to_hipchat_no_user_found(self):
        '''
        TBD
        '''
        pass

    def test_post_to_hipchat_no_project_found(self):
        '''
        TBD
        '''
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
          "auth_token" : "abcdef123456"
        }

        result = IfThisThenThatHelpers.make_hours_post(data, 8)

        from requests import Response

        assert isinstance(result, Response)
        assert result.json() == mock_response
        assert result is not None, "Result Empty"
