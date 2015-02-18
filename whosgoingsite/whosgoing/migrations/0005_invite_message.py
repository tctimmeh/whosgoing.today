# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whosgoing', '0004_event_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='from_name',
            field=models.CharField(max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='message',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
