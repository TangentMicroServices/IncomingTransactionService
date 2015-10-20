"""
Integration tests.
Run with:

python manage.py test -p integration_test*

Be careful. These will make actual posts to actual services
"""
from django.test import TestCase, Client, override_settings
from ifttt.helpers import get_current_user, get_project, hipchat_speak
from django.conf import settings
from webhook.models import IncomingRequest
import json

token = '5e971505f6901ec76bfb53c990b2ab488d2d08e6'

class TestHipchatIntegration(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        '''
        Cleanup after each test: clear all incoming requests
        '''
        for req in IncomingRequest.objects.all(): req.delete()

    def test_post_to_hipchat(self):
        response = hipchat_speak("Testing 1, 2, 3", "Test Robot")
        assert response.status_code == 200

class TestUserServiceIntegration(TestCase):

    @override_settings(MICROSERVICE_TLD='staging.tangentmicroservices.com')
    def test_get_current_user(self):

        response = get_current_user(token, 3)
        assert response.status_code == 200

class TestProjectServiceIntegration(TestCase):

    @override_settings(MICROSERVICE_TLD='staging.tangentmicroservices.com')
    def test_get_project(self):
        response = get_project(token, 3)
        assert response.status_code == 200

class TestIFTTTAPIIntegration(TestCase):

    @override_settings(HIPCHAT_ROOM_ID='873614')
    @override_settings(MICROSERVICE_TLD='staging.tangentmicroservices.com')
    def test_entry(self):

        c = Client()
        exit_payload = {  "user": "3",
                          "project_id": "3",
                          "project_task_id": "2",
                          "time": "October 1, 2015 at 09:34PM",
                          "entered_or_exited": "entered",
                          "auth_token" : "5e971505f6901ec76bfb53c990b2ab488d2d08e6"
                        }
        response = c.post('/ifttt/', exit_payload)

        assert response.status_code == 200, 'Expect 200OK'
        assert IncomingRequest.objects.count() == 1, 'IncomingRequest is saved'

    @override_settings(HIPCHAT_ROOM_ID='873614')
    @override_settings(MICROSERVICE_TLD='staging.tangentmicroservices.com')
    def test_exit(self):

        data ={"user": "3",
               "project_id": "3",
               "project_task_id": "2",
               "time": "October 1, 2015 at 02:00PM",
               "entered_or_exited": "entered",
               "auth_token" : "5e971505f6901ec76bfb53c990b2ab488d2d08e6"}

        IncomingRequest.objects.create(user=3, payload=json.dumps(data))

        c = Client()
        exit_payload = {  "user": "3",
                          "project_id": "3",
                          "project_task_id": "2",
                          "time": "October 1, 2015 at 04:31PM",
                          "entered_or_exited": "exited",
                          "auth_token" : "5e971505f6901ec76bfb53c990b2ab488d2d08e6"
                        }
        response = c.post('/ifttt/', exit_payload)

        assert response.status_code == 200, 'Expect 200OK'
        assert IncomingRequest.objects.count() == 2, 'IncomingRequest is saved'

    @override_settings(HIPCHAT_ROOM_ID='873614')
    @override_settings(MICROSERVICE_TLD='staging.tangentmicroservices.com')
    def test_place_entry(self):

        c = Client()
        exit_payload = {  "user": "3",
                          "project_id": "3",
                          "project_task_id": "2",
                          "time": "October 1, 2015 at 09:34PM",
                          "entered_or_exited": "entered",
                          "auth_token" : "5e971505f6901ec76bfb53c990b2ab488d2d08e6",
                          "place" : "Benoni Gym"
                        }
        response = c.post('/ifttt/', exit_payload)

        assert response.status_code == 200, 'Expect 200OK'
        assert IncomingRequest.objects.count() == 1, 'IncomingRequest is saved'

    @override_settings(HIPCHAT_ROOM_ID='873614')
    @override_settings(MICROSERVICE_TLD='staging.tangentmicroservices.com')
    def test_place_exit(self):

        data ={"user": "3",
               "project_id": "3",
               "project_task_id": "2",
               "place": "Benoni Gym",
               "time": "October 1, 2015 at 02:00PM",
               "entered_or_exited": "entered",
               "auth_token" : "5e971505f6901ec76bfb53c990b2ab488d2d08e6"}

        IncomingRequest.objects.create(user=3, payload=json.dumps(data))

        c = Client()
        exit_payload = {  "user": "3",
                          "project_id": "3",
                          "project_task_id": "2",
                          "place": "Benoni Gym",
                          "time": "October 1, 2015 at 04:31PM",
                          "entered_or_exited": "exited",
                          "auth_token" : "5e971505f6901ec76bfb53c990b2ab488d2d08e6"
                        }
        response = c.post('/ifttt/', exit_payload)

        assert response.status_code == 200, 'Expect 200OK'
        assert IncomingRequest.objects.count() == 2, 'IncomingRequest is saved'
