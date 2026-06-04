from django.contrib import admin
from .models import Aufgabe
from kommentare.models import Kommentar


class KommentarInline(admin.TabularInline):
    model = Kommentar
    extra = 0


@admin.register(Aufgabe)
class AufgabeAdmin(admin.ModelAdmin):
    list_display = (
        "titel", "projekt", "status",
        "prioritaet", "zugewiesen_an",
        "erstellt_von", "deadline"
    )
    list_filter = ("status", "prioritaet")
    search_fields = ("titel", "beschreibung")
    inlines = [KommentarInline]
