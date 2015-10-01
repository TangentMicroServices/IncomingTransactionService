from rest_framework import serializers
from webhook.models import IncomingRequest


class IncomingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomingRequest
        fields = ('source', 'incoming_url', 'payload', 'user')
