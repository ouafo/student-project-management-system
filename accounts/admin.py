from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Benutzer


@admin.register(Benutzer)
class BenutzerAdmin(UserAdmin):

    # Spalten in der Übersichtsliste
    list_display = (
        'username', 'email',
        'first_name', 'last_name',
        'is_staff', 'is_active', 'erstellt_am'
    )

    list_filter  = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering     = ('-erstellt_am',)

    # Bearbeitungsformular – eigene Felder hinzufügen
    fieldsets = UserAdmin.fieldsets + (
        ('Zusätzliche Informationen', {
            'fields': ('profilbild', 'erstellt_am')
        }),
    )

    # erstellt_am ist auto_now_add → nur lesbar
    readonly_fields = ('erstellt_am',)

    # Erstellungsformular
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Zusätzliche Informationen', {
            'fields': ('profilbild',)
        }),
    )