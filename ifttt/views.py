from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

class IFTTTViewSet(viewsets.ViewSet):

    def create(self, request):

        return Response({'message': 'OK'}, status=200)
