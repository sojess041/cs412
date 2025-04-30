from django.urls import path 
from .views import SheetMusicListView, upload_sheet
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import SheetMusicDeleteView


app_name = 'project'
urlpatterns = [
    path('upload/', views.upload_sheet, name='upload_sheet'),  
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),
    path('register/', views.register, name="register"), 
    path('sheets/', SheetMusicListView.as_view(), name='sheet_list'),
    path('delete/<int:pk>/', SheetMusicDeleteView.as_view(), name='delete_sheet'),
    path('send-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-requests/', views.view_friend_requests, name='view_friend_requests'),
    path('users/', views.view_users, name='view_users'),
    path('toggle-favorite/<int:sheet_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorite/<int:sheet_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('profile/', views.profile, name='profile'),
    path('sheet/<int:sheet_id>/', views.sheet_detail, name='sheet_detail'),
    path('rate/<int:sheet_id>/', views.rate_sheet, name='rate_sheet'),

    path('rate_sheet/<int:sheet_id>/<int:score>/', views.rate_sheet, name='rate_sheet'),
    path('sheet/<int:sheet_id>/', views.sheet_detail, name='sheet_detail'),
    path('status/', views.status_page, name='status_page'),

]


