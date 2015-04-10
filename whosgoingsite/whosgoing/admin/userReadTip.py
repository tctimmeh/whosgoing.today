from django.contrib import admin
from django.contrib.admin import ModelAdmin
from whosgoing.models import UserReadTip


@admin.register(UserReadTip)
class UserReadTipAdmin(ModelAdmin):
    search_fields = ['user', 'entry']
