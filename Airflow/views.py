from django.shortcuts import render
import requests
import json
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

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
        return Response({"dag_run_id":dag_id})
