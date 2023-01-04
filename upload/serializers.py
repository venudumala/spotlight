from rest_framework import serializers
from .models import Upload
from django.db import models

class UploadSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    record_id=serializers.IntegerField(read_only=True)
    file=serializers.FileField(default=None)
    file_name=serializers.CharField(default=None)
    file_type=serializers.CharField(default=None)
    upoload_layer=serializers.CharField(default=None)
    dump_layer=serializers.CharField(default=None)
    transformation_layer=serializers.CharField(default=None)
    records_inserted=serializers.CharField(default=None)
    valid_file_path=serializers.CharField(default=None)
    updated_at=serializers.CharField(default=None)

    def create(self, validated_data):
        return Upload.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.dump_layer=validated_data.get('dump_layer',instance.dump_layer)
        instance.updated_at=validated_data.get('updated_at',instance.updated_at)
        instance.save()
        return instance
