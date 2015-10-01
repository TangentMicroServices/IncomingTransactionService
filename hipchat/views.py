from django.shortcuts import render
from rest_framework import viewsets
from hipchat.serializers import *
from webhook.models import *
from rest_framework.response import Response
from rest_framework import status
import json
import requests
import datetime

class HipchatViewSet(viewsets.ViewSet):

    def getEmailAddress(self, hipchat_user_id ):
        """
        Returns the users email address from hipchat
        """
        payload = {"format":"json", "user_id": hipchat_user_id, "auth_token": "4efb6a0da2699a6c18be5623f40d08"}
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

        email = self.getEmailAddress("1956381")
        user = self.getUser("admin@tangentsolutions.co.za")

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
                    print("response.text")
                    return Response("OK", status=status.HTTP_201_CREATED)
                else:
                    return Response(response.text, status=status.HTTP_400_BAD_REQUEST)

            except requests.HTTPError as e:
                print ('HTTP ERROR %s occured' % e.code)
                print (e)

            except Exception as e:
                raise e

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
