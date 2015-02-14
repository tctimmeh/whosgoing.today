from django.contrib import admin
from whosgoing.models import Invitation


@admin.register(Invitation)
class EmailInvitationAdmin(admin.ModelAdmin):
    readonly_fields = ['sent']

