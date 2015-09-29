from django.test import TestCase, Client
from webhook.models import IncomingRequest
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

        icr_entry = IncomingRequest.objects.get(user=4)

        assert icr_entry is not None, 'Expect the Entry Record to Exist'

    def test_create_ifttt_exit(self):
        c = Client()
        response = c.post('/ifttt/', { 	"user": "4",
                                          "project_id": "2",
                                          "project_task_id": "23",
                                          "time": "17:12:00 12-09-2015",
                                          "entered_or_exited": "exited"})

        assert response.status_code == 200, 'Expect 200OK'

        icr_entry = IncomingRequest.objects.get(user=4)

        assert icr_entry is not None, 'Expect the Exit Record to Exist'

    # def test_create_ifttt_enter_added(self):
        # Test that enter was added
        # now check we can find it in the database again
        # all_icr_in_database = IncomingRequest.objects.all()
        # self.assertEquals(len(all_icr_in_database), 1)


        # only_poll_in_database = all_polls_in_database[0]
        # self.assertEquals(only_poll_in_database, poll)
        #
        # # and check that it's saved its two attributes: question and pub_date
        # self.assertEquals(only_poll_in_database.question, "What's up?")
        # self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)

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
