from rest_framework import serializers
from .models import DataQualityCheck, Upload
from django.db import models

class UploadSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    record_id=serializers.IntegerField(read_only=True)
    file=serializers.FileField(default=None)
    file_name=serializers.CharField(default=None)
    file_type=serializers.CharField(default=None)
    upoload_layer=serializers.BooleanField(default=True)
    dump_layer=serializers.BooleanField(default=False)
    transformation_layer=serializers.BooleanField(default=False)
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

class DataQualityCheckSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    data_source=serializers.CharField(default=None)
    column_name=serializers.CharField(default=None)
    null_check=serializers.BooleanField(default=False)
    date_check=serializers.BooleanField(default=False)
    special_character_check=serializers.BooleanField(default=False)
    string_check=serializers.BooleanField(default=False)
    integer_check=serializers.BooleanField(default=False)

    def create(self, validated_data):
        return DataQualityCheck.objects.create(**validated_data) 