from django.urls import path
from .views import (
    # TeamListView,
    TeamNewUserView,
    TeamDetailView,
    TeamAddUser,
    TeamUserUpdate,
    TeamCreateView,
    TeamUpdateView,
    TeamProjectListView,
    TeamProjectRequestListView
)

urlpatterns = [
    # path('<int:pk>/<str:slug>/', TeamListView.as_view(), name='team-index'),
    path('new-user/', TeamNewUserView.as_view(), name='team-new-user'),
    path('<int:pk>/<str:slug>/', TeamDetailView.as_view(), name='team-detail'),
    path('<int:pk>/<str:slug>/users/add/', TeamAddUser.as_view(), name='team-add-user'),
    path('<int:tpk>/<str:slug>/users/<int:pk>/update/', TeamUserUpdate.as_view(), name='team-user-update'),
    path('<int:pk>/<str:slug>/update/', TeamUpdateView.as_view(), name='team-update'),
    path('create/', TeamCreateView.as_view(), name='team-create'),
    path('<int:pk>/<str:slug>/projects/', TeamProjectListView.as_view(), name='team-projects'),
    path('<int:pk>/<str:slug>/projects/requests/', TeamProjectRequestListView.as_view(), name='team-project-requests'),
]
