from django.urls import path, include
from .views import TaskDetail, TaskList2, TaskViewSet, Tasklist, UserWithTasksList
from rest_framework.routers import DefaultRouter

app_name = 'tasks'
router = DefaultRouter()
router.register('tasks-viewset', TaskViewSet, basename='task')
urlpatterns = [
    path('tasks', Tasklist.as_view(), name='task-list'),
    path('tasks/<int:pk>', TaskDetail.as_view(), name='task-detail'),
    path('users-with-tasks', UserWithTasksList.as_view(), name='user-with-tasks'),
    path('tasks2', TaskList2.as_view(), name='task-list2'),
    path('', include(router.urls)), # For viewset testing
]