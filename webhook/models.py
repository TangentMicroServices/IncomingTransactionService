from django.db import models

class IncomingRequest(models.Model):
    
    source = models.CharField(blank=True, null=True, max_length=100)
    incoming_url = models.URLField(blank=True, null=True)
    payload = models.TextField(default='{}')
    
