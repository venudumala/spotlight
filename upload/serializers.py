from rest_framework import serializers
from .models import Upload

class UploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Upload
        fields=('id','url','file','file_name','file_type')