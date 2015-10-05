from django.test import TestCase
from ifttt.helpers import hipchat_speak

class TestHipchatIntegration(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_post_to_hipchat(self):    	
    	res = hipchat_speak("Test Robot", "Testing 1, 2, 3")
    	import pdb;pdb.set_trace()