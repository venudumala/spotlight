from rest_framework import serializers
from .models import DataQualityCheck, DataSource, Database, Project, Upload
from django.db import models


class DatabaseSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    database_name=serializers.BooleanField(default=None)

    def create(self, validated_data):
        return Database.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.database_name=validated_data.get('database_name',instance.database_name)
        instance.save()
        return instance


class ProjectSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    project_id=serializers.IntegerField(read_only=True)
    project_name=serializers.CharField(default=None)
    user_name=serializers.CharField(default=None)
    description=serializers.CharField(default=None)

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project_name=validated_data.get('project_name',instance.project_name)
        instance.save()
        return instance

class DataSourceSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    project_id=serializers.IntegerField(default=None)
    data_source=serializers.CharField(default=None)
    table_records=serializers.IntegerField(default=None)
    total_records=serializers.IntegerField(default=None)
    final_data_file_generate=serializers.CharField(default=None)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def create(self, validated_data):
        return DataSource.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project_id=validated_data.get('project_id',instance.project_id)
        instance.save()
        return instance

class UploadSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    record_id=serializers.IntegerField(read_only=True)
    project_name=serializers.CharField(default=None)
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


class QueryLogsSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    data_source=serializers.IntegerField()
    project_name=serializers.IntegerField()
    query_statement=serializers.IntegerField()
    target_table=serializers.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
