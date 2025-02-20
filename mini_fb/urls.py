#mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"),
]