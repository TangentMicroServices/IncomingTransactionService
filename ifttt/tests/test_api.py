from django.test import TestCase, Client
import responses


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
                                          "time": "08:12:00 12-09-2015",
                                          "entered_or_exited": "entered"})

        assert response.status_code == 200, 'Expect 200OK'

    def test_create_ifttt_exit(self):
        c = Client()
        response = c.post('/ifttt/', { 	"user": "4",
                                          "project_id": "2",
                                          "project_task_id": "23",
                                          "time": "17:12:00 12-09-2015",
                                          "entered_or_exited": "exited"})

        assert response.status_code == 200, 'Expect 200OK'

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
