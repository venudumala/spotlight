from django.shortcuts import render
from rest_framework import viewsets
from .models import Upload
from .serializers import UploadSerializer

class UploadView(viewsets.ModelViewSet):
    queryset=Upload.objects.all()
    serializer_class=UploadSerializer


