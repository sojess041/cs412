#mini_fb/urls.py

from django.urls import path
from . import views
from .views import ShowAllProfilesView, ShowProfilePageView, CreateStatusMessageView
from .views import UpdateProfileView, DeleteStatusMessageView, CreateFriendView, ShowFriendSuggestionsView, AddFriendView, ShowNewsFeedView
""""
urls.py file with configurations for mini_fb
"""

urlpatterns = [
    # General profile views
    path('profiles/', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),

    # Routes using logged-in user’s profile
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/friend_suggestions/', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed/', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path('profile/add_friend/<int:other_pk>/', views.AddFriendView.as_view(), name='add_friend'),

    # Status messages
    path('status/create_status/', views.CreateStatusMessageView.as_view(), name='create_status'),
    path('status/<int:pk>/delete/', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', views.UpdateStatusMessageView.as_view(), name='update_status'),

    # Auth routes
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
