from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from ifttt.helpers import IfThisThenThatHelpers
from webhook.models import IncomingRequest
import requests
import logging, json

class IFTTTViewSet(viewsets.ViewSet):

    # 1. Capture incoming request (certain fields required)
    # 2. Check if it is entering / exiting an area
    # 3. save in db
    # 4. if exiting (find matching in db)
    # 5. calculate number of hours (integer with rounding)
    # 6. send to hours
    # 7. handle response


    def create(self, request):
        data = request.data

        icr = IncomingRequest()
        icr.payload = json.dumps(data) # store payload as string
        #Get the User
        if 'user' in request.data:
            icr.user = request.data['user']
        icr.source = 'IT'
        icr.incoming_url = request.META.get('HTTP_REFFERER')
        icr.save()

        if not data or data is None:
            return Response({'message': 'ERROR', 'description': 'No data is set'}, status=400)



        return Response({'message': 'OK', 'data': data}, status=200)

    def list(self, request):

        return Response({'message' : 'OK'}, status=200)
