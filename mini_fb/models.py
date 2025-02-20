from django.db import models

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
