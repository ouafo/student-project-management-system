from django.contrib import admin
from . models import ChatNachricht
# Register your models here.
@admin.register(ChatNachricht)
class ChatNachrichtAdmin(admin.ModelAdmin):
    list_display = ("sender", "empfaenger", "erstellt_am")