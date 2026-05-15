from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status
from  rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS, BasePermission, DjangoModelPermissions, IsAdminUser,DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly

# Create your views here.

# Class based view for handling tasks
class TaskUserWritePermission(BasePermission):
    message='Editing tasks is restricted to the author only.'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class Tasklist(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]
    queryset = Task.objects.all()
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly] # Allow read-only access for unauthenticated users, and full access for authenticated users with the appropriate model permissions.mane j j field e permission ase oi user er
        # permission_classes = [DjangoModelPermissions]

    permission_classes =[IsAuthenticatedOrReadOnly]    

    def get(self,request):
        tasks= Task.objects.all()
        serializer =TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self,request):
        serializer= TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskDetail(APIView):
    # def get_object(self,pk):
    #     try:
    #         return Task.objects.get(pk=pk)
    #     except Task.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    permission_classes=[TaskUserWritePermission]
    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self,request,pk):
        task=self.get_object(pk)
        serializer= TaskSerializer(task)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk):
        task=self.get_object(pk)
        serializer= TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        task=self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


