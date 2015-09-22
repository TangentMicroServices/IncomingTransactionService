from webhook.models import IncomingRequest

class DataHelper:

	@staticmethod 
	def incoming_request(source="ifttt", url="http://www.google.com", payload="{}"):

		request = IncomingRequest()
		request.source = source
		request.incoming_url = url
		request.payload = payload
		request.save()