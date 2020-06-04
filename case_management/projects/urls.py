from django.urls import path

from .views import (
    TeamProjectListView,
    ClientProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    UpdateStatusView
)

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/<str:slug>/update', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/<str:slug>/projects/', TeamProjectListView.as_view(), name='team-projects'),
    path('<int:pk>/<str:slug>/projects/', ClientProjectListView.as_view(), name='client-projects'),
    path('<int:pk>/<str:slug>/details/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/<str:slug>/update-status/', UpdateStatusView.as_view(), name='project-status-update'),
]
