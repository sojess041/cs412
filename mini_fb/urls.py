#mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

""""
urls.py file with configurations for mini_fb
"""

urlpatterns = [
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'), #route to display all profiles
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"), #route to display individual profile pages 
]