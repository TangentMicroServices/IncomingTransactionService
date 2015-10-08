"""
Integration tests. 
Run with: 

python manage.py test hipchat -p integration_test*

Be careful. These will make actual posts to actual services
"""
from django.test import TestCase, Client, override_settings
from ifttt.helpers import get_current_user, get_project, hipchat_speak
from django.conf import settings
from webhook.models import IncomingRequest
import json

token = '5e971505f6901ec76bfb53c990b2ab488d2d08e6'

class TestHipchatIntegration(TestCase):

	def test_post_to_hipchat(self):
		pass

class TestProjectServiceIntegration(TestCase):

	def test_get_project(self):
		pass

class TestUserServiceIntegration(TestCase):

	def test_get_user(self):
		pass		