from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Profile, StatusMessage, Image
from .forms import CreateStatusMessageForm, CreateProfileForm
from mini_fb.models import Profile, Image, StatusImage 
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Profile
from .forms import UpdateProfileForm
from django.views.generic.edit import DeleteView
from .forms import UpdateStatusMessageForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Profile
from django.contrib.auth.forms import UserCreationForm






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
        profile = self.request.user.profile
        new_status = form.save(commit=False)
        new_status.profile = profile
        new_status.save()

        if 'files' in self.request.FILES:
            files = self.request.FILES.getlist('files')
            for image_file in files:
                image = Image(image_file=image_file, profile=profile)
                image.save()
                StatusImage.objects.create(status_message=new_status, image=image)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("show_profile", kwargs={"pk": self.request.user.profile.pk})


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
    

class AddFriendView(View):
    def get(self, request, other_pk):
        profile = request.user.profile
        other_profile = get_object_or_404(Profile, pk=other_pk)

        if profile == other_profile:
            messages.error(request, "You cannot befriend yourself.")
        else:
            success = profile.add_friend(other_profile)
            if success:
                messages.success(request, f"You are now friends with {other_profile.first_name}!")
            else:
                messages.warning(request, "Friendship already exists.")

        return redirect("show_profile", pk=profile.pk)

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
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        existing_friends = self.object.get_friends()
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
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news_feed"] = self.object.get_news_feed()
        return context




def login_view(request):
    "Handle login request from user. Will redirect to main profiles page after successful login"
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('show_all_profiles')  # Redirect after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'mini_fb/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('show_all_profiles')  # Redirect to the profiles page after logout

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'mini_fb/register.html', {'form': form})



class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        user_form = UserCreationForm(request.POST)
        profile_form = self.get_form()

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  
            profile_form.instance.user = user  
            login(request, user)  
            return self.form_valid(profile_form)  

        return self.form_invalid(profile_form)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.pk})
