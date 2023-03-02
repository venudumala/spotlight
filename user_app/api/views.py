from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from user_app.api.serializers import registrationSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
import uuid
from django.core.mail import send_mail
from django.conf import settings


@api_view(['POST',])
def registration_view(request):
    permission_classes = [AllowAny] 
    if request.method=='POST':
        registration_serializer=registrationSerializer(data=request.data)
        data={}
        if registration_serializer.is_valid():
            account=registration_serializer.save()

            data['response']="Registration Successful !!"
            data['username']=account.username
            data['email']=account.email
            refresh = RefreshToken.for_user(account)
            data['token']={
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }
            username=account.username
            password=request.data.get('password')
            recipient_list=list(account.email)
            subject='Welcome to Spotlight - Your Account Details'
            message=f'''Hi{username},
                            Congratulations! You have successfully signed up for Spotlight. 
                            We are delighted to have you as a member of our community. 
                            Your username and password have been created, and your account is now active.
                            Please find below your login details:
                                Username: {username}
                                Password: {password}
                            Best regards,
                            Spotlight Team.'''
            from_email=settings.EMAIL_HOST_USER
            send_mail(subject,message,from_email,recipient_list,fail_silently=False,)
            # return("Email sent successfully")
        else:
            data=registration_serializer.errors
        
        return Response(data)

@api_view(['POST',])
def logout_view(request):
    if request.method=='POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            payload = api_settings.JWT_PAYLOAD_HANDLER(user)
            token = api_settings.JWT_ENCODE_HANDLER(payload)
            return Response({'userId':user.id,'username':user.username,'email':user.email,'token': token})
        else:
            return Response({'error': 'Invalid Credentials'}, status=400)


