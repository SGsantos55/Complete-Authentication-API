# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sg.serializers import UserRegistrationSerializer, UserLoginSerializer,UserProfileSerializer
from django.contrib.auth import authenticate
from .renderers import CustomJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
#Generate Tokens manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# santos inherited from apiview
class UserRegistrationView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg': 'Registration Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [CustomJSONRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg': 'Login success'}, status=status.HTTP_200_OK)
            else:
                return Response({'non_field_errors': ['Email or Password is not valid']}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class UserProfileView(APIView):
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
    
        return Response(serializer.data,status=status.HTTP_200_OK)