from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('api/', views.apiOverview, name="api-overview"),
    path('api/task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
    path('api/task-list/', views.taskList, name="task-list"),
    path('api/task-create/', views.taskCreate, name="task-create"),
    path('api/task-update/<str:pk>/', views.taskUpdate, name="task-update"),
	path('api/task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
]