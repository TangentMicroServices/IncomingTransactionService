from django.shortcuts import render
from rest_framework import viewsets
from hipchat.serializers import *
from webhook.models import *
from rest_framework import status
from rest_framework.response import Response
import json
import requests
import datetime
from django.conf import settings

## refactor this to global package:
from ifttt.helpers import hipchat_speak

class HipchatViewSet(viewsets.ViewSet):

    def getEmailAddress(self, hipchat_user_id ):
        """
        Returns the users email address from hipchat
        """
        payload = {"format":"json", "user_id": hipchat_user_id, "auth_token": settings.HIPCHAT_AUTH_TOKEN}

        try:
            response = requests.get(settings.HIPCHAT_BASE_URI + "/users/show", params=payload)
            if response.status_code == requests.codes.ok:
                email_address = json.loads(response.text)['user']['email']
                return email_address

        except Exception as e:
            raise e

    def getUser(self, email):
        try:
            headers = {
                'Authorization': 'Token ' + settings.TANGENT_ADMIN_TOKEN,
                'Content-Type': 'application/json'
            }

            response = requests.get( settings.USERSERVICE_BASE_URI + "/api/v1/users/", headers=headers)

            print (settings.TANGENT_ADMIN_TOKEN)
            print (settings.USERSERVICE_BASE_URI)

            if response.status_code == requests.codes.ok:
                users = json.loads(response.text)
                for each_user in users:
                    if each_user['email'] == email:
                        return each_user
                return None

        except Exception as e:
            raise e

    def getEntryFromPost(self, data):
        """
        Returns the entry details from the hipchat slash command
        """

        slash_command = str(data['item']['message']['message'])
        slash_command_split = str.split(slash_command, ' ')
        comments = " ".join(slash_command_split[3: len(slash_command_split)])
        entry = {
            'project_id': str.split(slash_command_split[1], ":")[0],
            'project_task_id': str.split(slash_command_split[1], ":")[1],
            'hours': slash_command_split[2],
            'comments': comments,
        }

        # email = self.getEmailAddress("1956381")
        email = self.getEmailAddress(str(data['item']['message']['from']['id']))
        user = self.getUser(email)

        if user is not None:
            entry['user'] = user['id']

        return entry

    def create(self, request, format=None):
        """
        * Save IncomingRequest 
        * Get user from UserService 
        * Get project info from ProjectService
        * Post result back to HipChat
        """

        entry = self.getEntryFromPost(request.data)

        incoming_request = {
            'source': 'HC',
            'incoming_url': request.META.get('HTTP_REFERER'),
            'payload': request.data,
            'user': entry['user']
        }

        serializer = IncomingRequestSerializer(data=incoming_request)

        if serializer.is_valid():
            serializer.save()

            entry['day'] = datetime.datetime.now().date().strftime("%Y-%m-%d")
            entry['status'] = "Open"

            try:
                headers = {
                    'Authorization': 'Token ' + settings.TANGENT_ADMIN_TOKEN,
                    'Content-Type': 'application/json'
                }

                response = requests.post( settings.HOURSSERVICE_BASE_URI +"/entry/", headers=headers, data=json.dumps(entry))
                # print response.status_code
                if response.status_code == requests.codes.created:
                    message = "Entry successfully logged (rockon)"
                    hipchat_speak(message)
                    return Response(json.dumps({"color": "green","message": message,"notify": False,"message_format": "text"}), status=status.HTTP_200_OK)
                else:
                    message = "Entry could not be logged (sadpanda)"
                    hipchat_speak(message)
                    return Response(json.dumps({"color": "red","message": message,"notify": False,"message_format": "text"}), status=status.HTTP_400_BAD_REQUEST)

            except requests.HTTPError as e:
                # print ('HTTP ERROR %s occured' % e.code)
                raise e

            except Exception as e:
                raise e
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
