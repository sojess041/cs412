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
    model = Profile  
    template_name = "mini_fb/show_all_profiles.html"  # HTML template to show profiles
    context_object_name = "profiles"  

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
        context["status_messages"] = self.object.statusmessage_set.all() 
        context["form"] = CreateStatusMessageForm()  
        context["friends"] = self.object.get_friends()  
        return context

 

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def form_valid(self, form):
        # Get the profile associated with the form submission
        pk = self.kwargs.get("pk")
        profile = get_object_or_404(Profile, pk=pk)
        
        new_status = form.save(commit=False)
        new_status.profile = profile
        new_status.save()

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
        return redirect('show_profile', pk=profile.pk)


    

class ShowFriendSuggestionsView(DetailView):
    "View to display friend suggestions"
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        """Pass the friend suggestions list to the template, excluding existing friends."""
        context = super().get_context_data(**kwargs)

        # Get existing friends correctly using get_friends()
        existing_friends = self.object.get_friends()

        # Get friend suggestions but exclude current friends and the profile itself
        context["friend_suggestions"] = Profile.objects.exclude(
            id__in=existing_friends.values_list('id', flat=True)
        ).exclude(id=self.object.id)

        return context

class AddFriendView(View):
    def get(self, request, pk, other_pk):
        "Handles adding a friend when button is clicked"
        profile = get_object_or_404(Profile, pk=pk)  # Profile of logged-in user
        other_profile = get_object_or_404(Profile, pk=other_pk)  # Profile to add as friend
        profile.add_friend(other_profile)  # Call method to add friend
        return redirect("show_profile", pk=profile.pk)  # Redirect back to profile page

def add_friend(request, pk, other_pk):
    profile = get_object_or_404(Profile, pk=pk)
    other_profile = get_object_or_404(Profile, pk=other_pk)
    profile.add_friend(other_profile)
    return redirect("show_profile", pk=pk)




class ShowNewsFeedView(DetailView):
    "Display News feed for profile"

    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        "Retrieve news feed"
        context = super().get_context_data(**kwargs)
        
        context["news_feed"] = self.object.get_news_feed()
        
        return context
