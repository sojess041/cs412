from django.contrib import admin
from .models import Profile, StatusMessage, Image, StatusImage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'city', 'image_file')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

@admin.register(StatusMessage)
class StatusMessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'text', 'created_at')
    ordering = ('-created_at',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("profile", "image_file", "uploaded_at")
    search_fields = ('profile',)
    ordering = ('-uploaded_at',)

@admin.register(StatusImage)
class StatusImageAdmin(admin.ModelAdmin):
    list_display = ("status_message", "image")
    search_fields = ('status_message', 'image')
