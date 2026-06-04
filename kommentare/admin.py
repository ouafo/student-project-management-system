from django.contrib import admin
from . models import Kommentar
# Register your models here.
@admin.register(Kommentar)
class KommentarAdmin(admin.ModelAdmin):
    list_display = ("aufgabe", "autor", "erstellt_am")
    search_fields = ("text",)