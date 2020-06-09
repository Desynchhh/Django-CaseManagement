from django.urls import path

from .views import (
    TeamProjectListView,
    ClientProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    UpdateStatusView,
    NoteCreateView,
    NoteDeleteView,
    ImageCreateView,
    ImageDeleteView
)

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/<str:slug>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/<str:slug>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk>/<str:slug>/projects/', TeamProjectListView.as_view(), name='team-projects'),
    path('c/projects/', ClientProjectListView.as_view(), name='client-projects'),
    path('<int:pk>/<str:slug>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/<str:slug>/update-status/', UpdateStatusView.as_view(), name='project-status-update'),
    path('<int:pid>/<str:slug>/note/create/', NoteCreateView.as_view(), name='note-create'),
    path('<int:pid>/<str:slug>/note/<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
    path('<int:pid>/<str:slug>/image/create/', ImageCreateView.as_view(), name='image-create'),
    path('<int:pid>/<str:slug>/image/<int:pk>/delete/', ImageDeleteView.as_view(), name='image-delete'),
]
