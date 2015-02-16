from django.contrib import admin
from django.contrib.admin import TabularInline
from whosgoing.models import Event, EventMember


class EventMemberInline(TabularInline):
    model = EventMember
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = (EventMemberInline,)
