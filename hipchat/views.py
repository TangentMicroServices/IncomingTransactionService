from django.shortcuts import render
from rest_framework import viewsets
from hipchat.serializers import *
from webhook.models import *
from rest_framework import status
import json
import requests
import datetime
from django.conf import settings

class HipchatViewSet(viewsets.ViewSet):

    def getEmailAddress(self, hipchat_user_id ):
        """
        Returns the users email address from hipchat
        """
        payload = {"format":"json", "user_id": hipchat_user_id, "auth_token": settings.HIPCHAT_AUTH_TOKEN}
        url = "https://api.hipchat.com/v1/users/show"

        try:
            response = requests.get(url, params=payload)
            if response.status_code == requests.codes.ok:
                email_address = json.loads(response.text)['user']['email']
                return email_address

        except Exception as e:
            raise e

    def getUser(self, email):
        try:
            headers = {
                'Authorization': 'Token 5e971505f6901ec76bfb53c990b2ab488d2d08e6',
                'Content-Type': 'application/json'
            }

            response = requests.get("http://userservice.staging.tangentmicroservices.com/api/v1/users/", headers=headers)

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
                    'Authorization': 'Token 5e971505f6901ec76bfb53c990b2ab488d2d08e6',
                    'Content-Type': 'application/json'
                }

                response = requests.post("http://hoursservice.staging.tangentmicroservices.com/api/v1/entry/", headers=headers, data=json.dumps(entry))

                if response.status_code == requests.codes.accepted:

                    hipchat_response = {"color": "green","message": "It's going to be sunny tomorrow! (yey)","notify": False,"message_format": "text"}
                    return Response(json.decode(hipchat_response), status=status.HTTP_200_OK)
                else:
                    return Response(response.text, status=status.HTTP_400_BAD_REQUEST)

            except requests.HTTPError as e:
                print ('HTTP ERROR %s occured' % e.code)
                print (e)

            except Exception as e:
                raise e

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
