from rest_framework import routers
from webhook import views

webhook_router = routers.DefaultRouter()
webhook_router.register(r'webhook', views.WebhookViewSet)