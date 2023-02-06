from rest_framework import serializers
from .models import DataQualityCheck, DataSource, DataType, Database, Project, Upload, filterSymbol, goldLayerData
from django.db import models


class DatabaseSerializer(serializers.Serializer):
    # id=serializers.IntegerField(read_only=True)
    # database_name=serializers.BooleanField(default=None)
    class Meta:
        model = Database
        fields = ('id','database_name')

    def create(self, validated_data):
        return Database.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.database_name=validated_data.get('database_name',instance.database_name)
        instance.save()
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id','project_name','user_name','description')

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project_name=validated_data.get('project_name',instance.project_name)
        instance.save()
        return instance

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = ('id','project_id','data_source','table_records','total_records','final_data_file_generate','created_at','updated_at')

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
    data_source=serializers.CharField()
    column_name=serializers.CharField()
    null_check=serializers.BooleanField()
    date_check=serializers.BooleanField()
    special_character_check=serializers.BooleanField()
    string_check=serializers.BooleanField()
    integer_check=serializers.BooleanField()

class DataQualityArrayCheckSerializer(serializers.Serializer):
    objects=DataQualityCheckSerializer(many=True)

    def create(self, validated_data):
        return DataQualityCheck.objects.create(**validated_data)


class QueryLogsSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    data_source=serializers.IntegerField()
    project_id=serializers.IntegerField()
    query_statement=serializers.IntegerField()
    target_table=serializers.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

class DataTypeSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    datatype=serializers.CharField()
    created_at=models.DateTimeField(auto_now_add=True)

    def create(self, validated_data):
        return DataType.objects.create(**validated_data)

class filterSymbolSerializer(serializers.Serializer):
     id=serializers.IntegerField(read_only=True)
     symbol=serializers.CharField(default=None)

     def create(self, validated_data):
        return filterSymbol.objects.create(**validated_data)

class goldLayerDataSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    project_name=models.CharField()
    data_source=models.CharField()
    records_inserted=models.CharField()
    final_data_file_generate=models.CharField()

    def create(self, validated_data):
        return goldLayerData.objects.create(**validated_data)