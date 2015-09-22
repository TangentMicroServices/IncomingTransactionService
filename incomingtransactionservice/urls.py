from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from webhook.urls import webhook_router

from webhook.urls import webhook_router

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(webhook_router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

