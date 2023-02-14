from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from user_app.api.serializers import registrationSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST',])
def registration_view(request):
    if request.method=='POST':
        registration_serializer=registrationSerializer(data=request.data)
        data={}
        if registration_serializer.is_valid():
            account=registration_serializer.save()

            data['response']="Registration Successful !!"
            data['username']=account.username
            data['email']=account.email

            # token=Token.objects.get(user=account).key
            # data['token']=token
            refresh = RefreshToken.for_user(account)
            data['token']={
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                        }


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

