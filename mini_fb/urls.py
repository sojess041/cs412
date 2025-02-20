#mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView

urlpatterns = [
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'),
]