#mini_fb/urls.py

from django.urls import path
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateStatusMessageView
from .views import UpdateProfileView, DeleteStatusMessageView, CreateFriendView, ShowFriendSuggestionsView, AddFriendView, ShowNewsFeedView
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
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path("profile/<int:pk>/add_friend/<int:other_pk>/", AddFriendView.as_view(), name="add_friend"),
    path("profile/<int:pk>/news_feed/", ShowNewsFeedView.as_view(), name="news_feed"), 









 
]

