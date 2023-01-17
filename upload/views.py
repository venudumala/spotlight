from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import DataQualityCheck, DataSource, Database, Project, Upload
from .serializers import  DataQualityCheckSerializer, DataSourceSerializer, DatabaseSerializer, ProjectSerializer, UploadSerializer
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
import pandas as pd

class databaseView(APIView):
    def get(self,request):
        database=Database.objects.all()
        databaseserializer=DatabaseSerializer(database,many=True)
        return Response(databaseserializer.data)

    def post(self,request):
        database_serializer=DatabaseSerializer(data=request.data)
        if database_serializer.is_valid():
            database_serializer.save()
            return Response(database_serializer.data)
        
        else:
            return Response(database_serializer.errors)

class projectView(APIView):
    def get(self,request):
        project=Project.objects.all()
        projectserializer=ProjectSerializer(project,many=True)
        return Response(projectserializer.data)

    def post(self,request):
        project_serializer=ProjectSerializer(data=request.data)
        if project_serializer.is_valid():
            project_serializer.save()
            return Response(project_serializer.data)
        
        else:
            return Response(project_serializer.errors)

class DataSourceView(APIView):
    def get(self,request):
        data_source=DataSource.objects.all()
        datasourceserializer=DataSourceSerializer(data_source,many=True)
        return Response(datasourceserializer.data)

    def post(self,request):
        data_source_serializer=DataSourceSerializer(data=request.data)
        if data_source_serializer.is_valid():
            data_source_serializer.save()
            return Response(data_source_serializer.data)
        
        else:
            return Response(data_source_serializer.errors)

class uploadView(APIView):
    def get(self,request):
        uploads=Upload.objects.all()
        uploadserializer=UploadSerializer(uploads,many=True)
        return Response(uploadserializer.data)

    def post(self,request):
        insert_serializer=UploadSerializer(data=request.data)
        if insert_serializer.is_valid():
            insert_serializer.save()
            cursor = connection.cursor()
            ret = cursor.callproc("proc_schema_data",())
            cursor.close()
            return Response(insert_serializer.data)
        
        else:
            Response(insert_serializer.errors)

class UploadLayerView(APIView):
    def get(self,request,pk):
        get_uploaded_data=Upload.objects.get(pk=pk)
        get_uploaded_serializer=UploadSerializer(get_uploaded_data)
        return Response(get_uploaded_serializer.data)

    def put(self,request,pk):
        get_uploaded_data=Upload.objects.get(pk=pk)
        update_serializer=UploadSerializer(get_uploaded_data,data=request.data)
        if update_serializer.is_valid():
            update_serializer.save()
            return Response(update_serializer.data)
        else:
            return Response(update_serializer.errors)

class dataQualityCheck(APIView):
    def get(self,request):
        dataQuality=DataQualityCheck.objects.all()
        dataQualitySerializer=DataQualityCheckSerializer(dataQuality,many=True)
        return Response(dataQualitySerializer.data)

    def post(self,request):
        dataQuality_serializer=DataQualityCheckSerializer(data=request.data)
        if dataQuality_serializer.is_valid():
            dataQuality_serializer.save()
            return Response(dataQuality_serializer.data)
        
        else:
            Response(dataQuality_serializer.errors)

class getSchemaStructure(APIView):
    def get(self,request):
        cur = connection.cursor()
        sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'BRONZE_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"'"
        cur.execute(sql)
        records = cur.fetchall()
        return Response(records)

class getSchemaData(APIView):
    def get(self,request):
        cur = connection.cursor()
        string1=self.request.query_params.get('columns_name').replace("'",'')
        string2=string1.replace('[','')
        columns_name=string2.replace(']','')
        sql = "select "+ columns_name+"  from SPOTLIGHT.BRONZE_LAYER."+self.request.query_params.get('table_name')
        cur.execute(sql)
        records = cur.fetch_pandas_all()
        return Response(records)

class projectDataSourceData(APIView):
    def get(self,request):
        cur = connection.cursor()
        sql = "select pr.PROJECT_NAME, pr.USER_NAME, pr.DESCRIPTION,ds.DATA_SOURCE, ds.TABLE_RECORDS, ds.TOTAL_RECORDS from SPOTLIGHT.SPOTLIGHT.UPLOAD_PROJECT as pr inner join SPOTLIGHT.SPOTLIGHT.UPLOAD_DATASOURCE as ds on pr.id ="+self.request.query_params.get('project_id')
        cur.execute(sql)
        records = cur.fetch_pandas_all()
        return Response(records)

class silverGoldTransformView(APIView):
    def post(self,request):
        cursor = connection.cursor()
        SOURCE_TABLE_NAME1=self.request.query_params.get('SOURCE_TABLE_NAME1')
        SOURCE_TABLE_NAME2=self.request.query_params.get('SOURCE_TABLE_NAME2')
        TARGET_TABLE_NAME=self.request.query_params.get('TARGET_TABLE_NAME')
        JOIN_STATEMENT=self.request.query_params.get('JOIN_STATEMENT')
        FIRST_CLAUSE=self.request.query_params.get('FIRST_CLAUSE')
        SECOND_CLAUSE=self.request.query_params.get('SECOND_CLAUSE')
        string1=self.request.query_params.get('COLUMNS_NAME').replace("'",'')
        string2=string1.replace('[','')
        COLUMNS_NAME=string2.replace(']','')
        string3=self.request.query_params.get('COLUMNS_NAME').replace("'",'')
        string2=string1.replace('[','')
        INSERT_COLUMNS_NAME=string2.replace(']','')
        ret = cursor.callproc("proc_silver_gold_tansform",(SOURCE_TABLE_NAME1,SOURCE_TABLE_NAME2, TARGET_TABLE_NAME, INSERT_COLUMNS_NAME,COLUMNS_NAME, JOIN_STATEMENT, FIRST_CLAUSE, SECOND_CLAUSE))
        cursor.close()
        return Response("Success!!!")


class bronzeSilverTransform(APIView):
    def post(self,request):
        cur = connection.cursor()
        string1=self.request.query_params.get('columns_name').replace("'",'')
        string2=string1.replace('[','')
        columns_name=string2.replace(']','')
        sql ="Insert into SPOTLIGHT.SILVER_LAYER."+self.request.query_params.get('silver_table') +"("+columns_name+")"+ " select "+columns_name+" from SPOTLIGHT.BRONZE_LAYER."+self.request.query_params.get('bronze_table')
        cur.execute(sql)
        return Response("Success!!!")

class getSilverTable(APIView):
    def get(self,request):
        cur = connection.cursor()
        sql ="SELECT TABLE_NAME from information_schema.tables where TABLE_SCHEMA='SILVER_LAYER' "
        cur.execute(sql)
        records = cur.fetch_pandas_all()
        return Response(records)

class getSilverSchemaStructure(APIView):
    def get(self,request):
        cur = connection.cursor()
        sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'SILVER_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"'"
        cur.execute(sql)
        records = cur.fetchall()
        return Response(records)