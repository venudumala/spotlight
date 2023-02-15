from django.http import HttpResponse
from .models import DataQualityCheck, DataSource, DataType, Database, Project, QueryLogs, Upload, filterSymbol, goldLayerData
from .serializers import DataQualityCheckSerializer, DataSourceSerializer, DataTypeSerializer, DatabaseSerializer, ProjectSerializer, QueryLogsSerializer, UploadSerializer, filterSymbolSerializer, goldLayerDataSerializer, projectDataSourceDataSerializer
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
import pandas as pd
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

class databaseView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
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

class createTableView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        cursor = connection.cursor()
        DB_NAME="SPOTLIGHT"
        SCHEMA_NAME="SPOTLIGHT"
        TABLE_NAME=self.request.query_params.get('table_name')
        COLUMN_NAME=self.request.query_params.get('column_name')
        ret = cursor.callproc("proc_create_table",(DB_NAME,SCHEMA_NAME,TABLE_NAME,COLUMN_NAME))
        cursor.close()
        return Response("Success!!!")


class DataSourceView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data_source=DataSource.objects.all()
        datasourceserializer=DataSourceSerializer(data_source,many=True)
        return Response(datasourceserializer.data)

    def post(self,request,project_id,data_source):
        cursor = connection.cursor()
        ret = cursor.callproc("proc_create_datasource",(project_id,data_source))
        cursor.close()
        return Response("Success!!!")

class uploadView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        dataQuality=DataQualityCheck.objects.all()
        dataQualitySerializer=DataQualityCheckSerializer(dataQuality,many=True)
        return Response(dataQualitySerializer.data)

    def post(self,request):
        with connection.cursor() as cursor:
            fields = set()
            for item in request.data:
                fields.update(item.keys())
            fields = sorted(list(fields))
            for item in request.data:
                values = [f"'{item.get(field, 'NULL')}'" for field in fields]
                statement = f"INSERT INTO SPOTLIGHT.UPLOAD_DATAQUALITYCHECK ({','.join(fields)}) VALUES ({','.join(['%s'] * len(fields))});"
                cursor.execute(statement % tuple((values)))
        return Response("Success!!!")

