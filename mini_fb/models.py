from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

""""
models.py file to degine the Profile model for mini_fb 
"""

class Profile(models.Model):
    '''Attributes of FB users'''

    first_name = models.CharField(max_length=50, blank=False)  #first name field
    last_name = models.CharField(max_length=50, blank=False)  #last name field 
    city = models.CharField(max_length=100, blank=True)  #city field 
    email = models.EmailField(unique=True)  # email field 
    profilepic = models.URLField(blank=True) #profile picture URL 


    def __str__(self):
        '''Return a formatted string representation of the user'''
        return f'{self.first_name} {self.last_name} ({self.email})'

class StatusMessage(models.Model):
    "Represent status message for MINIFB"
    timestamp = models.DateTimeField(default = now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')


    def __str__(self):
        "Return a string representation of the StatusMessage"
        return f"{self.profile.first_name} {self.profile.last_name} - {self.timestamp}: {self.message[:50]}"  # Display first 50 chars
