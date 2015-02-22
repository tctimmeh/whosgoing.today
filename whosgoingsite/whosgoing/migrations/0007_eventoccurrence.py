# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('whosgoing', '0006_event_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventOccurrence',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(related_name='occurrences', to='whosgoing.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
