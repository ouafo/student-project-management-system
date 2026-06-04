from django.contrib import admin
from .models import Projekt, Mitgliedschaft, Profile
# Register your models here.


@admin.register(Projekt)
class ProjektAdmin(admin.ModelAdmin):
    list_display = ['titel', 'admin', 'erstellt_am']

@admin.register(Mitgliedschaft)
class MitgliedschaftAdmin(admin.ModelAdmin):
    list_display = ['user', 'projekt', 'beigetreten_am']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']