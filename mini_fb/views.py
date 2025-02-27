from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile  


"""
Class-based views to display all profiles and individual profile pages.
"""


class ShowAllProfilesView(ListView):
    '''display all profiles'''
    model = Profile #User profile model 
    template_name = "mini_fb/show_all_profiles.html" #HTML template to show profiles
    context_object_name = "profiles" #context variable to access profile data 

    def get_queryset(self):
        '''retrieve all profile objects from the database'''
        queryset = Profile.objects.all()
        print("Profiles in DB:", queryset) 
        return queryset

class ShowProfilePageView(DetailView): 
    '''Obtain data for one Profile record'''
    model = Profile #use profile model 
    template_name = "mini_fb/show_profile.html" #HTML for single profile page
    context_object_name = "profile" #context variable to access single profile data 

    def get_context_data(self, **kwargs):
         '''Retrieve additional data (status messages) for the profile page'''
         context = super().get_context_data(**kwargs)
         context["status_messages"] = self.object.status_messages.all()  # Get all status messages for this profile
         return context       