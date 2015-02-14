from django.contrib import admin
from whosgoing.models import EmailInvitation


@admin.register(EmailInvitation)
class EmailInvitationAdmin(admin.ModelAdmin):
    readonly_fields = ['sent']

