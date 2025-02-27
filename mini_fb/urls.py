#mini_fb/urls.py

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateStatusMessageView

""""
urls.py file with configurations for mini_fb
"""

urlpatterns = [
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'), #route to display all profiles
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"), #route to display individual profile pages
    path('profile/<int:pk>/add_status/', CreateStatusMessageView.as_view(), name="add_status"),
 
]

