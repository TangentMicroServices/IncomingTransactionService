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

    def create(self, request, format=None):

        incoming_request = {
            'source': 'hipchat',
            'incoming_url': request.META.get('HTTP_REFERER'),
            'payload': request.data.get('payload'),
            'user': 0
        }

        serializer = IncomingRequestSerializer(data=incoming_request)

        if serializer.is_valid():
            serializer.save()
            payload = incoming_request['payload']

            payload['comments'] = payload['description']
            payload['day'] = payload.get('day', datetime.datetime.now().date().strftime("%Y-%m-%d"))
            payload['status'] = payload.get('status', "Submitted" )
            payload['hours'] = payload.get('hours', 0)
            payload['user']: incoming_request.get('user'),


            entry = {
                
                'project_id': payload.get('project_id'),
                'project_task_id': payload.get('project_task_id'),
                'status': 'Submitted',
                'day':  ,
                'hours': ,
                'comments': payload.get('description', "")
            }

            try:
                headers = {
                    'Authorization': 'Token 5e971505f6901ec76bfb53c990b2ab488d2d08e6',
                    'Content-Type': 'application/json'
                }
                response = requests.post("http://hoursservice.staging.tangentmicroservices.com/api/v1/entry/", headers=headers, data=json.dumps(entry))

                if response.status_code == requests.codes.accepted:
                    return Response("OK", status=status.HTTP_201_CREATED)
            except Exception as e:
                raise e

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
