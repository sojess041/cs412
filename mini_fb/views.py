from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Profile, StatusMessage, Image
from .forms import CreateStatusMessageForm
from mini_fb.models import Profile, Image, StatusImage 
from django.urls import reverse



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
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        '''Retrieve additional data (status messages and form) for the profile page'''
        context = super().get_context_data(**kwargs)
        context["status_messages"] = self.object.statusmessage_set.all()  # Corrected to use related_name
        context["form"] = CreateStatusMessageForm()  # Pass the form to the template
        return context

    #def post(self, request, *args, **kwargs):
        '''Handle form submission when a user posts a new status message'''
        self.object = self.get_object()  # Get the profile
        form = CreateStatusMessageForm(request.POST)

        if form.is_valid():
            new_status = form.save(commit=False)  
            new_status.profile = self.object  
            new_status.save() 
            return redirect('show_profile', pk=self.object.pk)  

        return self.get(request, *args, **kwargs)  # Re-render the page if the form is invalid

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def form_valid(self, form):
        # Get the profile associated with the form submission
        pk = self.kwargs.get("pk")
        profile = get_object_or_404(Profile, pk=pk)
        
        # Create the status message
        new_status = form.save(commit=False)
        new_status.profile = profile
        new_status.save()

        # Handle the image file(s) from the form
        files = self.request.FILES.getlist('files')  # Retrieve the uploaded files
        for image_file in files:
            image = Image(image_file=image_file, profile = profile)
            image.save()  # Save the image
            StatusImage.objects.create(status_message=new_status, image=image)

        return redirect(self.get_success_url())  # Redirect to the profile page after saving the status and image
    
    def get_success_url(self):
        """Redirect back to the profile page after posting."""
        return reverse("show_profile", kwargs={"pk": self.kwargs.get("pk")})