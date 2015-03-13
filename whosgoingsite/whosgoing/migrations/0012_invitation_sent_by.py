# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whosgoing', '0011_event_notify_addresses'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='sent_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='event',
            field=models.ForeignKey(to='whosgoing.Event', related_name='invitations'),
            preserve_default=True,
        ),
    ]
