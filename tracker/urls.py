from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, TaskViewSet, dashboard_view,
    create_project_view, delete_project_view,
    create_task_view,update_task_view, delete_task_view
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"tasks", TaskViewSet)
urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('project/new/', create_project_view, name='create_project'),
    path('project/<int:project_id>/delete/', delete_project_view, name='delete_project'),
    path('project/<int:project_id>/task/new/', create_task_view, name='create_task'),
    path('task/<int:task_id>/edit/', update_task_view, name='update_task'),
    path('task/<int:task_id>/delete/', delete_task_view, name='delete_task'),
    path('api/', include(router.urls)),
]