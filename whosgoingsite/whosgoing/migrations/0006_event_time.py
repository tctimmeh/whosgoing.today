# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import whosgoing.models.event


class Migration(migrations.Migration):

    dependencies = [
        ('whosgoing', '0005_invite_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='time',
            field=models.DateTimeField(help_text='Time when this event normally occurs', verbose_name='Default Time', default=whosgoing.models.event.default_event_time),
            preserve_default=True,
        ),
    ]
