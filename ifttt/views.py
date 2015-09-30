from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from ifttt.helpers import IfThisThenThatHelpers
from webhook.models import IncomingRequest
import requests
import logging, json

class IFTTTViewSet(viewsets.ViewSet):

    # 1. Capture incoming request (certain fields required)
    # 2. save in db
    # 3. if exiting (find matching in db)
    # 4. calculate number of hours (integer with rounding)
    # 5. send to hours
    # 6. handle response


    def create(self, request):
        data = request.data

        #Save Record
        icr = IncomingRequest()
        icr.payload = json.dumps(data) # store payload as string
        #Get the User
        if 'user' in request.data:
            icr.user = data['user']
        icr.source = 'IT'
        icr.incoming_url = request.META.get('HTTP_REFFERER')
        icr.save()

        if not data or data is None:
            return Response({'message': 'ERROR', 'description': 'No data is set'}, status=400)

        # If exiting an area find corresponding entry time
        if data.get('entered_or_exited', None) == "exited":
            #if IncomingRequest.objects.filter(user=icr.user).order_by('-id')[1].exists():
            try:
                entered_icr = IncomingRequest.objects.filter(user=icr.user).order_by('-id')[1]
            except IndexError:
                return Response({'message': 'ERROR', 'description': 'could not find a matching enter entry'}, status=400)

            # get the entered time
            #import ipdb; ipdb.set_trace()
            entered_data = json.loads(entered_icr.payload)
            time_in = entered_data['time']
            time_out = data['time']
            # Validate in Model
            # Valdiate it is longer than 1 hour

            # Validate it is less than 24 hours
            # else:
            #     return Response({'message': 'ERROR', 'description': 'No corresponding entered time'}, status=400)

        return Response({'message': 'OK', 'data': data}, status=200)

    def list(self, request):

        return Response({'message' : 'OK'}, status=200)
