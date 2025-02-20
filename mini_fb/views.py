from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile  


"""""
Class based views to display all profiles and separate profiles 
"""""

class ShowAllProfilesView(ListView):
    '''display all profiles'''
    model = Profile #User profile model 
    template_name = "mini_fb/show_all_profiles.html" #HTML template to show profiles
    context_object_name = "profiles" #context variable to access profile data 

    def get_queryset(self):
        '''retrieve all profile objects from the database'''
        return Profile.objects.all() 

class ShowProfilePageView(DetailView): 
    '''Obtain data for one Profile record'''
    model = Profile #use profile model 
    template_name = "mini_fb/show_profile.html" #HTML for single profile page
    context_object_name = "profile" #context variable to access single profile data 
