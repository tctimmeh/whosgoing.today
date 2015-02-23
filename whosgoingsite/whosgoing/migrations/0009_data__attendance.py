# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.migrations import RunPython


def create_attendance_values(apps, schema_editor):
    Attendance = apps.get_model('whosgoing', 'Attendance')
    Attendance.objects.bulk_create([
        Attendance(pk=1, name='Undecided'),
        Attendance(pk=2, name='Accept'),
        Attendance(pk=3, name='Regret'),
    ])

def remove_attendance_values(apps, schema_editor):
    Attendance = apps.get_model('whosgoing', 'Attendance')
    Attendance.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('whosgoing', '0008_occurence_member'),
    ]

    operations = [
        RunPython(create_attendance_values, remove_attendance_values)
    ]
