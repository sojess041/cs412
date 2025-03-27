from django.contrib import admin
from .models import Profile, StatusMessage, Image, StatusImage, Friend

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')
    list_filter = ('user',)

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

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_dislay = ('profile1', 'profile2', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('profile1__first_name', 'profile2__first_name')

