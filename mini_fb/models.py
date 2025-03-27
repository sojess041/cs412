from django.db import models
from django.utils.timezone import now
from django.db.models import Q
from django.contrib.auth.models import User


class Profile(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    image_file = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    # Add bio and location fields
    bio = models.TextField(blank=True, null=True)  # Add bio field
    location = models.CharField(max_length=100, blank=True, null=True)  # Add location field

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def get_friends(self):
        """Returns a list of the profile's friends from the Friend model."""
        from .models import Friend  # Move import inside the function to avoid circular import errors
    
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        return Profile.objects.filter(id__in=friend_ids)


    def add_friend(self, other):
        "Adds a freindship between current Profile and another profile"
        from .models import Friend
        
        if self == other: #Avoid self friending 
            return 
        
        existing_friend = Friend.objects.filter(models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
).exists()
        if existing_friend:
            print("Friendship already exists")

        else:
            Friend.objects.create(profile1 = self, profile2 = other)
            print(f" Friendship added: {self.first_name} & {other.first_name}")


    def get_news_feed(self):
        """Returns status messages from the profile and all of their friends."""
        from .models import StatusMessage  # Import to avoid circular import issues
        
        friends = self.get_friends()  # Get all friends
        friend_ids = friends.values_list("id", flat=True)  # Extract friend IDs as a list

        # Get status messages from the profile and friends, ordered by newest first
        news_feed = StatusMessage.objects.filter(
            Q(profile=self) | Q(profile__id__in=friend_ids)
        ).order_by("-created_at")  # Newest messages first

        return news_feed  # Returns a QuerySet



    def get_friend_suggestions(self):
        "return a list (or QuerySet) of possible friends for a Profile"

        from .models import Friend 
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile2', flat=True)

        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        return Profile.objects.exclude(id__in=friend_ids + [self.id])



class Image(models.Model):
    "Represent image uploaded by user "
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.profile.first_name} {self.profile.last_name}"


class StatusMessage(models.Model):
    "Represent status message posted by user"
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Status by {self.profile} on {self.created_at}"

class StatusImage(models.Model):
    "associate image with status message"
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.status_message.text}"
    
    def get_images(self):
        "get all images linked to a specific status message"
        return StatusImage.objects.filter(status_message=self)
    

class Friend(models.Model): 
    "represent friendship between two profiles"
    
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friendships1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friendships2")
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"


