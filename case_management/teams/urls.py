from django.urls import path
from .views import TeamListView, TeamDetailView

urlpatterns = [
    path('', TeamListView.as_view(), name='team-index'),
    path('<int:pk>/<str:slug>/', TeamDetailView.as_view(), name='team-detail'),
]
