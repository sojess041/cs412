from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Profile, StatusMessage, Image
from .forms import CreateStatusMessageForm
from mini_fb.models import Profile, Image, StatusImage 
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Profile
from .forms import UpdateProfileForm
from django.views.generic.edit import DeleteView
from .forms import UpdateStatusMessageForm
from django.contrib import messages
from django.views import View

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
        '''Retrieve additional data (status messages, friends, and form) for the profile page'''
        context = super().get_context_data(**kwargs)
        context["status_messages"] = self.object.statusmessage_set.all()  # Fetch status messages
        context["form"] = CreateStatusMessageForm()  # Pass the form to the template
        context["friends"] = self.object.get_friends()  
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

        # Handle image upload
        if 'files' in self.request.FILES:
            files = self.request.FILES.getlist('files')  # Retrieve the uploaded files
            for image_file in files:
                image = Image(image_file=image_file, profile=profile)
                image.save()
                StatusImage.objects.create(status_message=new_status, image=image)

        return super().form_valid(form)

    def get_success_url(self):
        """Redirect back to the profile page after posting."""
        return reverse("show_profile", kwargs={"pk": self.kwargs.get("pk")})

class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
    def get_object(self, queryset=None):
        # Retrieve the Profile object based on the primary key from the URL
        return get_object_or_404(Profile, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        # Redirect to the profile page after the update
        return reverse('show_profile', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        # Handle form submission, including file uploads
        profile = form.save(commit=False)
        
        # If there's an image uploaded, handle the image field
        if 'image_file' in self.request.FILES:
            profile.image_file = self.request.FILES['image_file']
        
        # Save the profile and the uploaded file if applicable
        profile.save()
        return super().form_valid(form)



class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/confirm_delete.html'
    context_object_name = 'status_message'

    def get_object(self, queryset=None):
        # Get the status message object based on the pk in the URL
        return get_object_or_404(StatusMessage, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        # Redirect back to the profile page after deleting the status message
        return reverse_lazy('show_profile', kwargs={'pk': self.object.profile.pk})

class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    template_name = 'mini_fb/update_status_form.html'
    fields = ['text']

    def get_object(self, queryset=None):
        return get_object_or_404(StatusMessage, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the status object to the context
        context['status'] = self.get_object()
        return context

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

def add_friend_view(request, profile_id, friend_id):
    """
    Function-based view to add a friendship between two Profile instances.
    Prevents self-friending and duplicate friendships.
    """
    profile = get_object_or_404(Profile, id=profile_id)
    friend = get_object_or_404(Profile, id=friend_id)

    if profile == friend:
        messages.error(request, "You cannot befriend yourself!")
    else:
        existing_friend = Profile.add_friend(profile, friend)
        if existing_friend:
            messages.success(request, f"You are now friends with {friend.first_name}!")
        else:
            messages.warning(request, "Friendship already exists.")

    return redirect('show_profile', pk=profile_id)

class CreateFriendView(View):
    "Add a friend using a URL"
    
    def dispatch(self, request, *args, **kwargs):
        "Handles the request to add a friend using URL parameters"
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other = get_object_or_404(Profile, pk=self.kwargs['other_pk'])

        if profile == other:
            messages.error(request, "You cannot befriend yourself")
        else:
            existing_friend = profile.add_friend(other)
            if existing_friend:
                messages.success(request, "You are now friends with {other.first_name}")
            else:
                messages.warning(request, "Friendship already exists.")
        return redirect('profile_detail', pk=profile.pk)


    

class ShowFriendSuggestionsView(DetailView):
    """
    View to display friend suggestions for a specific Profile.
    """
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """Pass the friend suggestions list to the template."""
        context = super().get_context_data(**kwargs)
        context["friend_suggestions"] = self.object.get_friend_suggestions()
        return context

