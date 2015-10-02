from django.db import models
import json

IFTTT = 'IT'
HIPCHAT = 'HC'
UNKNOWN = 'UK'
SOURCE_CHOICES = (
    (IFTTT, 'If This Then That'),
    (HIPCHAT, 'Hipchat'),
    (UNKNOWN, 'Unknown'),
)

class IncomingRequest(models.Model):

    def __str__(self):
        return self.payload

    last_edited = models.DateTimeField(auto_now=True,db_index=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)    
    source = models.CharField(max_length=2, choices=SOURCE_CHOICES, default=UNKNOWN)
    incoming_url = models.URLField(blank=True, null=True)
    payload = models.TextField(default='{}')
    user = models.IntegerField(default='-1')

    @property
    def payload_as_json(self):
        return json.loads(self.payload)
