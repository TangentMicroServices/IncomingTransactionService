from django.test import TestCase, Client, override_settings
from mock import patch
from hipchat.helpers import parse_hipchat_message, get_user
import responses, json, unittest


from hipchat.views import HipchatViewSet

class TestHelpers(TestCase):

	def setUp(self):
		pass

	@patch.object(HipchatViewSet, 'getEmailAddress')
	@patch.object(HipchatViewSet, 'getUser')
	def test_get_entry_from_post(self, mock_getUser, mock_getEmailAddress):

		mock_getEmailAddress.return_value = "joe@soap.com"
		mock_getUser.return_value = {"id": 1}

		data = {
			"item": {
				"message": {
					"message": "/hours 23:2 10 Did some stuff",
					"from": {
						"id": 123
					}
				}
			}
		}

		viewset = HipchatViewSet()
		entry = viewset.getEntryFromPost(data)

		mock_getEmailAddress.assert_called_with('123')
		mock_getUser.assert_called_with("joe@soap.com")

		# {'project_id': '23', 'comments': 'Did some stuff', 'project_task_id': '2', 'user': 1, 'hours': '10'}
		
		assert entry['project_id'] == '23'
		assert entry['project_task_id'] == '2'
		assert entry['hours'] == '10'
		assert entry['user'] == 1
		assert entry['comments'] == "Did some stuff"

	@override_settings(HIPCHAT_BASE_URI='https://api.hipchat.com')
	@responses.activate
	def test_get_email_address(self):

		responses.add(responses.GET, 'https://api.hipchat.com/users/show',
						body='{"user": {"email":"joe@soap.com"}}')

		hipchat_user_id = '123'
		viewset = HipchatViewSet()
		email = viewset.getEmailAddress(hipchat_user_id)

		assert email == "joe@soap.com"

	@responses.activate
	@override_settings(USERSERVICE_BASE_URI='http://userserivce.tangentmicroservices.com')
	def test_get_user(self):

		responses.add(responses.GET, 'http://userserivce.tangentmicroservices.com/api/v1/users/',
						body='[{"email":"joe@soap.com"}]')

		viewset = HipchatViewSet()
		user = viewset.getUser("joe@soap.com")
		
		assert user['email'] == 'joe@soap.com'

	@responses.activate
	@override_settings(USERSERVICE_BASE_URI='http://userserivce.tangentmicroservices.com')
	def test_get_user(self):

		responses.add(responses.GET, 'http://userserivce.tangentmicroservices.com/api/v1/users/',
						body='[]')

		viewset = HipchatViewSet()
		user = viewset.getUser("joe@soap.com")
		
		assert user is None



	"""
	Refactored versions:
	"""
	@unittest.skip("Not yet implemented")
	def test_parse_hipchat_message(self):

		incoming_message = "/hours 23:2 10 Did some stuff"
		response = parse_hipchat_message(incoming_message)

		assert response['project_id'] == 23
		assert response['project_task_id'] == 2
		assert response['hours'] == 10
		assert response['comments'] == "Did some stuff"
		





