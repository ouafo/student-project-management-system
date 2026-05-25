from django.contrib import admin
from .models import Projekt
# Register your models here.


@admin.register(Projekt)
class ProjektAdmin(admin.ModelAdmin):
    list_display = ('name', 'besitzer', 'erstellt_am')