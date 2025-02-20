from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

class ShowAllProfilesView(ListView):
    '''display all profiles'''
    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

    def get_queryset(self):
        return Profile.objects.all()  # Force Django to fetch profiles
