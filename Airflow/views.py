from django.shortcuts import render
import requests
import json
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from rest_framework import status
# Create your views here.

def auditLogs(PROJECT_ID,DATASOURCE,OPERATION,CALLED_FUNCTION_NAME,LAYER,TABLE_NAME,STATUS,MESSAGE,LOGINUSER,CREATED_AT,GUID):
    try:
    #define cursor 
        cursor = connection.cursor()
        statement =  f"insert into UPLOAD_AUDIT(PROJECT_ID,DATASOURCE,OPERATION,CALLED_FUNCTION_NAME,LAYER,TABLE_NAME,STATUS,MESSAGE,CREATED_BY,UID,CREATED_AT) values('{PROJECT_ID}','{DATASOURCE}','{OPERATION}','{CALLED_FUNCTION_NAME}','{LAYER}','{TABLE_NAME}','{STATUS}','{MESSAGE}','{LOGINUSER}','{GUID}',{CREATED_AT})"
        print(statement)
        cursor.execute(statement)
        cursor.close()
    except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class sourceTestMssql(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data=request.data.get('conf')
        payload=json.dumps({'conf':data})
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.post(url='http://20.253.0.141:8080/api/v1/dags/source_test/dagRuns',headers=headers, data=payload)
        api_js=api.json()
        dag_id=api_js['dag_run_id']
        tablename=data['dbname']
        auditLogs(request.session.get('project_id'),"","Data loading started","Source to bonze","source to bronze",tablename,"Success","Data has been added",request.user.username,'current_timestamp()',"")
        return Response({"dag_run_id":dag_id})

class SourceStatus(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        dag_id = request.data.get('dag_run_id')
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.get(url=f'http://20.253.0.141:8080/api/v1/dags/source_test/dagRuns/{dag_id}/taskInstances/testing_source/xcomEntries/status'
        ,headers=headers)
        api_json=api.json()
        status=api_json['value']
        return Response({"status":status})

class SourceFailMsg(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        dag_id = request.data.get('dag_run_id')
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.get(url=f'http://20.253.0.141:8080/api/v1/dags/source_test/dagRuns/{dag_id}/taskInstances/testing_source/xcomEntries/failed_msg'
        ,headers=headers)
        api_json=api.json()
        failed_msg=api_json['value']
        return Response({"value":failed_msg})


class getSourceID(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        dag_id = request.data.get('dag_run_id')
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.get(url=f'http://20.253.0.141:8080/api/v1/dags/source_test/dagRuns/{dag_id}/taskInstances/createsource/xcomEntries/sourceId'
        ,headers=headers)
        api_json=api.json()
        sourceid=api_json['value']
        return Response({"value":sourceid})

class getConnId(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        dag_id = request.data.get('dag_run_id')
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.get(url=f'http://20.253.0.141:8080/api/v1/dags/source_test/dagRuns/{dag_id}/taskInstances/create_connection/xcomEntries/return_value'
        ,headers=headers)
        api_json=api.json()
        connid=api_json['value']
        return Response({"value":connid})
    
class getTablesList(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        dag_id = request.data.get('dag_run_id')
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.get(url=f'http://20.253.0.141:8080/api/v1/dags/source_test/dagRuns/{dag_id}/taskInstances/discover_schema/xcomEntries/tablelist'
        ,headers=headers)
        api_json=api.json()
        tablelist=api_json['value']
        return Response({"value":tablelist})

class syncConnection(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        data=request.data.get('conf')
        payload=json.dumps({'conf':data})
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.post(url='http://20.253.0.141:8080/api/v1/dags/sync_connection/dagRuns',headers=headers, data=payload)
        return Response("Data Loading started successfully")

class syncCsvFile(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        data=request.data.get('conf')
        payload=json.dumps({'conf':data})
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.post(url='http://20.253.0.141:8080/api/v1/dags/csv_file_dag/dagRuns',headers=headers, data=payload)
        return Response("Data Loading started successfully")

class syncAzureBlob(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated] 
    def post(self, request):
        data=request.data.get('conf')
        payload=json.dumps({'conf':data})
        headers = {'Content-Type': 'application/json','Authorization': 'Basic YWRtaW46YWRtaW4='}
        api=requests.post(url='http://20.253.0.141:8080/api/v1/dags/Azure_Blob_Storage_Dag/dagRuns',headers=headers, data=payload)
        return Response("Data Loading started successfully")
