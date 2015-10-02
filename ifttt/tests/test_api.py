from django.test import TestCase, Client
from webhook.models import IncomingRequest
from ifttt.helpers import IfThisThenThatHelpers
import responses, json
from mock import patch, ANY


class TestIFTTTViewSetPOST(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_ifttt_enter(self):
        '''
        POST /ifttt/
        '''

        c = Client()
        response = c.post('/ifttt/', { 	"user": "4",
                                          "project_id": "2",
                                          "project_task_id": "23",
                                          "time": "October 1, 2015 at 04:34PM",
                                          "entered_or_exited": "entered",
                                          "auth_token" : "abcdef123456"})

        assert response.status_code == 200, 'Expect 200OK'

        icr_entry = IncomingRequest.objects.get(user=4)

        assert icr_entry is not None, 'Expect the Entry Record to Exist'


    @patch.object(IfThisThenThatHelpers, 'make_hours_post')
    def test_create_ifttt_exit(self, mock_get_hours_post):
        #Setup

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



    def test_create_ifttt_empty(self):
        '''
        POST /ifttt/
        '''

        c = Client()
        response = c.post('/ifttt/', {})
        assert response.status_code == 400, 'Expect 400ERROR'

    def test_create_ifttt_none(self):
        '''
        POST /ifttt/
        '''

        c = Client()
        response = c.post('/ifttt/')
        assert response.status_code == 400, 'Expect 400ERROR'
