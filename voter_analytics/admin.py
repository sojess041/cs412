from django.contrib import admin
from .models import Voter

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'party', 'voter_score']
