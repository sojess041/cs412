#mini_fb/urls.py

from django.urls import path
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateStatusMessageView
from .views import UpdateProfileView, DeleteStatusMessageView

""""
urls.py file with configurations for mini_fb
"""

urlpatterns = [
    path('profiles/', ShowAllProfilesView.as_view(), name='show_all_profiles'), #route to display all profiles
    path("profile/<int:pk>/", ShowProfilePageView.as_view(), name="show_profile"), #route to display individual profile pages
    path('profile/<int:pk>/add_status/', CreateStatusMessageView.as_view(), name="add_status"),
    path('profile/<int:pk>/add/', views.CreateStatusMessageView.as_view(), name='add_status'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),






 
]

