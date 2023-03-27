import json
from rest_framework import serializers
from .models import DataQualityCheck, DataSource, DataType, Database, Project, Upload, layerDetails, workflowRules, filterSymbol, goldLayerData, workflowTransition
from django.db import models


class DatabaseSerializer(serializers.ModelSerializer):
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
        fields = "__all__"

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project_name=validated_data.get('project_name',instance.project_name)
        instance.description=validated_data.get('description',instance.description)
        instance.save()
        return instance

class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        # fields = ('id','project_id','data_source','table_records','total_records','final_data_file_generate','created_at','updated_at')
        fields ="__all__"

    def create(self, validated_data):
        return DataSource.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.project_id=validated_data.get('project_id',instance.project_id)
        instance.save()
        return instance
        
class projectDataSourceDataSerializer(serializers.ModelSerializer):
    data_source_list=DataSourceSerializer(many=True,read_only=True)

    class Meta:
        model = Project
        fields = "__all__"

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = "__all__"

    def create(self, validated_data):
        return Upload.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.dump_layer=validated_data.get('dump_layer',instance.dump_layer)
        instance.updated_at=validated_data.get('updated_at',instance.updated_at)
        instance.save()
        return instance

class DataQualityCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataQualityCheck
        fields = "__all__"

    def create(self, validated_data):
        return DataQualityCheck.objects.create(**validated_data)


class QueryLogsSerializer(serializers.Serializer):
    class Meta:
        model = DataQualityCheck
        fields = "__all__"

class DataTypeSerializer(serializers.Serializer):
    class Meta:
        model = DataType
        fields = "__all__"

    def create(self, validated_data):
        return DataType.objects.create(**validated_data)

class filterSymbolSerializer(serializers.Serializer):
    class Meta:
        model = filterSymbol
        fields = "__all__"

    def create(self, validated_data):
        return filterSymbol.objects.create(**validated_data)

class goldLayerDataSerializer(serializers.Serializer):
    class Meta:
        model = goldLayerData
        fields = "__all__"

    def create(self, validated_data):
        return goldLayerData.objects.create(**validated_data)

class WorkflowRulesSerializer(serializers.ModelSerializer):
    rules_data = serializers.SerializerMethodField()
    class Meta:
        model = workflowRules
        fields = '__all__'
        
    def get_rules_data(self, obj):
        return json.loads(obj.rules_data)
    
class WorkflowRulesDeserializer(serializers.ModelSerializer):  
    rules_data = serializers.JSONField()
    class Meta:
        model = workflowRules
        fields = '__all__'

    def create(self, validated_data):
        rules_data = validated_data.pop('rules_data')
        validated_data['rules_data'] = json.dumps(rules_data)
        return workflowRules.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.save()
        return instance
    
class layerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = layerDetails
        fields = "__all__"

    def create(self, validated_data):
        return layerDetails.objects.create(**validated_data)
    
class workflowTransitionSerializer(serializers.ModelSerializer):
    projectId=ProjectSerializer()
    ruleId=WorkflowRulesSerializer()
    layerId=layerDetailsSerializer()

    class Meta:
        model = workflowTransition
        fields = "__all__"

    def create(self, validated_data):
        return workflowTransition.objects.create(**validated_data)