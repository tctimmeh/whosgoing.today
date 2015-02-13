from django.contrib import admin
from whosgoing.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
