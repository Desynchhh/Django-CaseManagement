from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('<int:pk>/profile/', ProfileDetailView.as_view(), name='user-profile'),
    path('<int:pk>/profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
]
