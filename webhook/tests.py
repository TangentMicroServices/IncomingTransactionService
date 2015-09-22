from django.test import TestCase, Client
from webhook.datahelper import DataHelper
from webhook.models import IncomingRequest
import json
class WebHookTests(TestCase):

	def setUp(self):
		self.icr = DataHelper.incoming_request()
		self.icr2 = DataHelper.incoming_request()

	def tearDown(self):
		for icr in IncomingRequest.objects.all():
			icr.delete()

	def test_list_requests(self):
		c = Client()
		response = c.get('/webhook/')
		
		assert response.status_code == 200, 'Expect 200 OK'
		assert response.data['count'] == 2, 'Expect 2 results back'
		
	def test_create_request(self):

		payload = {'test': 'true'}
		data = {
			'source': 'http://google.com',
			'payload': json.dumps(payload)
		}
		c = Client()
		response = c.post('/webhook/', data)
		
		assert response.status_code == 201, 'Expect 201 CREATED'
		assert IncomingRequest.objects.count() == 3, 'Expect a webhook object to exist'



