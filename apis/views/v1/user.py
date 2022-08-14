from apis.models import User
from apis.serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apis.views.v1 import Permission

class UserList(APIView, Permission):
    
    def get(self, request, *args, **kwargs):
        print(f'{request.user=}')
        # print(request.user.is_authenticated)
        
        user_context = []
        users = User.objects.all()
        
        for u in users:
            serializer = UserSerializer(u)
            user_context.append(serializer.data)
        
        return Response(user_context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView, Permission):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Response(f"User id {pk} is not found", status=status.HTTP_404_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        print(f'{request.user=}')
        User = self.get_object(kwargs['pk'])
        serializer = UserSerializer(User)
        
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        User = self.get_object(kwargs['pk'])
        serializer = UserSerializer(User, data=request.data)
       
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        User = self.get_object(kwargs['pk'])
        User.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)