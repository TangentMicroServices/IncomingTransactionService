from django.test import TestCase, Client


class TestIFTTTViewSetPOST(TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_create_ifttt_webhook(self):
		'''
		POST /ifttt/
		'''

		c = Client()
		response = c.post('/ifttt/')
		
		assert response.status_code == 200, 'Expect 200OK'
