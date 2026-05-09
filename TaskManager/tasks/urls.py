from django.urls import path, include
from .views import TaskDetail, Tasklist

app_name = 'tasks'

urlpatterns = [
    path('tasks/', Tasklist.as_view(), name='task-list'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
]