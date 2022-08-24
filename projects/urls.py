from django.urls import path
from . import views


urlpatterns = [
    path('', views.projects,name="projects"),
    path('project/<str:pk>/', views.project,name="project"), #in url path we are adding a str or no and calling it dynamically in our function
    path('create-project/', views.createProject,name="create-project"),
    path('update-project/<str:pk>/', views.updateProject,name="update-project"),
    path('delete-project/<str:pk>/', views.deleteProject,name="delete-project"),
]


