from django.db import models

class Profile(models.Model):
    '''Attributes of FB users'''

    first_name = models.CharField(max_length=50, blank=False)  
    last_name = models.CharField(max_length=50, blank=False)  
    city = models.CharField(max_length=100, blank=True)  
    email = models.EmailField(unique=True)  
    profilepic = models.URLField(blank=True)


    def __str__(self):
        '''Return a formatted string representation of the user'''
        return f'{self.first_name} {self.last_name} ({self.email})'
