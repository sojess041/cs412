from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Profile(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    image_file = models.ImageField(upload_to='profile_images/', blank=True, null=True) 

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
    
    def get_friends(self):
        "returns a list representing the profile's friends"
        friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)

        friend_ids = list(friends_as_profile1) + list(friends_as_profile2)
        return Profile.objects.filter(id__in=friend_ids)




class Image(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.profile.first_name} {self.profile.last_name}"


class StatusMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Status by {self.profile} on {self.created_at}"

class StatusImage(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.status_message.text}"
    
    def get_images(self):
        return StatusImage.objects.filter(status_message=self)
    

class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friendships1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="friendships2")
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"


