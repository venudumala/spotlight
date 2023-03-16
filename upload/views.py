import datetime
import json
from django.http import HttpResponse
from .models import DataQualityCheck, DataSource, DataType, Database, Project, QueryLogs, Upload, filterSymbol, goldLayerData, Rules
from .serializers import DataQualityCheckSerializer, DataSourceSerializer, DataTypeSerializer, DatabaseSerializer, ProjectSerializer, QueryLogsSerializer, UploadSerializer, filterSymbolSerializer, goldLayerDataSerializer, projectDataSourceDataSerializer, RulesSerializer
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
import pandas as pd
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
import jwt
import uuid
#function to convert dict type exeception into string
def dict_str (x):
    msg=''
    for i in x.keys():
        msg = msg + f"{i}:{x[i][0]}"
    return msg

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
        try:
            user_id = request.user.id
            project=Project.objects.filter(user_id=user_id)
            projectserializer=ProjectSerializer(project,many=True)
            return Response(projectserializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            project_serializer=ProjectSerializer(data=request.data)
            if project_serializer.is_valid(raise_exception=True):
                project_serializer.save()
                auditLogs("0","0","Project Creation","Post Project Creation","Project Dashboard","Project","Success","Project has been created",request.user.username)
                return Response(project_serializer.data)
            # else:
            #     auditLogs("0","0","Project Creation","Post Project Creation","Project Dashboard","Project","Failure","Project has not been created",request.user.username)
            #     return Response(project_serializer.errors)
        except Exception as e:
            error_msg=project_serializer.errors
            msg=dict_str(error_msg) 
            auditLogs("0","0","Project Creation","Post Project Failed","-","Project","Failed",msg,request.user.username)
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        try:
            id=request.data.get('id')
            project=Project.objects.get(pk=id)
            project_serializer=ProjectSerializer(project, data=request.data)
            if project_serializer.is_valid(raise_exception=True):
                project_serializer.save()
                return Response(project_serializer.data)
            else:
                return Response(project_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        try:
            id=request.data.get('id')
            project=Project.objects.get(pk=id)
            project.delete()
            return Response("Project has been deleted successfully")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class createTableView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            cursor = connection.cursor()
            DB_NAME="SPOTLIGHT"
            SCHEMA_NAME="SPOTLIGHT"
            TABLE_NAME=self.request.query_params.get('table_name')
            COLUMN_NAME=self.request.query_params.get('column_name')
            ret = cursor.callproc("proc_create_table",(DB_NAME,SCHEMA_NAME,TABLE_NAME,COLUMN_NAME))
            cursor.close()
            project_id = request.session.get('project_id')
            # auditLogs(project_id,"0","Table Creation","Post Table Creation","",'{TABLE_NAME}',"Success","Project has been created",request.user.username,'current_timestamp()',"")
            return Response("Success!!!")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DataSourceView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            data_source=DataSource.objects.all()
            datasourceserializer=DataSourceSerializer(data_source,many=True)
            return Response(datasourceserializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,project_id,data_source):
        try:
            cursor = connection.cursor()
            cursor.callproc("proc_create_datasource",(project_id,data_source))
            cursor.close()
            project_ids = request.session.get('project_id')
            # auditLogs(project_ids,data_source,"Data Source Creation","Post Data Source Creation","","Data Source","Success","Data Source has been created",request.user.username,'current_timestamp()',"")
            return Response("Success!!!")
        except Exception as e:
            auditLogs(project_id,"","Data Source Creation","Post Data Source Creation","","Data Source","Failed",'error'+" "+str(e),request.user.username,'current_timestamp()',"")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class uploadView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            uploads=Upload.objects.all()
            uploadserializer=UploadSerializer(uploads,many=True)
            return Response(uploadserializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            insert_serializer=UploadSerializer(data=request.data)
            if insert_serializer.is_valid():
                insert_serializer.save()
                cursor = connection.cursor()
                ret = cursor.callproc("proc_schema_data",())
                cursor.close()
                project_ids = request.session.get('project_id')
                # auditLogs(project_ids,"","Data Source Creation","Post Data Source Creation","-","Data Source","Success","Data Source has been created",request.user.username,'current_timestamp()',"")
                return Response(insert_serializer.data)
            else:
                Response(insert_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UploadLayerView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            get_uploaded_data=Upload.objects.get(pk=pk)
            get_uploaded_serializer=UploadSerializer(get_uploaded_data)
            return Response(get_uploaded_serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk):
        try:
            get_uploaded_data=Upload.objects.get(pk=pk)
            update_serializer=UploadSerializer(get_uploaded_data,data=request.data)
            if update_serializer.is_valid():
                update_serializer.save()
                project_ids = request.session.get('project_id')
                #auditLogs(project_ids,"","File Uploaded Done","File Uploaded Creation Done","","File Uploaded","Success","Data Source has been created",request.user.username,'current_timestamp()',"")
                return Response(update_serializer.data)
            else:
                return Response(update_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class dataQualityCheck(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            dataQuality=DataQualityCheck.objects.all()
            dataQualitySerializer=DataQualityCheckSerializer(dataQuality,many=True)
            return Response(dataQualitySerializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            with connection.cursor() as cursor:
                fields = set()
                for item in request.data:
                    fields.update(item.keys())
                fields = sorted(list(fields))
                for item in request.data:
                    values = [f"'{item.get(field, 'NULL')}'" for field in fields]
                    statement = f"INSERT INTO SPOTLIGHT.UPLOAD_DATAQUALITYCHECK ({','.join(fields)}) VALUES ({','.join(['%s'] * len(fields))});"
                    cursor.execute(statement % tuple((values)))
            #auditLogs(request.session.get('project_id'),"","Data Quality Creation","Post Data Quality Creation","","UPLOAD_DATAQUALITYCHECK","Success","Data Source has been created",request.user.username,'current_timestamp()',"")
            return Response("Success!!!")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getSchemaStructure(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'BRONZE_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"' AND column_name NOT LIKE '%_AIRBYTE_%'"
            cur.execute(sql)
            records = cur.fetchall()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getSchemaData(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            string1=self.request.query_params.get('columns_name').replace("'",'')
            string2=string1.replace('[','')
            columns_name=string2.replace(']','')
            sql = "select "+ columns_name+"  from SPOTLIGHT.BRONZE_LAYER."+self.request.query_params.get('table_name')
            cur.execute(sql)
            records = cur.fetch_pandas_all()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class projectDataSourceData(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            request.session['project_id'] =self.request.query_params.get('project_id')
            cur = connection.cursor()
            sql = "select pr.PROJECT_NAME, pr.user_id, pr.DESCRIPTION,ds.DATA_SOURCE, ds.TABLE_RECORDS, ds.TOTAL_RECORDS,ds.FINAL_DATA_FILE_GENERATE from SPOTLIGHT.SPOTLIGHT.UPLOAD_PROJECT as pr inner join SPOTLIGHT.SPOTLIGHT.UPLOAD_DATASOURCE as ds on pr.id =ds.project_id where pr.id="+self.request.query_params.get('project_id')
            cur.execute(sql)
            records = cur.fetch_pandas_all().to_json(orient='records')
            sql1='select ID,PROJECT_NAME from UPLOAD_PROJECT where id='+self.request.query_params.get('project_id')
            cur.execute(sql1)
            project_values=cur.fetchall()
            data = [dict(zip([col[0] for col in cur.description], row)) for row in project_values]
            return Response({"records":records, "projectValue":data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class bronzeSilverTransform(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            cur = connection.cursor()
            string1=self.request.query_params.get('columns_name').replace("'",'')
            string2=string1.replace('[','')
            columns_name=string2.replace(']','')
            sql ="Insert into SPOTLIGHT.SILVER_LAYER."+self.request.query_params.get('silver_table') +"("+columns_name+")"+ " select "+columns_name+" from SPOTLIGHT.BRONZE_LAYER."+self.request.query_params.get('bronze_table')
            cur.execute(sql)
            #auditLogs(request.session.get('project_id'),"","Data Insertedd in Silver Table","bronzeSilverTransform","BRONZE to SILVER",str(self.request.query_params.get('silver_table')),"Success","Data Source has been created",request.user.username,'current_timestamp()',"")
            return Response("Success!!!")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getSilverTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql ="SELECT TABLE_NAME from information_schema.tables where TABLE_SCHEMA='SILVER_LAYER' AND TABLE_NAME NOT LIKE '%TEMP_%'"
            cur.execute(sql)
            records = cur.fetch_pandas_all()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getGoldTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,table_name):
        try:
            cur = connection.cursor()
            sql = "select *  from GOLD_LAYER."+table_name
            cur.execute(sql)
            records = cur.fetch_pandas_all().to_json(orient='records')
            cur.close()
            return HttpResponse(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getSilverSchemaStructure(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'SILVER_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"'"
            cur.execute(sql)
            records = cur.fetchall()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(records)

class getSilverSchemaColumn(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'SILVER_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"'"
            cur.execute(sql)
            records = cur.fetchall()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(records)

class silverGoldTransformView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            cursor = connection.cursor()
            TABLE_NAME=self.request.query_params.get('TABLE_NAME')
            COLUMNS_NAME=self.request.query_params.get('COLUMNS_NAME')
            FILTER_CONDITIONS=self.request.query_params.get('FILTER_CONDITIONS')
            ret = cursor.callproc("PROC_TEMP_SILVER_GOLD_TANSFORM",(TABLE_NAME,COLUMNS_NAME, FILTER_CONDITIONS))
            #auditLogs(request.session.get('project_id'),"","Data Inserted in Gold Table","silverGoldTransformView","SILVER to GOLD",str(self.request.query_params.get('TABLE_NAME')),"Success","Data has been added",request.user.username,'current_timestamp()',"")
            cursor.close()
            return Response("Success!!!")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class bronzeSilverInsert(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            cur = connection.cursor()
            SOURCE_TABLE_NAME1=self.request.query_params.get('SOURCE_TABLE_NAME1')
            SOURCE_TABLE_NAME2=self.request.query_params.get('SOURCE_TABLE_NAME2')
            TARGET_TABLE_NAME=self.request.query_params.get('TARGET_TABLE_NAME')
            JOIN_STATEMENT=self.request.query_params.get('JOIN_STATEMENT')
            FIRST_CLAUSE=self.request.query_params.get('FIRST_CLAUSE')
            SECOND_CLAUSE=self.request.query_params.get('SECOND_CLAUSE')
            COLUMNS_NAME=self.request.query_params.get('COLUMNS_NAME')
            sql="create or replace table SILVER_LAYER.TEMP_"+TARGET_TABLE_NAME+ " as select "+COLUMNS_NAME +" from "+SOURCE_TABLE_NAME1+" "+JOIN_STATEMENT +" "+SOURCE_TABLE_NAME2+ " on "+FIRST_CLAUSE+" = "+SECOND_CLAUSE
            #auditLogs(request.session.get('project_id'),"","Data Inserted in Gold Table","silverGoldTransformView","SILVER to GOLD",str(self.request.query_params.get('TABLE_NAME')),"Success","Data has been added",request.user.username,'current_timestamp()',"")
            cur.execute(sql)
            cur.close()
            return Response("Success!!!")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getSilverTableData(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,table_name):
        try:
            cur = connection.cursor()
            sql = "select *  from SILVER_LAYER."+table_name
            cur.execute(sql)
            records = cur.fetch_pandas_all()
            cur.close()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class QueryLogsView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            querylogs=QueryLogs.objects.all()
            querylogsserializer=QueryLogsSerializer(querylogs,many=True)
            return Response(querylogsserializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            querylogs_serializer=ProjectSerializer(data=request.data)
            if querylogs_serializer.is_valid():
                querylogs_serializer.save()
                return Response(querylogs_serializer.data)
            else:
                return Response(querylogs_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getBronzeTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql ="Select UPPER(DATA_SOURCE) as DATA_SOURCE from SPOTLIGHT.SPOTLIGHT.UPLOAD_DATASOURCE where PROJECT_ID="+self.request.query_params.get('project_id')
            cur.execute(sql)
            records = cur.fetch_pandas_all()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getBronzeSchemaStructure(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql = "select column_name  from SPOTLIGHT.information_schema.columns where table_schema = 'BRONZE_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"' AND column_name NOT LIKE '%_AIRBYTE_%'"
            cur.execute(sql)
            records = cur.fetchall()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class getBronzeTableData(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,table_name):
        try:
            cur = connection.cursor()
            # to get the columns name of a bronze table by excluding the airbyte columns
            sql=f"select column_name from spotlight.information_schema.columns where table_name='{table_name.upper()}' and column_name not like '_AIR%'"
            cur.execute(sql)
            columns=cur.fetchall()
            #loop to convert fetched data into a list of columns names
            columns_list=[]
            for col in columns:
                for value in col:
                    columns_list.append(value)
            #loop to convert the column list into a string as a valid sql statement
            columns_str= ','.join([col for col in columns_list])
            sql_table=f"select {columns_str} from spotlight.bronze_layer.{table_name}"
            cur.execute(sql_table)
            records = cur.fetch_pandas_all().to_json(orient='records')
            return HttpResponse(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class checkColumnSilverTable(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql = "select to_boolean(count(1)) from SPOTLIGHT.information_schema.columns where table_schema = 'SILVER_LAYER' and table_name ='"+self.request.query_params.get('table_name')+"' and COLUMN_NAME='"+self.request.query_params.get('column_name')+"' AND column_name NOT LIKE '%_AIRBYTE_%';"
            cur.execute(sql)
            records = cur.fetchall()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class alterTableSilver(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql = "Alter TABLE SPOTLIGHT.SILVER_LAYER."+self.request.query_params.get('table_name')+" ADD "+self.request.query_params.get('column_name')+" "+self.request.query_params.get('data_type')
            print(sql)
            cur.execute(sql)
            records = cur.fetchall()
            return Response(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class dataTypeView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            database=DataType.objects.all()
            databaseserializer=DataTypeSerializer(database,many=True)
            return Response(databaseserializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            database_serializer=DataTypeSerializer(data=request.data)
            if database_serializer.is_valid():
                database_serializer.save()
                return Response(database_serializer.data)
            
            else:
                return Response(database_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class filterSymbolView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            filterSymbol=filterSymbol.objects.all()
            filterSymbolserializer=filterSymbolSerializer(filterSymbol,many=True)
            return Response(filterSymbolserializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            filterSymbol_serializer=filterSymbolSerializer(data=request.data)
            if filterSymbol_serializer.is_valid():
                filterSymbol_serializer.save()
                return Response(filterSymbol_serializer.data)
            else:
                return Response(filterSymbol_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class silverDataInsert(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            cur = connection.cursor()
            SILVER_TABLE_NAME=self.request.query_params.get('silver_table_name')
            TEMP_SILVER_TABLE_NAME="TEMP_"+SILVER_TABLE_NAME
            COLUMN_NAME=self.request.query_params.get('column_name')
            ret = cur.callproc("proc_check_dataquality",(SILVER_TABLE_NAME,TEMP_SILVER_TABLE_NAME,COLUMN_NAME))
            cur.close()
            return Response(ret)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class goldLayerDataView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            sql = "select * from SPOTLIGHT.INFORMATION_SCHEMA.TABLES where TABLE_CATALOG = 'SPOTLIGHT' AND TABLE_SCHEMA = 'GOLD_LAYER'"
            cur.execute(sql)
            records = cur.fetch_pandas_all().to_json(orient='records')
            cur.close()
            return HttpResponse(records)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class projectTempView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
           token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
           jwt_payload = jwt.decode(token, verify=False)
           guid = request.user.guid
           token = request.GET.get('guid')
           user_id = request.user.id
           user_name = request.user.username
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': f'Hello, {jwt_payload}! Your guid ID is {guid}'})
    
# CFunction to log the message 
def auditLogs(PROJECT_ID,DATASOURCE,OPERATION,CALLED_FUNCTION_NAME,LAYER,TABLE_NAME,STATUS,MESSAGE,LOGINUSER):
    try:
    #define cursor 
        cursor = connection.cursor()
        guid=uuid.uuid4()
        created_at=datetime.datetime.now()
        statement =  f"insert into spotlight.UPLOAD_AUDIT(UID,PROJECT_ID,DATASOURCE,OPERATION,CALLED_FUNCTION_NAME,LAYER,TABLE_NAME,STATUS,MESSAGE,CREATED_BY,CREATED_AT) values('{guid}','{PROJECT_ID}','{DATASOURCE}','{OPERATION}','{CALLED_FUNCTION_NAME}','{LAYER}','{TABLE_NAME}','{STATUS}','{MESSAGE}','{LOGINUSER}','{created_at}')"
        print(statement)
        cursor.execute(statement)
        cursor.close()
    except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# Edited after this
# class goldDataPreview(APIView):
#     authentication_classes = [JSONWebTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self,request):
#         try:
#             query_str=self.request.query_params.get('query_str')
#             cur = connection.cursor()
#             sql = query_str + " lIMIT 15"
#             cur.execute(sql)
#             records = cur.fetch_pandas_all().to_json(orient='records')
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(records)

class goldDataPreview(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            case_stmt=self.request.query_params.get('case_stmt')
            filter_stmt=self.request.query_params.get('filter_stmt')
            order_by_stmt=self.request.query_params.get('order_by_stmt')
            group_by_stmt=self.request.query_params.get('group_by_stmt')
            custom_stmt=self.request.query_params.get('custom_stmt')
            tbl_name = self.request.query_params.get('tbl_name')
            col_list = self.request.query_params.get('col_list')
            query_str = "SELECT " + col_list 
            if(case_stmt):
                query_str += " , " + case_stmt
            if(custom_stmt):
                query_str += " , " + custom_stmt 
            query_str += " FROM " + tbl_name
            if(filter_stmt):
                query_str += "  " + filter_stmt
            if(group_by_stmt):
                query_str += " " + group_by_stmt
            if(order_by_stmt):
                query_str += " "+ order_by_stmt
            sql = query_str + " LIMIT 30"
            cur = connection.cursor()
            cur.execute(sql)
            records = cur.fetch_pandas_all().to_json(orient='records')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(records)  
        

class goldDataCreate(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            gold_table_name=self.request.query_params.get('gold_table_name')
            case_stmt=self.request.query_params.get('case_stmt')
            filter_stmt=self.request.query_params.get('filter_stmt')
            order_by_stmt=self.request.query_params.get('order_by_stmt')
            group_by_stmt=self.request.query_params.get('group_by_stmt')
            custom_stmt=self.request.query_params.get('custom_stmt')
            tbl_name = self.request.query_params.get('tbl_name')
            col_list = self.request.query_params.get('col_list')
            query_str = "SELECT " + col_list 
            if(case_stmt):
                query_str += " , " + case_stmt
            if(custom_stmt):
                query_str += " , " + custom_stmt
            query_str += " FROM " + tbl_name
            if(filter_stmt):
                query_str += " " + filter_stmt
            if(group_by_stmt):
                query_str += " " + group_by_stmt
            if(order_by_stmt):
                query_str += " "+ order_by_stmt
            sql = "CREATE OR REPLACE TABLE GOLD_LAYER."+ gold_table_name +" AS (" + query_str + ")"
            cur.execute(sql)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response("Success !!!!")
    
class goldDataInsert(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            cur = connection.cursor()
            gold_table_name=self.request.query_params.get('gold_table_name')
            case_stmt=self.request.query_params.get('case_stmt')
            filter_stmt=self.request.query_params.get('filter_stmt')
            order_by_stmt=self.request.query_params.get('order_by_stmt')
            group_by_stmt=self.request.query_params.get('group_by_stmt')
            custom_stmt=self.request.query_params.get('custom_stmt')
            tbl_name = self.request.query_params.get('tbl_name')
            col_list = self.request.query_params.get('col_list')
            query_str = "SELECT " + col_list 
            if(case_stmt):
                query_str += " , " + case_stmt
            if(custom_stmt):
                query_str += " , " + custom_stmt
            query_str += " FROM " + tbl_name
            if(filter_stmt):
                query_str += " " + filter_stmt
            if(group_by_stmt):
                query_str += " " + group_by_stmt
            if(order_by_stmt):
                query_str += " "+ order_by_stmt
            sql = "Insert into GOLD_LAYER."+ gold_table_name+" ("+col_list +")  (" + query_str + ")"
            cur.execute(sql)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response("Success !!!!")
    

class rulesView(APIView):
    def get(self, request):
        try:
            project_id = request.data.get('project_id')
            data = Rules.objects.filter(project_id=project_id)
            databaseserializer=RulesSerializer(data,many=True)
            return JsonResponse(databaseserializer.data, safe=False)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        try:
            database_serializer=RulesSerializer(data=request.data)
            if database_serializer.is_valid():
                database_serializer.save()
                return Response(database_serializer.data)
            else:
                return Response(database_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
        try:
            ruleId=request.data.get('rule_id')
            rules=Rules.objects.get(pk=ruleId)
            rules_serializer=RulesSerializer(rules, data=request.data)
            if rules_serializer.is_valid():
                rules_serializer.save()
                return Response(rules_serializer.data)
            else:
                return Response(rules_serializer.errors)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        try:
            ruleId=request.data.get('rule_id')
            rules=Rules.objects.get(pk=ruleId)
            rules.delete()
            return Response("Rule has been deleted successfully")
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
