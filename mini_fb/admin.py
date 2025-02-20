from django.contrib import admin
from .models import Profile  

""""
admin.py file that registers the Profile model with the Django admin site 
"""

admin.site.register(Profile)  
