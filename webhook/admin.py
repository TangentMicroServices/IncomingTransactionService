from django.contrib import admin
from .models import IncomingRequest

class IncomingRequestAdmin(admin.ModelAdmin):
    # ...
    list_display = ('user', 'source', 'payload', 'created')


admin.site.register(IncomingRequest, IncomingRequestAdmin)

