from django.contrib import admin
from whosgoing.models import EventOccurrence


@admin.register(EventOccurrence)
class EventOccurrenceAdmin(admin.ModelAdmin):
    list_filter = ['event']
    ordering = ['time']

