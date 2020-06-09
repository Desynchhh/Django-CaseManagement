from django.urls import path
from .views import (
    # TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView
)

urlpatterns = [
    # path('<int:pk>/<str:slug>/', TeamListView.as_view(), name='team-index'),
    path('<int:pk>/<str:slug>/details/', TeamDetailView.as_view(), name='team-detail'),
    path('<int:pk>/<str:slug>/update/', TeamUpdateView.as_view(), name='team-update'),
    path('create/', TeamCreateView.as_view(), name='team-create'),
]
