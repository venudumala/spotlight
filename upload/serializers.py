from rest_framework import serializers
from .models import Upload
from django.db import models

# class UploadSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model=Upload
#         fields=('id','record_id','url','file','file_name','file_type','upoload_layer','dump_layer','transformation_layer','records_inserted','created_at')

# class UploadLayerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Upload
#         fields=('id','record_id','dump_layer','transformation_layer','records_inserted')

#         def update(self, instance, validated_data):
#             return super().update(instance, validated_data)

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
        instance.record_id=validated_data.get('record_id',instance.record_id)
        instance.file=validated_data.get('file',instance.file)
        instance.file_name=validated_data.get('file_name',instance.file_name)
        instance.file_type=validated_data.get('file_type',instance.file_type)
        instance.upoload_layer=validated_data.get('upoload_layer',instance.upoload_layer)
        instance.dump_layer=validated_data.get('dump_layer',instance.dump_layer)
        instance.transformation_layer=validated_data.get('transformation_layer',instance.transformation_layer)
        instance.records_inserted=validated_data.get('records_inserted',instance.records_inserted)
        instance.valid_file_path=validated_data.get('valid_file_path',instance.valid_file_path)
        instance.updated_at=validated_data.get('updated_at',instance.updated_at)
        instance.save()
        return instance