class getSchemaStructure(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'BRONZE_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"' AND column_name NOT LIKE '%_AIRBYTE_%'"
        cur.execute(sql)
        records = cur.fetchall()
        return Response(records)

class getSchemaData(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql = "select pr.PROJECT_NAME, pr.USER_NAME, pr.DESCRIPTION,ds.DATA_SOURCE, ds.TABLE_RECORDS, ds.TOTAL_RECORDS,ds.FINAL_DATA_FILE_GENERATE from SPOTLIGHT.SPOTLIGHT.UPLOAD_PROJECT as pr inner join SPOTLIGHT.SPOTLIGHT.UPLOAD_DATASOURCE as ds on pr.id =ds.project_id where pr.id="+self.request.query_params.get('project_id')
        cur.execute(sql)
        records = cur.fetch_pandas_all().to_json(orient='records')
        return Response(records)


class bronzeSilverTransform(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        cur = connection.cursor()
        string1=self.request.query_params.get('columns_name').replace("'",'')
        string2=string1.replace('[','')
        columns_name=string2.replace(']','')
        sql ="Insert into SPOTLIGHT.SILVER_LAYER."+self.request.query_params.get('silver_table') +"("+columns_name+")"+ " select "+columns_name+" from SPOTLIGHT.BRONZE_LAYER."+self.request.query_params.get('bronze_table')
        cur.execute(sql)
        return Response("Success!!!")

class getSilverTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql ="SELECT TABLE_NAME from information_schema.tables where TABLE_SCHEMA='SILVER_LAYER' AND TABLE_NAME NOT LIKE '%TEMP_%'"
        cur.execute(sql)
        records = cur.fetch_pandas_all()
        return Response(records)

class getGoldTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,table_name):
        cur = connection.cursor()
        sql = "select *  from GOLD_LAYER."+table_name
        cur.execute(sql)
        records = cur.fetch_pandas_all().to_json(orient='records')
        cur.close()
        return HttpResponse(records)

class getSilverSchemaStructure(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'SILVER_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"' AND column_name NOT LIKE '%_AIRBYTE_%'"
        cur.execute(sql)
        records = cur.fetchall()
        return Response(records)

class silverGoldTransformView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        cursor = connection.cursor()
        TABLE_NAME=self.request.query_params.get('TABLE_NAME')
        COLUMNS_NAME=self.request.query_params.get('COLUMNS_NAME')
        FILTER_CONDITIONS=self.request.query_params.get('FILTER_CONDITIONS')
        ret = cursor.callproc("PROC_TEMP_SILVER_GOLD_TANSFORM",(TABLE_NAME,COLUMNS_NAME, FILTER_CONDITIONS))
        cursor.close()
        return Response("Success!!!")

class bronzeSilverInsert(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        cur = connection.cursor()
        SOURCE_TABLE_NAME1=self.request.query_params.get('SOURCE_TABLE_NAME1')
        SOURCE_TABLE_NAME2=self.request.query_params.get('SOURCE_TABLE_NAME2')
        TARGET_TABLE_NAME=self.request.query_params.get('TARGET_TABLE_NAME')
        JOIN_STATEMENT=self.request.query_params.get('JOIN_STATEMENT')
        FIRST_CLAUSE=self.request.query_params.get('FIRST_CLAUSE')
        SECOND_CLAUSE=self.request.query_params.get('SECOND_CLAUSE')
        COLUMNS_NAME=self.request.query_params.get('COLUMNS_NAME')
        sql="create or replace table SILVER_LAYER.TEMP_"+TARGET_TABLE_NAME+ " as select "+COLUMNS_NAME +" from "+SOURCE_TABLE_NAME1+" "+JOIN_STATEMENT +" "+SOURCE_TABLE_NAME2+ " on "+FIRST_CLAUSE+" = "+SECOND_CLAUSE
        print(sql)
        cur.execute(sql)
        cur.close()
        return Response("Success!!!")

class getSilverTableData(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,table_name):
        cur = connection.cursor()
        sql = "select *  from SILVER_LAYER."+table_name
        cur.execute(sql)
        records = cur.fetch_pandas_all()
        cur.close()
        return Response(records)

class QueryLogsView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        querylogs=QueryLogs.objects.all()
        querylogsserializer=QueryLogsSerializer(querylogs,many=True)
        return Response(querylogsserializer.data)

    def post(self,request):
        querylogs_serializer=ProjectSerializer(data=request.data)
        if querylogs_serializer.is_valid():
            querylogs_serializer.save()
            return Response(querylogs_serializer.data)
        
        else:
            return Response(querylogs_serializer.errors)

class getBronzeTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql ="Select UPPER(DATA_SOURCE) as DATA_SOURCE from SPOTLIGHT.SPOTLIGHT.UPLOAD_DATASOURCE where PROJECT_ID="+self.request.query_params.get('project_id')
        cur.execute(sql)
        records = cur.fetch_pandas_all()
        return Response(records)

class getBronzeSchemaStructure(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'BRONZE_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"' AND column_name NOT LIKE '%_AIRBYTE_%'"
        cur.execute(sql)
        records = cur.fetchall()
        return Response(records)

class getBronzeTableData(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,table_name):
        cur = connection.cursor()
        sql = "select *  from BRONZE_LAYER."+table_name
        cur.execute(sql)
        records = cur.fetch_pandas_all().to_json(orient='records')
        return HttpResponse(records)

class checkColumnSilverTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql = "select to_boolean(count(1)) from SPOTLIGHT.information_schema.columns where table_schema = 'SILVER_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"' and COLUMN_NAME='"+self.request.query_params.get('column_name')+"' AND column_name NOT LIKE '%_AIRBYTE_%';"
        cur.execute(sql)
        records = cur.fetchall()
        return Response(records)

class alterTableSilver(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql = "Alter TABLE SPOTLIGHT.SILVER_LAYER."+self.request.query_params.get('table_name')+" ADD "+self.request.query_params.get('column_name')+" "+self.request.query_params.get('data_type')
        print(sql)
        cur.execute(sql)
        records = cur.fetchall()
        return Response(records)

class dataTypeView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        database=DataType.objects.all()
        databaseserializer=DataTypeSerializer(database,many=True)
        return Response(databaseserializer.data)

    def post(self,request):
        database_serializer=DataTypeSerializer(data=request.data)
        if database_serializer.is_valid():
            database_serializer.save()
            return Response(database_serializer.data)
        
        else:
            return Response(database_serializer.errors)

class filterSymbolView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        filterSymbol=filterSymbol.objects.all()
        filterSymbolserializer=filterSymbolSerializer(filterSymbol,many=True)
        return Response(filterSymbolserializer.data)

    def post(self,request):
        filterSymbol_serializer=filterSymbolSerializer(data=request.data)
        if filterSymbol_serializer.is_valid():
            filterSymbol_serializer.save()
            return Response(filterSymbol_serializer.data)
        
        else:
            return Response(filterSymbol_serializer.errors)

class silverDataInsert(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        cur = connection.cursor()
        SILVER_TABLE_NAME=self.request.query_params.get('silver_table_name')
        TEMP_SILVER_TABLE_NAME="TEMP_"+SILVER_TABLE_NAME
        COLUMN_NAME=self.request.query_params.get('column_name')
        ret = cur.callproc("proc_check_dataquality",(SILVER_TABLE_NAME,TEMP_SILVER_TABLE_NAME,COLUMN_NAME))
        cur.close()
        return Response(ret)

class goldLayerDataView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cur = connection.cursor()
        sql = "select *  from SPOTLIGHT.UPLOAD_GOLDLAYERDATA"
        cur.execute(sql)
        records = cur.fetch_pandas_all().to_json(orient='records')
        cur.close()
        return HttpResponse(records)