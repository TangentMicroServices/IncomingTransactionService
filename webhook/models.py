from django.db import models

class IncomingRequest(models.Model):
    last_edited = models.DateTimeField(auto_now=True,db_index=True)
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    source = models.CharField(blank=True, null=True, max_length=100)
    incoming_url = models.URLField(blank=True, null=True)
    payload = models.TextField(default='{}')
    user = models.IntegerField()
