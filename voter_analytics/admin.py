from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Voter

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'party_affiliation', 'voter_score')
    search_fields = ('last_name', 'first_name', 'zip_code')
