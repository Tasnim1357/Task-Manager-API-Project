from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status
from  rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS, BasePermission, DjangoModelPermissions, IsAdminUser,DjangoModelPermissionsOrAnonReadOnly, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.

# Class based view for handling tasks
class TaskUserWritePermission(BasePermission):
    message='Editing tasks is restricted to the author only.'
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user

# Class based API view for handling tasks
# class Tasklist(APIView):
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAdminUser]
#     authentication_classes = [SessionAuthentication]
#     queryset = Task.objects.all()
#     # permission_classes = [DjangoModelPermissionsOrAnonReadOnly] # Allow read-only access for unauthenticated users, and full access for authenticated users with the appropriate model permissions.mane j j field e permission ase oi user er
#     # permission_classes = [DjangoModelPermissions]
#     permission_classes = [IsAuthenticated] # Allow read-only access for unauthenticated users, and full access for authenticated users.
#     # permission_classes =[IsAuthenticatedOrReadOnly] 


#     def get(self,request):
#         tasks= Task.objects.all()
#         serializer =TaskSerializer(tasks, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     def post(self,request):
#         serializer= TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CustomPaginationOne(PageNumberPagination):
    page_size=3

class CustomPaginationTwo(PageNumberPagination):

    page_size_query_param='page_size'

class CustomPaginationThree(PageNumberPagination):
    page_size=2
    page_size_query_param='page_size'           ## Allow clients to set the page size using a query parameter (e.g., ?page_size=5)
    max_page_size=5    

# Class based Generic APIview for handling tasks
class Tasklist(ListCreateAPIView): 
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    pagination_class = CustomPaginationThree
    


class TaskDetail(APIView):
    # def get_object(self,pk):
    #     try:
    #         return Task.objects.get(pk=pk)
    #     except Task.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    authentication_classes = [SessionAuthentication]
    permission_classes=[TaskUserWritePermission]
    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self,request,pk):
        task=self.get_object(pk)
        self.check_object_permissions(request, task) # Check if the user has custom permission to access this object
        serializer= TaskSerializer(task)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def patch(self,request,pk):
        task=self.get_object(pk)
        self.check_object_permissions(request, task)
        serializer= TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        
        task=self.get_object(pk)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


