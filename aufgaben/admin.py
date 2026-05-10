from django.contrib import admin
from .models import Aufgabe, Kommentar


class KommentarInline(admin.TabularInline):
    model = Kommentar
    extra = 0


@admin.register(Aufgabe)
class AufgabeAdmin(admin.ModelAdmin):
    list_display = ("titel", "status", "prioritaet", "zugewiesen_an", "erstellt_von", "deadline")
    list_filter = ("status", "prioritaet")
    search_fields = ("titel", "beschreibung")
    inlines = [KommentarInline]


@admin.register(Kommentar)
class KommentarAdmin(admin.ModelAdmin):
    list_display = ("aufgabe", "autor", "erstellt_am")
    search_fields = ("text",)