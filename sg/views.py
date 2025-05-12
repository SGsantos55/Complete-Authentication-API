# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sg.serializers import UserRegistrationSerializer

# Create your views here.
#santos inherited from apiview
class UserRegistrationView(APIView): 
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)#note data came from frontend will go in this request.data.
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({'msg':'Registration Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


