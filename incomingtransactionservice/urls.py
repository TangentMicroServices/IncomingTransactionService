from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from webhook import views as webhook_views
from ifttt import views as ifttt_views
from hipchat import views as hipchat_views

router = routers.DefaultRouter()
router.register(r'webhook', webhook_views.WebhookViewSet)
router.register(r'ifttt', ifttt_views.IFTTTViewSet, base_name='ifttt')
router.register(r'hipchat', hipchat_views.HipchatViewSet, base_name='hipchat')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
