from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Upload
from .serializers import  UploadSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# class UploadView(viewsets.ModelViewSet):
#     serializer_class=UploadSerializer
#     queryset=Upload.objects.all()

# class UploadLayerView(viewsets.ModelViewSet):
#     serializer_class=UploadLayerSerializer
#     queryset=Upload.objects.all()

class uploadView(APIView):
    def get(self,request):
        uploads=Upload.objects.all()
        uploadserializer=UploadSerializer(uploads,many=True)
        return Response(uploadserializer.data)

    def post(self,request):
        insert_serializer=UploadSerializer(data=request.data)
        if insert_serializer.is_valid():
            insert_serializer.save()
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


# @api_view(['GET','POST'])
# def uploaded_list(request):
#     if request.method=='GET':
#         uploads=Upload.objects.all()
#         uploadserializer=UploadSerializer(uploads,many=True)
#         return Response(uploadserializer.data)

#     if request.method=='POST':
#         insert_serializer=UploadSerializer(data=request.data)
#         if insert_serializer.is_valid():
#             insert_serializer.save()
#             return Response(insert_serializer.data)
        
#         else:
#             Response(insert_serializer.errors)

# @api_view(['GET','PUT'])
# def get_uploaded_list_id(request,pk):
#     if request.method=='GET':
#         get_uploaded_data=Upload.objects.get(pk=pk)
#         get_uploaded_serializer=UploadSerializer(get_uploaded_data)
#         return Response(get_uploaded_serializer.data)
    
#     if request.method=='PUT':
#         get_uploaded_data=Upload.objects.get(pk=pk)
#         update_serializer=UploadSerializer(get_uploaded_data,data=request.data)
#         if update_serializer.is_valid():
#             update_serializer.save()
#             return Response(update_serializer.data)
#         else:
#             return Response(update_serializer.errors)
