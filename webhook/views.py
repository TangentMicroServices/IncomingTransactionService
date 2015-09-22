from django.shortcuts import render

from rest_framework import viewsets, serializers
from rest_framework.response import Response
from webhook.models import IncomingRequest

class IncomingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingRequest

class WebhookViewSet(viewsets.ModelViewSet):
    queryset = IncomingRequest.objects.all()
    serializer_class = IncomingRequestSerializer
    