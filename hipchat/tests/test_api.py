from django.test import TestCase, Client, override_settings
from mock import patch
import responses, json
from urllib.parse import parse_qs

from hipchat.views import HipchatViewSet

class TestHipchatAPI(TestCase):

	def setUp(self):
		self.c = Client()

		self.hook_data = {
		    "event": 'room_message',
		    "item": {
		        "message": {
		            "date": '2015-01-20T22:45:06.662545+00:00',
		            "from": {
		                "id": 1661743,
		                "mention_name": 'Blinky',
		                "name": 'Blinky the Three Eyed Fish'
		            },
		            "id": '00a3eb7f-fac5-496a-8d64-a9050c712ca1',
		            "mentions": [],
		            "message": '/hours project:task 10 this is the comment',
		            "type": 'message'
		        },
		        "room": {
		            "id": 1147567,
		            "name": 'The Weather Channel'
		        }
		    },
		    "webhook_id": 578829
		}

	@responses.activate
	@override_settings(HOURSSERVICE_BASE_URI='http://hoursservice.example.com')
	@override_settings(USERSERVICE_BASE_URI='http://userservuce.example.com')
	@override_settings(HIPCHAT_ROOM_ID='873614')
	@patch.object(HipchatViewSet, 'getEntryFromPost')	
	def test_create(self, mock_get_entry_from_post):

		responses.add(responses.POST, 'http://hoursservice.example.com/entry/', status=201)
		responses.add(responses.POST, 'https://api.hipchat.com/v1/rooms/message')


		mock_get_entry_from_post.return_value = {
			"user": 1,
			"hours": 8,
			"project_id": 1,
			"project_task_id": 2,
			"comments": "testing testing 1, 2, 3"
		}
		
		response = self.c.post('/hipchat/', self.hook_data)

		assert len(responses.calls) == 2, 'Expect 2 calls'
		
		entry_request_data = json.loads(responses.calls[0].request.body)
		assert entry_request_data['project_id'] == 1
		assert entry_request_data['user'] == 1
		assert entry_request_data['hours'] == 8
		assert entry_request_data['project_task_id'] == 2
		assert entry_request_data['comments'] == "testing testing 1, 2, 3"
		assert entry_request_data['status'] == "Open"

		hipchat_request_data = responses.calls[1].request.body
		hipchat_request_data = parse_qs(hipchat_request_data)
		assert hipchat_request_data['message'][0] == '(successful) Entry successfully logged'
		assert hipchat_request_data['room_id'][0] == '873614'
		assert hipchat_request_data['from'][0] == 'Mr Robot'
		assert hipchat_request_data['message_format'][0] == 'text'

		assert response.status_code == 200, 'Expect 200 OK'







