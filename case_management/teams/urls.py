from django.urls import path
from .views import (
    # TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamProjectListView,
    TeamProjectRequestListView
)

urlpatterns = [
    # path('<int:pk>/<str:slug>/', TeamListView.as_view(), name='team-index'),
    path('<int:pk>/<str:slug>/', TeamDetailView.as_view(), name='team-detail'),
    path('<int:pk>/<str:slug>/update/', TeamUpdateView.as_view(), name='team-update'),
    path('create/', TeamCreateView.as_view(), name='team-create'),
    path('<int:pk>/<str:slug>/projects/', TeamProjectListView.as_view(), name='team-projects'),
    path('<int:pk>/<str:slug>/projects/requests/', TeamProjectRequestListView.as_view(), name='team-project-requests'),
]
