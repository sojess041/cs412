from django.contrib import admin
from .models import Profile  
from .models import StatusMessage

""""
admin.py file that registers the Profile model with the Django admin site 
"""

admin.site.register(Profile)  


class StatusMessageAdmin(admin.ModelAdmin):
    "Admin configuration for the StatusMessage model"
    "customize the display of status messages in the django admin"
    list_display = ('profile', 'timestamp', 'message')
    search_fields = ('message', 'profile__user__username')
    ordering = ('-timestamp',)
admin.site.register(StatusMessage, StatusMessageAdmin)