from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'), 
    path('order/', views.order_form, name='order'), 
    path('main/', views.main_page, name='main'), 
    path('submit/', views.submit_order, name='submit'),
]
