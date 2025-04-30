from django.contrib import admin
from .models import UserProfile, SheetMusic, Tag, Favorite, Rating


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('skill_level', 'favorite_genre')
    search_fields = ('username', 'email')

class SheetMusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'composer', 'difficulty', 'category')

admin.site.register(SheetMusic, SheetMusicAdmin)

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0

class SheetMusicAdmin(admin.ModelAdmin):
    inlines = [RatingInline]



admin.site.register(Tag)
admin.site.register(Favorite)
