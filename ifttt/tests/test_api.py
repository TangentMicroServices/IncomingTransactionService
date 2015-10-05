from django.test import TestCase, Client
from webhook.models import IncomingRequest
from ifttt.helpers import IfThisThenThatHelpers
import responses, json
from mock import patch, ANY


class TestIFTTTViewSetPOST(TestCase):

    @patch.object(IfThisThenThatHelpers, 'post_to_hipchat')
    def test_create_ifttt_enter(self, mock_post_to_hipchat):
        '''
        POST /ifttt/
        '''

        c = Client()
        data = {  "user": "4",
                  "project_id": "2",
                  "project_task_id": "23",
                  "time": "October 1, 2015 at 04:34PM",
                  "entered_or_exited": "entered",
                  "auth_token" : "abcdef123456"
                }
        response = c.post('/ifttt/', data)

        assert response.status_code == 200, 'Expect 200OK'

        icr_entry = IncomingRequest.objects.get(user=4)

        assert icr_entry is not None, 'Expect the Entry Record to Exist'
        assert mock_post_to_hipchat.called == True, 'Expect hipchat message to have been posted'

    @patch('ifttt.helpers.hipchat_speak')
    @patch.object(IfThisThenThatHelpers, 'post_to_hipchat')
    @patch.object(IfThisThenThatHelpers, 'make_hours_post')
    def test_create_ifttt_exit(self, 
        mock_get_hours_post, 
        mock_post_to_hipchat,
        mock_hipchat_speak):
        
        mock_get_hours_post.return_value = {}

        data ={"user": "4",
               "project_id": "2",
               "project_task_id": "23",
               "time": "October 1, 2015 at 04:34PM",
               "entered_or_exited": "entered",
               "auth_token" : "abcdef123456"}

        IncomingRequest.objects.create(user=4, payload=json.dumps(data))

        c = Client()
        exit_payload = {  "user": "4",
                          "project_id": "2",
                          "project_task_id": "23",
                          "time": "October 1, 2015 at 09:34PM",
                          "entered_or_exited": "exited",
                          "auth_token" : "abcdef123456"
                        }
        response = c.post('/ifttt/', exit_payload)

        assert response.status_code == 200, 'Expect 200OK'

        icr_entry = IncomingRequest.objects.filter(user=4)[1]

        mock_get_hours_post.assert_called_with(ANY, 5)

        assert icr_entry is not None, 'Expect the Exit Record to Exist'
        assert icr_entry.payload_as_json == exit_payload, 'Expect {} to equal {}'. format(icr_entry.payload_as_json, exit_payload)
        assert mock_post_to_hipchat.called == True, 'Expect hipchat message to have been posted'
        #mock_hipchat_speak.assert_called_with('5 hours logged')

    def test_create_ifttt_empty(self):
        '''
        POST /ifttt/
        '''

        c = Client()
        response = c.post('/ifttt/', {})
        assert response.status_code == 400, 'Expect 400 ERROR'

    def test_create_ifttt_none(self):
        '''
        POST /ifttt/
        '''

        c = Client()
        response = c.post('/ifttt/')
        assert response.status_code == 400, 'Expect 400 ERROR'
