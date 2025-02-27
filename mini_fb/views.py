from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Profile, StatusMessage
from .forms import CreateStatusMessageForm

"""
Class-based views to display all profiles and individual profile pages.
"""


class ShowAllProfilesView(ListView):
    '''Display all profiles'''
    model = Profile  # User profile model
    template_name = "mini_fb/show_all_profiles.html"  # HTML template to show profiles
    context_object_name = "profiles"  # Context variable to access profile data

    def get_queryset(self):
        '''Retrieve all profile objects from the database'''
        queryset = Profile.objects.all()
        print("Profiles in DB:", queryset)
        return queryset


class ShowProfilePageView(DetailView): 
    '''Obtain data for one Profile record'''
    model = Profile  # Use profile model
    template_name = "mini_fb/show_profile.html"  # HTML for single profile page
    context_object_name = "profile"  # Context variable to access single profile data

    def get_context_data(self, **kwargs):
        '''Retrieve additional data (status messages and form) for the profile page'''
        context = super().get_context_data(**kwargs)
        context["status_messages"] = self.object.status_messages.all()  # Get all status messages for this profile
        context["form"] = CreateStatusMessageForm()  # Pass the form to the template
        return context    

    def post(self, request, *args, **kwargs):
        '''Handle form submission when a user posts a new status message'''
        self.object = self.get_object()  # Get the profile
        form = CreateStatusMessageForm(request.POST)

        if form.is_valid():
            new_status = form.save(commit=False)  
            new_status.profile = self.object  # Assign the current profile
            new_status.save()  # Save the message
            return redirect('show_profile', pk=self.object.pk)  

        return self.get(request, *args, **kwargs)  # Re-render the page if the form is invalid


class CreateStatusMessageView(CreateView):
    """
    View to handle creating a new status message.
    """
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
        """Assign the status message to the correct profile before saving."""
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        new_status = form.save(commit=False)
        new_status.profile = profile  # Assign the profile to the status message
        new_status.save()
        return redirect('show_profile', pk=profile.pk)


    
