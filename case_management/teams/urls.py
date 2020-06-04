from django.urls import path
from .views import TeamListView, TeamDetailView

urlpatterns = [
    path('<int:pk>/<str:slug>/', TeamListView.as_view(), name='team-index'),
    path('<int:pk>/<str:slug>/details/', TeamDetailView.as_view(), name='team-detail'),
]
